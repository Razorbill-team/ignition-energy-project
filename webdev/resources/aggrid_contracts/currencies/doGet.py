def doGet(request, session):
    import system


    """
    Currencies for the 'Currency' and 'BCost CCY' dropdowns.
    Uses Named Query: Contract / Currencies_list
    Expected columns: currency_id, currency_code, currency_name
    Frontend uses:
      - id
      - code (EUR, RON, ...)
      - name
    """

    ds = system.db.runNamedQuery("Contract/Currencies_list", {})

    rows = []
    for r in ds:
        rows.append({
            "id":   int(r["currency_id"]),
            "code": str(r["currency_code"]),
            "name": str(r["currency_name"])
        })

    return {"json": {"ok": True, "rows": rows}}