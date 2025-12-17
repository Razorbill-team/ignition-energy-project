def doPost(request, session):
	import system, traceback
	
	log = system.util.getLogger("contragents.update")
	
	def ok(obj, code=200):
	    return {"status": code, "json": obj}
	
	def to_int_or_none(v):
	    try:
	        if v in (None, "", "null"):
	            return None
	        return int(v)
	    except:
	        return None
	
	try:
	    # ---------- 1) Read JSON ----------
	    raw = request.get("body") or request.get("data") or ""
	    log.info("update.doPost raw: %r (%s)" % (raw, type(raw)))
	
	    if isinstance(raw, (dict, list)):
	        data = raw
	    else:
	        raw_str = str(raw).strip()
	        if not raw_str:
	            return ok({"status": "error", "message": "Empty request body"}, 400)
	        data = system.util.jsonDecode(raw_str)
	
	    log.info("update parsed JSON: %r" % data)
	
	    # ---------- 2) Required ----------
	    contragentid = to_int_or_none(data.get("contragentid"))
	    if not contragentid:
	        return ok({"status": "error", "message": "Missing contragentid"}, 400)
	
	    client_name = (data.get("client_name") or "").strip()
	    idno        = (data.get("idno") or "").strip()
	    open_date   = (data.get("open_date") or "").strip()
	    country     = (data.get("country") or "").strip()
	
	    if not client_name or not idno or not open_date or not country:
	        return ok({
	            "status": "error",
	            "message": "client_name, idno, open_date and country are required"
	        }, 400)
	
	    # ---------- 3) Optional ----------
	    close_date_raw = (data.get("close_date") or "").strip()
	    close_date = close_date_raw if close_date_raw else None
	
	    address     = data.get("address") or None
	    admin_name  = data.get("admin_name") or None
	    admin_phone = data.get("admin_phone") or None
	    admin_email = data.get("admin_email") or None
	
	    # ---------- Contacts ----------
	    params = {
	        "contragentid": contragentid,
	
	        "client_name": client_name,
	        "idno":        idno,
	        "country":     country,
	        "open_date":   open_date,
	        "close_date":  close_date,
	        "address":     address,
	
	        "admin_name":  admin_name,
	        "admin_phone": admin_phone,
	        "admin_email": admin_email,
	
	        "contact_person_1_role_id": to_int_or_none(data.get("contact_person_1_role_id")),
	        "contact_person_1_name":    data.get("contact_person_1_name")  or None,
	        "contact_person_1_phone":   data.get("contact_person_1_phone") or None,
	        "contact_person_1_email":   data.get("contact_person_1_email") or None,
	
	        "contact_person_2_role_id": to_int_or_none(data.get("contact_person_2_role_id")),
	        "contact_person_2_name":    data.get("contact_person_2_name")  or None,
	        "contact_person_2_phone":   data.get("contact_person_2_phone") or None,
	        "contact_person_2_email":   data.get("contact_person_2_email") or None,
	
	        "contact_person_3_role_id": to_int_or_none(data.get("contact_person_3_role_id")),
	        "contact_person_3_name":    data.get("contact_person_3_name")  or None,
	        "contact_person_3_phone":   data.get("contact_person_3_phone") or None,
	        "contact_person_3_email":   data.get("contact_person_3_email") or None,
	    }
	
	    log.info("update.doPost params: %r" % params)
	
	    # ---------- 4) Execute ----------
	    system.db.runNamedQuery("Contragent/update_contragent", params)
	
	    log.info("update.doPost OK for contragentid=%s" % contragentid)
	    return ok({"status": "ok", "id": contragentid}, 200)
	
	except Exception as ex:
	    trace = traceback.format_exc()
	    log.error("update.doPost crashed: %s" % ex)
	    log.error(trace)
	    return ok({"status": "error", "message": str(ex)}, 500)