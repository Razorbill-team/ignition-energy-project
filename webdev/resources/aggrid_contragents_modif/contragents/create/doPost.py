def doPost(request, session):
	import system, traceback
	
	log = system.util.getLogger("contragents.create")
	
	def ok(obj, code=200):
	    return {"status": code, "json": obj}
	
	def to_int_or_none(v):
	    if v is None:
	        return None
	    s = unicode(v).strip()
	    if not s:
	        return None
	    try:
	        return int(s)
	    except:
	        return None
	
	try:
	    # ---------- 1) Read JSON payload ----------
	    raw = request.get("body") or request.get("data") or ""
	    log.info("create.doPost - raw payload: %r (%s)" % (raw, type(raw)))
	
	    if isinstance(raw, (dict, list)):
	        data = raw
	    else:
	        raw_str = str(raw).strip()
	        if not raw_str:
	            return ok({"status": "error",
	                       "message": "Empty request body"}, 400)
	        try:
	            data = system.util.jsonDecode(raw_str)
	        except Exception as ex:
	            log.error("JSON decode failed in create: %s | raw=%r" % (ex, raw_str))
	            return ok({"status": "error",
	                       "message": "Invalid JSON in request body"}, 400)
	
	    log.info("create.doPost - parsed JSON: %r" % data)
	
	    # ---------- 2) Required fields ----------
	    client_name = (data.get("client_name") or "").strip()
	    idno        = (data.get("idno") or "").strip()
	    open_date   = (data.get("open_date") or "").strip()   # "YYYY-MM-DD"
	
	    if not client_name or not idno or not open_date:
	        return ok({
	            "status": "error",
	            "message": "client_name, idno and open_date are required."
	        }, 400)
	
	    # ---------- 3) Optional basic fields ----------
	    close_date   = (data.get("close_date") or "").strip() or None
	    address      = (data.get("address") or "").strip() or None
	    admin_name   = (data.get("admin_name") or "").strip() or None
	    admin_phone  = (data.get("admin_phone") or "").strip() or None
	    admin_email  = (data.get("admin_email") or "").strip() or None
	    country      = (data.get("country") or "").strip() or None
	
	    # ---------- 4) Contacts ----------
	    cp1_role_id  = to_int_or_none(data.get("contact_person_1_role_id"))
	    cp1_name     = (data.get("contact_person_1_name")  or "").strip() or None
	    cp1_phone    = (data.get("contact_person_1_phone") or "").strip() or None
	    cp1_email    = (data.get("contact_person_1_email") or "").strip() or None
	
	    cp2_role_id  = to_int_or_none(data.get("contact_person_2_role_id"))
	    cp2_name     = (data.get("contact_person_2_name")  or "").strip() or None
	    cp2_phone    = (data.get("contact_person_2_phone") or "").strip() or None
	    cp2_email    = (data.get("contact_person_2_email") or "").strip() or None
	
	    cp3_role_id  = to_int_or_none(data.get("contact_person_3_role_id"))
	    cp3_name     = (data.get("contact_person_3_name")  or "").strip() or None
	    cp3_phone    = (data.get("contact_person_3_phone") or "").strip() or None
	    cp3_email    = (data.get("contact_person_3_email") or "").strip() or None
	
	    # optional is_active flag from UI (default = 1)
	    is_active = data.get("is_active")
	    try:
	        if is_active is not None:
	            is_active = int(is_active)
	    except:
	        is_active = 1
	
	    # ---------- 5) Named query params (MATCH your INSERT) ----------
	    params = {
	        "client_name":  client_name,
	        "idno":         idno,
	        "country":      country,
	        "open_date":    open_date,
	        "close_date":   close_date,
	        "address":      address,
	        "admin_name":   admin_name,
	        "admin_phone":  admin_phone,
	        "admin_email":  admin_email,
	
	        "contact_person_1_role_id": cp1_role_id,
	        "contact_person_1_name":    cp1_name,
	        "contact_person_1_phone":   cp1_phone,
	        "contact_person_1_email":   cp1_email,
	
	        "contact_person_2_role_id": cp2_role_id,
	        "contact_person_2_name":    cp2_name,
	        "contact_person_2_phone":   cp2_phone,
	        "contact_person_2_email":   cp2_email,
	
	        "contact_person_3_role_id": cp3_role_id,
	        "contact_person_3_name":    cp3_name,
	        "contact_person_3_phone":   cp3_phone,
	        "contact_person_3_email":   cp3_email,
	
	        "is_active": is_active
	    }
	
	    log.info("create.doPost - InsertContragents params: %r" % params)
	
	    ds = system.db.runNamedQuery("Contragent/InsertContragents", params)
	
	    new_id = None
	    if ds is not None and ds.getRowCount() > 0:
	        new_id = ds.getValueAt(0, 0)
	
	    log.info("create.doPost - insert OK, new_id=%r" % new_id)
	
	    return ok({"status": "ok", "id": new_id}, 200)
	
	except Exception as ex:
	    trace = traceback.format_exc()
	    log.error("create.doPost crashed: %s" % ex)
	    log.error(trace)
	    return ok({"status": "error", "message": str(ex)}, 500)