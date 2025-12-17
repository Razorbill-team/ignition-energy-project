def doGet(request, session):
	    import system
	
	    """
	    Counterparties for the 'Counterparty' dropdown.
	    Uses Named Query: Contract / Counterparties_list
	    Expected columns: id, client_name
	    """
	
	    result = {
	        "ok": True,
	        "rows": []
	    }
	
	    try:
	        ds = system.db.runNamedQuery("Contract/Counterparties_list", {})
	        pds = system.dataset.toPyDataSet(ds)
	
	        for row in pds:
	            result["rows"].append({
	                "id":   row["id"],          # contragentid
	                "name": row["client_name"]  # display name
	            })
	
	    except Exception, e:
	        result["ok"] = False
	        result["error"] = str(e)
	
	    return {"json": result}