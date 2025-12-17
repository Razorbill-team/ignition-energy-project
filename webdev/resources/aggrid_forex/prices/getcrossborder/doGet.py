def doGet(request, session):
	# WebDev Scripted Resource: aggrid_market_prices/section/listSections
	# HTTP Method: doGet
	
	import system
	from java.util import Date as JavaDate
	
	log = system.util.getLogger("webdev.listSections")
	
	try:
	    # ---------- 1) Read filters from GET ----------
	    params_get = request.get("get", {})
	    area_str = (params_get.get("area") or "").strip().upper()   # RO / UA
	
	    # ---------- 2) HARDCODED SEPTEMBER ----------
	    date_from = system.date.parse("2025-09-01", "yyyy-MM-dd")
	    date_to   = system.date.parse("2025-09-30", "yyyy-MM-dd")
	
	    log.info("listSections DateFrom=%s DateTo=%s area=%s"
	             % (str(date_from), str(date_to), area_str))
	
	    # ---------- 3) Run Named Query ----------
	    ds = system.db.runNamedQuery(
	        "Reports/Cross_Border_Market",  # <-- your SQL with RO/UA UNION ALL
	        {
	            "DateFrom": date_from,
	            "DateTo":   date_to
	        }
	    )
	
	    # ---------- 4) Build rows ----------
	    rows = []
	
	    if ds is not None:
	        for row in ds:
	            area_val = str(row["area"]).upper()
	
	            # Optional filter:
	            if area_str and area_val != area_str:
	                continue
	
	            # Convert date types
	            df = row["date_from"]
	            dt = row["date_to"]
	
	            df_str = system.date.format(df, "yyyy-MM-dd") if isinstance(df, JavaDate) else df
	            dt_str = system.date.format(dt, "yyyy-MM-dd") if isinstance(dt, JavaDate) else dt
	
	            rows.append({
	                "area":                              area_val,
	                "currencyid":                        row["currencyid"],
	                "forecast_price_section_import":     row["forecast_price_section_import"],
	                "forecast_price_section_export":     row["forecast_price_section_export"],
	                "forecast_quantity_section_import":  row["forecast_quantity_section_import"],
	                "forecast_quantity_section_export":  row["forecast_quantity_section_export"],
	                "date_from":                         df_str,
	                "date_to":                           dt_str
	            })
	
	    log.info("listSections returned %d rows" % len(rows))
	
	    # ---------- 5) Return JSON ----------
	    return {"json": rows}
	
	except Exception, e:
	    log.error("Error in listSections: %s" % str(e), e)
	    return {"json": []}