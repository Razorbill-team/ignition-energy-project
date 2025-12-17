def doGet(request, session):

    # Return ALL rows for now; add WHERE/filters later if you want.
    sql = """
      SELECT
        contract_id, contract_typeid, contragentid, dealno,
        contract_currencyid, price_mwh, price_eq_mdl, quantity_kwh,
        x_border_costs, x_border_cost_ccyid,
        contragent_countryid,
        date_from, date_to, sign_date,notes, datetime,
        created_at, created_by, updated_at, updated_by
      FROM contract.contracts
      ORDER BY contract_id DESC
    """
    rows = system.db.runQuery(sql, "postgresDB")
    # build columns from dataset meta (Ignition returns PyDatasets with col names)
    columns = [c for c in rows.getColumnNames()]
    # turn into list[dict]
    out = []
    for r in rows:
        d = {}
        for c in columns:
            d[c] = r[c]
        out.append(d)
    return {"json": {"columns": columns, "rows": out}}