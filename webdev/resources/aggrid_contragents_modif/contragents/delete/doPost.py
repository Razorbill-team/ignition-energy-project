def doPost(request, session):
	import system, traceback
	
	log = system.util.getLogger("contragents.delete")
	
	def ok(obj, code=200):
	    # Always return JSON to the browser
	    return {"status": code, "json": obj}
	
	try:
	    # ---------- 1) Read JSON from body ----------
	    raw = request.get("body") or request.get("data") or ""
	    log.info("delete.doPost - raw payload: %r (%s)" % (raw, type(raw)))
	
	    if isinstance(raw, (dict, list)):
	        data = raw
	    else:
	        raw_str = str(raw).strip()
	        if not raw_str:
	            return ok(
	                {"status": "error",
	                 "message": "Empty request body"},
	                400
	            )
	
	        try:
	            data = system.util.jsonDecode(raw_str)
	        except Exception as ex:
	            log.error("JSON decode failed in delete: %s | raw=%r" % (ex, raw_str))
	            return ok(
	                {"status": "error",
	                 "message": "Invalid JSON in request body"},
	                400
	            )
	
	    log.info("delete.doPost - parsed JSON: %r" % data)
	
	    # ---------- 2) Validate contragentid ----------
	    contragentid = data.get("contragentid", None)
	    if contragentid is None or str(contragentid).strip() == "":
	        return ok(
	            {"status": "error",
	             "message": "Field 'contragentid' is required."},
	            400
	        )
	
	    try:
	        contragentid = int(contragentid)
	    except Exception:
	        return ok(
	            {"status": "error",
	             "message": "Field 'contragentid' must be numeric."},
	            400
	        )
	
	    params = {"contragentid": contragentid}
	    log.info("delete.doPost - calling Contragent/delete_contragent with %r" % params)
	
	    # ---------- 3) Run Named Query ----------
	    system.db.runNamedQuery("Contragent/delete_contragent", params)
	
	    log.info("delete.doPost - delete OK for ID=%s" % contragentid)
	
	    # ---------- 4) Return success ----------
	    return ok({"status": "ok", "id": contragentid}, 200)
	
	except Exception as ex:
	    trace = traceback.format_exc()
	    log.error("delete.doPost crashed: %s" % ex)
	    log.error(trace)
	    return ok(
	        {"status": "error",
	         "message": str(ex)},
	        500
	    )