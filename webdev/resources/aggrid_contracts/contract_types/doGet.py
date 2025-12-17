def doGet(request, session):
    import system


    result = {
        "ok": True,
        "rows": []
    }

    try:
        # Named Query: Contract / Contract_types_list
        ds = system.db.runNamedQuery("Contract/Contract_types_list", {})

        pds = system.dataset.toPyDataSet(ds)
        for row in pds:
            result["rows"].append({
                "id":   row["id"],    # contract_typeid
                "name": row["name"]   # contracttype_description (aliased as name)
            })

    except Exception, e:
        # Don't crash – report error in JSON
        result["ok"] = False
        result["error"] = str(e)

    # WebDev will serialize this dict as JSON
    return {"json": result}