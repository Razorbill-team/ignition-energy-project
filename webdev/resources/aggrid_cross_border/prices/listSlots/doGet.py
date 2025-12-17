def doGet(request, session):
	# WebDev Scripted Resource: aggrid_market_prices/section/listSections
	# HTTP Method: GET -> doGet(request)
	
	import system
	from java.text import SimpleDateFormat
	from java.util import TimeZone, Date as JDate
	
	LOG = system.util.getLogger("WebDev.CrossBorder.listSections")
	
	def fmt_price(v):
	    """No decimals for prices."""
	    if v is None:
	        return ""
	    try:
	        return str(int(round(float(str(v).replace(",", ".")))))
	    except:
	        return str(v)
	
	def fmt_quantity(v):
	    """No decimals for quantities."""
	    if v is None:
	        return ""
	    try:
	        return str(int(round(float(str(v).replace(",", ".")))))
	    except:
	        return str(v)
	
	# ---------- 1) Read params ----------
	p = request.get("params", {}) or request.get("get", {}) or {}
	
	from_in   = (p.get("from")   or "").strip()
	to_in     = (p.get("to")     or "").strip()
	area_in   = (p.get("area")   or "").strip()
	
	area = area_in.upper()
	if area in ("ALL", "ALL AREAS"):
	    area = ""   # all areas
	
	LOG.info("Raw params from UI: from=%s, to=%s, area=%s"
	         % (from_in, to_in, area or "ALL"))
	
	# ---------- 2) Default / normalize dates ----------
	TZ       = TimeZone.getTimeZone("Europe/Chisinau")
	OUT_DATE = SimpleDateFormat("yyyy-MM-dd")
	OUT_DATE.setTimeZone(TZ)
	
	now = system.date.now()
	
	if from_in:
	    date_from = from_in
	else:
	    d_from = system.date.addDays(now, -1)
	    date_from = OUT_DATE.format(d_from)
	
	if to_in:
	    date_to = to_in
	else:
	    d_to = system.date.addDays(now, 1)
	    date_to = OUT_DATE.format(d_to)
	
	LOG.info("Using DateFrom=%s DateTo=%s Area=%s"
	         % (date_from, date_to, area or "ALL"))
	
	# ---------- 3) Run Named Query ----------
	nq_params = {
	    "DateFrom": date_from,
	    "DateTo":   date_to
	    # area is derived in SQL as 'RO'/'UA' and filtered below
	}
	
	try:
	    ds = system.db.runNamedQuery("CrossBorder/Cross_Border_Market", nq_params)
	except Exception, ex:
	    LOG.error("NamedQuery CrossBorder/Cross_Border_Market failed: %r" % ex)
	    return {"json": [], "error": "NamedQuery error: %s" % ex}
	
	# ---------- 4) Dataset -> ordered list[dict] ----------
	try:
	    pds = system.dataset.toPyDataSet(ds)
	except Exception, ex:
	    LOG.error("Dataset conversion failed: %r" % ex)
	    return {"json": [], "error": "Dataset conversion error: %s" % ex}
	
	rows = []
	rownum = 1
	
	for r in pds:
	    # Filter by area if specified
	    area_val = str(r["area"]).upper() if r["area"] else ""
	    if area and area_val != area:
	        continue
	
	    # Convert date types
	    df = r["date_from"]
	    dt = r["date_to"]
	
	    if JDate and isinstance(df, JDate):
	        df_str = OUT_DATE.format(df)
	    else:
	        df_str = df
	
	    if JDate and isinstance(dt, JDate):
	        dt_str = OUT_DATE.format(dt)
	    else:
	        dt_str = dt
	
	    # Build row with formatted numeric fields
	    row_obj = {
	        "rownum":       rownum,
	        "area":         area_val,
	        "currencyid":   r["currencyid"],
	        "hour":         r["hour"],  # new column if you want to use it later
	        "date_from":    df_str,
	        "date_to":      dt_str,
	
	        "forecast_price_section_import":    fmt_price(r["forecast_price_section_import"]),
	        "forecast_price_section_export":    fmt_price(r["forecast_price_section_export"]),
	        "forecast_quantity_section_import": fmt_quantity(r["forecast_quantity_section_import"]),
	        "forecast_quantity_section_export": fmt_quantity(r["forecast_quantity_section_export"]),
	    }
	
	    rows.append(row_obj)
	    rownum += 1
	
	LOG.info("listSections returning %d rows" % len(rows))
	return {"json": rows}