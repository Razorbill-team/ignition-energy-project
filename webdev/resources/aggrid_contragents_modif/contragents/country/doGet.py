def doGet(request, session):
	import system
	from java.util import Date as JavaDate
	
	# --- run your Named Query ---
	ds = system.db.runNamedQuery("Nomenclator/Country")  # <-- EXACT name of your named query
	
	out = []
	if ds is not None:
	    for i in range(ds.rowCount):
	        code = ds.getValueAt(i, "country_code3")
	        name = ds.getValueAt(i, "country_name")
	        cid  = ds.getValueAt(i, "country_id")
	
	        # ensure not null
	        code = code if code else ""
	        name = name if name else ""
	        cid  = cid if cid  else None
	
	        # if name is DATE (rare case)
	        if isinstance(name, JavaDate):
	            name = system.date.format(name, "yyyy-MM-dd")
	
	        out.append({
	            "country_id":    cid,
	            "country_code3": code,
	            "country_name":  name
	        })
	
	return {"json": out}