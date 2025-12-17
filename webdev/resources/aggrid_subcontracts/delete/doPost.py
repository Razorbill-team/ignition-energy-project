def doPost(request, session):
# WebDev → aggrid_subcontracts/delete → doPost

    import json


    try:
        payload = json.loads(request["data"]) if "data" in request else request.json
    except:
        payload = json.loads(request.getBody())

    sid = payload.get("subcontract_id")
    if not sid:
        return {"json": {"ok": False, "error": "subcontract_id required"}}

    system.db.runNamedQuery(
        "Subcontracts/DeleteRow",
        {"p_subcontract_id": sid}
    )

    return {"json": {"ok": True}}