def doGet(request, session):

    """
    Returns:
      {
        "columns": ["KPI","01","02",...,"24"],
        "rows": [ {"KPI": "<label>", "01": <int>, ..., "24": <int>}, ... ],
        "debug": {...}
      }
    """
    import system
    from datetime import datetime
    # ---------- read params ----------
    params_in = request.get("params") or {}
    day = params_in.get("day")

    # If day is given, build full-day window; else accept date_from/date_to
    if day:
        date_from = "%s 00:00:00" % day
        date_to   = "%s 23:00:00" % day
    else:
        date_from = params_in.get("date_from")
        date_to   = params_in.get("date_to")
        # safe fallbacks if not provided
        if not date_from or not date_to:
            today = datetime.now().strftime("%Y-%m-%d")
            date_from = date_from or (today + " 00:00:00")
            date_to   = date_to   or (today + " 23:00:00")

    # ---------- run Named Query ----------
    NQ_PATH = "Output/OutputForecast"   # your Named Query path
    try:
        ds = system.db.runNamedQuery(NQ_PATH, {
            "date_from": date_from,
            "date_to": date_to
        })
    except Exception as ex:
        return {
            "json": {
                "error": "NamedQuery failed",
                "detail": str(ex),
                "debug": {"path": NQ_PATH, "date_from": date_from, "date_to": date_to}
            }
        }

    # ---------- define matrix ----------
    HH = ["%02d" % h for h in range(1, 25)]
    columns = ["KPI"] + HH

    # KPI order to display (exactly like your screenshot)
    ROW_LABELS = [
        "BESS Charge  PV",
        "BESS Charge WT",
        "BESS Charge Grid",
        "BESS Charge Gas",
        "BESS Charge FCR",
        "BESS Charge mFRR dw",
        "BESS AN FCR reservation up",
        "BESS AN FCR reservation dw",
        "BESS AN MFRR reservation up",
        "BESS AN MFRR reservation dw",
        "Band out BESS (discharge)",
        "Band out WT (To grid from WT)",
        "Band out PV (To grid from PV)",
        "Band out GAS",
        "EBand out BESS (discharge)",
        "EBand out WT (To grid from WT)",
        "EBand out PV (To grid from PV)",
        "EBand out GAS",
        "BESS discharge FCR up",
        "BESS discharge mFRR up",
        "BAL market out WT (To grid from WT)",
        "BAL market out PV (To grid from PV)",
        "BAL market out GAS",
    ]

    # For each display label, list possible column names we can read.
    # (Your Named Query uses the first alias with spaces; the second entry is the raw field name fallback.)
    COL_CANDIDATES = {
        "BESS Charge  PV":                     ["BESS Charge  PV", "ch_bess_from_pv"],
        "BESS Charge WT":                      ["BESS Charge WT", "ch_bess_from_wt"],
        "BESS Charge Grid":                    ["BESS Charge Grid", "ch_bess_from_grid"],
        "BESS Charge Gas":                     ["BESS Charge Gas", "ch_bess_from_gas"],
        "BESS Charge FCR":                     ["BESS Charge FCR", "ch_bess_from_fcr_dn"],
        "BESS Charge mFRR dw":                 ["BESS Charge mFRR dw", "ch_bess_from_mfrr_dn"],
        "BESS AN FCR reservation up":          ["BESS AN FCR reservation up", "res_bess_fcr_up"],
        "BESS AN FCR reservation dw":          ["BESS AN FCR reservation dw", "res_bess_fcr_dn"],
        "BESS AN MFRR reservation up":         ["BESS AN MFRR reservation up", "res_bess_mfrr_up"],
        "BESS AN MFRR reservation dw":         ["BESS AN MFRR reservation dw", "res_bess_mfrr_dn"],
        "Band out BESS (discharge)":           ["Band out BESS (discharge)", "out_bess"],
        "Band out WT (To grid from WT)":       ["Band out WT (To grid from WT)", "out_wt"],
        "Band out PV (To grid from PV)":       ["Band out PV (To grid from PV)", "out_pv"],
        "Band out GAS":                        ["Band out GAS", "out_gas"],
        "EBand out BESS (discharge)":          ["EBand out BESS (discharge)", "eband_out_bess_dch"],
        "EBand out WT (To grid from WT)":      ["EBand out WT (To grid from WT)", "eband_out_wt"],
        "EBand out PV (To grid from PV)":      ["EBand out PV (To grid from PV)", "eband_out_pv"],
        "EBand out GAS":                       ["EBand out GAS", "eband_out_gas"],
        "BESS discharge FCR up":               ["BESS discharge FCR up", "act_bess_fcr_up"],
        "BESS discharge mFRR up":              ["BESS discharge mFRR up", "act_bess_mfrr_up"],
        "BAL market out WT (To grid from WT)": ["BAL market out WT (To grid from WT)", "bal_out_wt"],
        "BAL market out PV (To grid from PV)": ["BAL market out PV (To grid from PV)", "bal_out_pv"],
        "BAL market out GAS":                  ["BAL market out GAS", "bal_out_gas"],
    }

    # choose first existing column for each label
    pds = system.dataset.toPyDataSet(ds)
    colnames = set([c for c in pds.getColumnNames()])

    label_to_col = {}
    for label, candidates in COL_CANDIDATES.items():
        chosen = None
        for c in candidates:
            if c in colnames:
                chosen = c
                break
        label_to_col[label] = chosen  # may be None if missing

    # hour buckets: "01".."24" -> { label -> value }
    buckets = dict((h, {}) for h in HH)

    def to_dt(x):
        # Accept Java Date/Timestamp or ISO-string
        try:
            if hasattr(x, "getTime"):
                return datetime.fromtimestamp(x.getTime()/1000.0)
        except:
            pass
        try:
            s = str(x).strip()
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M:%S"):
                try:
                    return datetime.strptime(s, fmt)
                except:
                    pass
        except:
            pass
        return None

    # prefer 'slot_ts', else 'datetime' or 'date_from'
    slot_field = "slot_ts" if "slot_ts" in colnames else ("datetime" if "datetime" in colnames else ("date_from" if "date_from" in colnames else None))

    for r in pds:
        hh = None
        if slot_field:
            dt = to_dt(r[slot_field])
            if dt is not None:
                hh = "%02d" % ((dt.hour % 24) + 1)  # 1..24
        if hh not in buckets:
            continue

        # put each KPI for that hour
        for label in ROW_LABELS:
            src_col = label_to_col.get(label)
            if not src_col:
                continue
            try:
                val = r[src_col]
            except Exception:
                val = 0
            # coerce to int
            try:
                val = 0 if val is None else int(float(str(val).replace(",", ".")))
            except Exception:
                val = 0
            buckets[hh][label] = val

    # build final rows
    rows = []
    for label in ROW_LABELS:
        row = {"KPI": label}
        for h in HH:
            row[h] = buckets[h].get(label, 0)
        rows.append(row)

    return {
        "json": {
            "columns": columns,
            "rows": rows,
            "debug": {
                "rowcount": pds.getRowCount(),
                "date_from": date_from,
                "date_to": date_to
            }
        }
    }