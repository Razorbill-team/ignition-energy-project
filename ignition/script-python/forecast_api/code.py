# project library: forecast_api
import system, re

HHMM = re.compile(r"^(\d{1,2}):(\d{2})$")   # "08:00", "08:15", ...

def _to_float(x):
    if x is None: return None
    if isinstance(x, (int, float)): return float(x)
    s = unicode(x).strip().replace(" ", "").replace(",", ".")
    try: return float(s)
    except: return None

def _slot_ts(base_date, hh, mm):
    return system.date.setTime(base_date, int(hh), int(mm), 0)

def save_four_rows(payload, datasource="YourDS", db_kind="oracle"):
    rows = payload.get("rows") or []
    if not rows: return {"inserted": 0, "errors": ["no rows provided"]}

    date_str = payload.get("date")
    if not date_str: return {"inserted": 0, "errors": ["missing date (YYYY-MM-DD)"]}

    try:
        base_date = system.date.parse(date_str, "yyyy-MM-dd")
        siteid = int(payload.get("siteid"))
        farmid = int(payload.get("farmid"))
        userid = payload.get("userid", None)
        userid = None if userid in (None, "", "null") else int(userid)
        interval_minutes = int(payload.get("interval_minutes", 15))
    except Exception, e:
        return {"inserted": 0, "errors": [unicode(e)]}

    table_map = {
        "avg_sources":       ("forecast.avg_forecast_settings",    "avg_value"),
        "auto_correction":   ("forecast.auto_forecast_settings",   "auto_value"),
        "manual_correction": ("forecast.manual_forecast_settings", "manual_correction"),
        "final_forecast":    ("forecast.final_forecast_settings",  "final_value"),
    }

    tx = system.db.beginTransaction(datasource)
    inserted, errors = 0, []
    try:
        for r in rows:
            key = unicode(r.get("Source_name","")).strip().lower()
            if key not in table_map: 
                continue
            tab, col = table_map[key]

            for k, v in r.items():
                m = HHMM.match(unicode(k))
                if not m: 
                    continue
                val = _to_float(v)
                if val is None: 
                    continue

                hh, mm = int(m.group(1)), int(m.group(2))
                if mm not in (0, 15, 30, 45): 
                    continue

                slot_ts = _slot_ts(base_date, hh, mm)

                if db_kind == "oracle":
                    sql = u"""
                    MERGE INTO {tab} t
                    USING (
                      SELECT ? AS slot_ts, ? AS datetime,
                             TO_DATE(?, 'YYYY-MM-DD') AS data,
                             ? AS hour, ? AS interval_minutes,
                             ? AS siteid, ? AS farmid,
                             ? AS {col}, ? AS userid
                      FROM dual
                    ) s
                    ON (t.siteid=s.siteid AND t.farmid=s.farmid AND t.slot_ts=s.slot_ts)
                    WHEN MATCHED THEN UPDATE SET
                      t.datetime=s.datetime, t.data=s.data, t.hour=s.hour, t.interval_minutes=s.interval_minutes,
                      t.{col}=s.{col}, t.userid=s.userid
                    WHEN NOT MATCHED THEN INSERT
                      (slot_ts, datetime, data, hour, interval_minutes, siteid, farmid, {col}, userid, date_from, date_to)
                      VALUES (s.slot_ts, s.datetime, s.data, s.hour, s.interval_minutes, s.siteid, s.farmid, s.{col}, s.userid, NULL, NULL)
                    """.format(tab=tab, col=col)
                elif db_kind == "postgres":
                    sql = u"""
                    INSERT INTO {tab} (slot_ts, datetime, data, hour, interval_minutes, siteid, farmid, {col}, userid, date_from, date_to)
                    VALUES (?, ?, TO_DATE(?, 'YYYY-MM-DD'), ?, ?, ?, ?, ?, ?, NULL, NULL)
                    ON CONFLICT (siteid, farmid, slot_ts) DO UPDATE SET
                      datetime=EXCLUDED.datetime, data=EXCLUDED.data, hour=EXCLUDED.hour, interval_minutes=EXCLUDED.interval_minutes,
                      {col}=EXCLUDED.{col}, userid=EXCLUDED.userid
                    """.format(tab=tab, col=col)
                else:
                    raise Exception("Unsupported db_kind: " + db_kind)

                args = [slot_ts, slot_ts, date_str, hh, interval_minutes, siteid, farmid, val, userid]
                system.db.runPrepUpdate(sql, args, datasource, tx)
                inserted += 1

        system.db.commitTransaction(tx)
        return {"inserted": inserted, "errors": []}
    except Exception, e:
        system.db.rollbackTransaction(tx)
        return {"inserted": inserted, "errors": [unicode(e)]}
    finally:
        system.db.closeTransaction(tx)