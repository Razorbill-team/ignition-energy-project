def doPost(request, session):
# WebDev → aggrid_subcontracts/save → doPost

    import json


    try:
        payload = json.loads(request["data"]) if "data" in request else request.json
    except:
        payload = json.loads(request.getBody())

    # AG-Grid usually sends {rows: [ {...}, {...} ]}
    rows = payload.get("rows") or []
    if not isinstance(rows, list):
        rows = [rows]

    if hasattr(session, "props") and hasattr(session.props, "user"):
        user = session.props.user.get("username", "system")
    else:
        user = "system"

    saved_ids = []

    for r in rows:
        params = {
            "p_subcontract_id"      : r.get("subcontract_id"),
            "p_contract_id"         : r.get("contract_id"),
            "p_slot_date"           : r.get("slot_date"),
            "p_slot_hour"           : r.get("slot_hour"),
            "p_datetime_from"       : r.get("datetime_from"),
            "p_datetime_to"         : r.get("datetime_to"),
            "p_quantity_kwh"        : r.get("quantity_kwh"),
            "p_price_mwh"           : r.get("price_mwh"),
            "p_price_eq_mdl"        : r.get("price_eq_mdl"),
            "p_contract_currencyid" : r.get("contract_currencyid"),
            "p_x_border_contract"   : r.get("x_border_contract"),
            "p_notes"               : r.get("notes"),
            "p_sign_date"           : r.get("sign_date"),
            "p_user"                : user
        }

        result = system.db.runNamedQuery("Subcontracts/SaveRow", params)
        # result[0][0] = subcontract_id returned
        if result and len(result) > 0:
            saved_ids.append(result[0][0])

    return {"json": {"ok": True, "saved_ids": saved_ids}}