def doGet(request, session):
	# WebDev Scripted Resource: aggrid_market_prices/prices/listSlots
	# HTTP Method: GET -> doGet(request)
	
	import system
	from java.text import SimpleDateFormat
	from java.util import TimeZone
	try:
	    from java.util import Date as JDate
	except:
	    JDate = None
	
	LOG = system.util.getLogger("WebDev.MarketPrices.listSlots")
	
	def fmt_price(v):
	    if v is None:
	        return ""
	    try:
	        return str(int(round(float(str(v).replace(",", ".")))))
	    except:
	        return str(v)
	
	def fmt_fx(v):
	    if v is None:
	        return ""
	    try:
	        return "%.2f" % float(str(v).replace(",", "."))
	    except:
	        return str(v)
	
	def fmt_dt(v):
	    if v is None:
	        return ""
	    if JDate and isinstance(v, JDate):
	        return OUT_DATE.format(v)
	    return str(v)
	
	def fmt_ts(v):
	    if v is None:
	        return ""
	    try:
	        if JDate and isinstance(v, JDate):
	            sdf = SimpleDateFormat("dd.MM.yyyy HH:mm:ss")
	            sdf.setTimeZone(TZ)
	            return sdf.format(v)
	        return str(v)
	    except:
	        return str(v)
	
	# ---------- 1) Read params ----------
	p = request.get("params", {}) or request.get("get", {}) or {}
	
	from_in   = (p.get("from")     or "").strip()
	to_in     = (p.get("to")       or "").strip()
	market_in = (p.get("market")   or "").strip()
	ccy_in    = (p.get("currency") or "").strip()
	hour_in   = (p.get("hour")     or "").strip()
	
	# Market normalization
	if not market_in:
	    market = None
	else:
	    market = market_in.upper()
	    if market in ("ALL", "ALL MARKETS"):
	        market = None
	
	# Currency normalization
	currency = ccy_in.strip()
	if not currency or currency.upper() in ("ALL", "ALL CCY", "ALL CURRENCIES"):
	    currency = None
	
	# Hour normalization
	hour = None
	if hour_in:
	    try:
	        hour = int(hour_in)
	    except Exception, ex:
	        LOG.warn("Invalid hour param %r: %r" % (hour_in, ex))
	        hour = None
	
	# ---------- 2) Default dates ----------
	TZ       = TimeZone.getTimeZone("Europe/Chisinau")
	OUT_DATE = SimpleDateFormat("yyyy-MM-dd")
	OUT_DATE.setTimeZone(TZ)
	
	now = system.date.now()
	
	if from_in:
	    date_from = from_in
	else:
	    date_from = OUT_DATE.format(system.date.addDays(now, -1))
	
	if to_in:
	    date_to = to_in
	else:
	    date_to = OUT_DATE.format(system.date.addDays(now, 1))
	
	
	# ---------- 3) Run Named Query ----------
	params = {
	    "DateFrom": date_from,
	    "DateTo":   date_to,
	    "Market":   market,
	    "Currency": currency,
	    "Hour":     hour
	}
	
	try:
	    ds = system.db.runNamedQuery("Market/market_prices", params)
	except Exception, ex:
	    LOG.error("NamedQuery failed: %r" % ex)
	    return {"json": [], "error": str(ex)}
	
	
	# ---------- 4) Convert dataset ----------
	try:
	    pds = system.dataset.toPyDataSet(ds)
	except Exception, ex:
	    LOG.error("Dataset conversion failed: %r" % ex)
	    return {"json": [], "error": str(ex)}
	
	rows = []
	rownum = 1
	
	for r in pds:
	
	    # format main date
	    data_val = r["data"]
	    if JDate and isinstance(data_val, JDate):
	        data_str = OUT_DATE.format(data_val)
	    else:
	        data_str = data_val
	
	    row_obj = {
	        "rownum": rownum,
	
	        # existing fields
	        "data": data_str,
	        "hour_slot": int(r["hour_slot"]) if r["hour_slot"] is not None else "",
	        "market": r["market"],
	        "currencyid": r["currencyid"],
	        "forecast_price_closed": fmt_price(r["forecast_price_closed"]),
	        "CURRENCY_FX_EQ_MDL": fmt_fx(r["CURRENCY_FX_EQ_MDL"]),
	        "forecast_price_closed_eq": fmt_price(r["forecast_price_closed_eq"]),
	
	        # NEW fields (formatted)
	        "created_at": fmt_ts(r["created_at"]),
	        "created_by_userid": r["created_by_userid"],
	        "create_user_name": r["create_user_name"],
	
	        "updated_at": fmt_ts(r["updated_at"]),
	        "updated_by_userid": r["updated_by_userid"],
	        "updated_user_name": r["updated_user_name"],
	
	        "date_from": fmt_dt(r["date_from"]),
	        "date_to": fmt_dt(r["date_to"]),
	    }
	
	    rows.append(row_obj)
	    rownum += 1
	
	LOG.info("listSlots returning %d rows" % len(rows))
	return {"json": rows}