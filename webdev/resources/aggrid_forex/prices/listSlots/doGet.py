def doGet(request, session):
	# WebDev Scripted Resource: Forex/ForeCastForex/listSlots
	# HTTP Method: GET -> doGet(request)
	
	import system
	from java.text import SimpleDateFormat
	from java.util import TimeZone, Date as JDate
	
	log = system.util.getLogger("webdev.forex.listSlots")
	
	try:
	    # ---------- 1) Read filters from GET ----------
	    p = request.get("params", {}) or request.get("get", {}) or {}
	
	    from_in = (p.get("from") or "").strip()
	    to_in   = (p.get("to")   or "").strip()
	    ccy_in  = (p.get("ccy")  or "").strip().upper()   # EUR / USD / ...
	
	    # ---------- 2) Default / normalize dates ----------
	    tz       = TimeZone.getTimeZone("Europe/Chisinau")
	    out_fmt  = SimpleDateFormat("yyyy-MM-dd")
	    out_fmt.setTimeZone(tz)
	
	    now = system.date.now()
	
	    if from_in:
	        date_from = from_in
	    else:
	        d_from = system.date.addDays(now, -1)
	        date_from = out_fmt.format(d_from)
	
	    if to_in:
	        date_to = to_in
	    else:
	        d_to = system.date.addDays(now, 1)
	        date_to = out_fmt.format(d_to)
	
	    log.info("listSlots DateFrom=%s DateTo=%s Ccy=%s"
	             % (date_from, date_to, ccy_in or "ALL"))
	
	    # ---------- 3) Run Named Query ----------
	    # Named Query path: Forex/ForeCastForex
	    nq_params = {
	        "DateFrom": date_from,
	        "DateTo":   date_to,
	        "Currency": ccy_in or ""     # matches :Currency parameter in your SQL
	    }
	
	    ds = system.db.runNamedQuery("Forex/ForeCastForex", nq_params)
	
	    # ---------- 4) Build rows ----------
	    rows = []
	    rownum = 1
	
	    if ds is not None:
	        pds = system.dataset.toPyDataSet(ds)
	
	        for r in pds:
	            d = r["day_date"]
	
	            if isinstance(d, JDate):
	                day_str = out_fmt.format(d)
	            else:
	                day_str = d
	
	            rows.append({
	                "rownum":       rownum,
	                "day_date":     day_str,
	                "currency_id":  r["currency_id"],
	                "exchange_rate": r["exchange_rate"],
	                "eq_value":      r["eq_value"]
	            })
	
	            rownum += 1
	
	    log.info("listSlots returned %d rows" % len(rows))
	
	    # ---------- 5) Return JSON ----------
	    return {"json": rows}
	
	except Exception, e:
	    log.error("Error in forex listSlots: %s" % str(e), e)
	    return {"json": []}