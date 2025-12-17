def doGet(request, session):
	import system
	from java.util import Date as JavaDate
	
	# --- run Named Query ---
	ds = system.db.runNamedQuery("Contragent/contragent_roles")
	
	out = []
	if ds is not None:
	    for i in range(ds.rowCount):
	        rid  = ds.getValueAt(i, "contragent_user_role_id")
	        name = ds.getValueAt(i, "contragent_user_role_name")
	
	        # ensure not null
	        rid  = rid if rid else None
	        name = name if name else ""
	
	        # if name is a DATE (should never happen, but for consistency)
	        if isinstance(name, JavaDate):
	            name = system.date.format(name, "yyyy-MM-dd")
	
	        out.append({
	            "contragent_user_role_id":   rid,
	            "contragent_user_role_name": name
	        })
	
	return {"json": out}