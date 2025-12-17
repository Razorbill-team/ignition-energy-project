def doPost(request, session):
    import json
    import system


    """
    Delete contract by ID.
    Front-end sends:
        body: JSON.stringify({ contract_id: id })
    WebDev sometimes gives string, sometimes already a dict in request["data"].
    """

    res = {"ok": False}

    try:
        # 1) Get payload from request["data"] or request.getBody()
        payload = {}

        if "data" in request:
            raw = request["data"]
            # If it's a JSON string
            if isinstance(raw, basestring):
                try:
                    payload = json.loads(raw)
                except:
                    payload = {}
            # If it's already a dict
            elif isinstance(raw, dict):
                payload = raw
        else:
            # Fallback: read raw body as JSON string
            try:
                body = request.getBody()
                if body:
                    payload = json.loads(body)
            except:
                payload = {}

        # 2) Extract contract_id
        cid = payload.get("contract_id")
        if not cid:
            res["error"] = "contract_id required"
            return {"json": res}

        contract_id = int(cid)

        # 3) Run Named Query (must be Update Query)
        system.db.runNamedQuery(
            "Contract/Contracts_delete",
            {"contract_id": contract_id}
        )

        # 4) Return success
        res["ok"] = True
        return {"json": res}

    except Exception, e:
        res["error"] = str(e)
        return {"json": res}