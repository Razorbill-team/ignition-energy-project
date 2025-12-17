def doPost(request, session):
	import system, json, traceback
	
	log = system.util.getLogger("market.saveSlot.v3")
	DATASOURCE = "PostgresDB"
	
	
	def ok(obj, code=200):
	    return {"status": code, "json": obj}
	
	
	def _to_float(v):
	    if v is None:
	        return None
	    s = unicode(v).replace(",", ".").strip()
	    if not s:
	        return None
	    try:
	        return float(s)
	    except:
	        return None
	
	
	try:
	    # ------------------- 1) Read JSON -------------------
	    raw = request.get("body") or request.get("data") or ""
	    if isinstance(raw, dict):
	        payload = raw
	    else:
	        payload = system.util.jsonDecode(str(raw))
	
	    log.info("saveSlot.v3 payload: %r" % payload)
	
	    date_from  = payload.get("date_from") or payload.get("DateFrom")
	    date_to    = payload.get("date_to")   or payload.get("DateTo")
	    market     = payload.get("market")    or payload.get("Market")
	    currencyid = payload.get("currencyid") or payload.get("Currency")
	    prices     = payload.get("prices") or {}
	
	    # ------------------- 2) Validate ---------------------
	    if not date_from or not market or not currencyid:
	        return ok({"ok": False, "error": "Missing date_from, market or currencyid"}, 400)
	
	    m = unicode(market).strip().upper()
	
	    # ------------------- 3) Choose table -----------------
	    if m == "OPCOM":
	        table_name = "forecast.forecast_p_q_opcom"
	    elif m == "OPEM":
	        table_name = "forecast.forecast_p_q_opem"
	    elif m == "RDN":
	        table_name = "forecast.forecast_p_q_rdn"
	    else:
	        return ok({"ok": False, "error": "Unknown market"}, 400)
	
	    # ------------------- 4) Build SQL --------------------
	    sql_delete = """
	        DELETE FROM %s
	         WHERE data = CAST(? AS DATE)
	           AND currencyid = ?
	    """ % table_name
	
	    sql_insert = """
	        INSERT INTO %s (
	            data,
	            interval_hour,
	            interval_minutes,
	            forecast_price_closed,
	            currencyid
	        )
	        VALUES (CAST(? AS DATE), ?, 0, ?, ?)
	    """ % table_name
	
	    # ------------------- 5) Run transaction --------------
	    tx = system.db.beginTransaction(DATASOURCE)
	
	    try:
	        # delete old rows for that date+ccy
	        system.db.runPrepUpdate(sql_delete, [date_from, int(currencyid)], tx=tx)
	
	        inserted = 0
	
	        # loop 24 hours
	        for hour_str, price_str in prices.items():
	            try:
	                hour = int(hour_str)
	            except:
	                continue  # ignore invalid keys
	
	            price_val = _to_float(price_str)
	            if price_val is None:
	                continue  # skip empty cells
	
	            args = [
	                date_from,
	                hour,
	                price_val,
	                int(currencyid)
	            ]
	
	            system.db.runPrepUpdate(sql_insert, args, tx=tx)
	            inserted += 1
	
	        system.db.commitTransaction(tx)
	        system.db.closeTransaction(tx)
	
	    except:
	        system.db.rollbackTransaction(tx)
	        system.db.closeTransaction(tx)
	        raise
	
	    return ok({
	        "ok": True,
	        "inserted": inserted,
	        "date_from": date_from,
	        "market": m,
	        "currencyid": currencyid,
	        "table": table_name
	    }, 200)
	
	except Exception as ex:
	    traceback_str = traceback.format_exc()
	    log.error("saveSlot.v3 crashed: %s" % ex)
	    log.error(traceback_str)
	    return ok({"ok": False, "error": str(ex)}, 500)