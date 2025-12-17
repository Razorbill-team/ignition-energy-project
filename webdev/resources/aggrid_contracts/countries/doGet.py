def doGet(request, session):
    import system


    """
    Countries for the 'Country' dropdown.
    Uses Named Query: Contract / Countries_list
    Expected columns: country_id, country_code3, country_name
    Frontend uses:
      - id   (we won't use it now, but good to have)
      - code (MDA, HUN, etc)  -> goes into contracts.contragent_countryid
      - name
    """

    ds = system.db.runNamedQuery("Contract/Countries_list", {})

    rows = []
    for r in ds:
        rows.append({
            "id":   int(r["country_id"]),
            "code": str(r["country_code3"]),
            "name": str(r["country_name"])
        })

    return {"json": {"ok": True, "rows": rows}}