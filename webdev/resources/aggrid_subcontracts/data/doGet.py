def doGet(request, session):
# WebDev → aggrid_subcontracts/data : doGet
# Returns ALL contracts, each with nested "subcontracts" list

    import system
    import json


    # --- call Named Query that returns ALL contracts --------------------
    # NOTE: adjust "Contract/SubcontractsMatrix" Named Query so it no longer
    #       requires p_contract_id and returns rows for all contracts.
    ds = system.db.runNamedQuery(
        "Contract/SubcontractsMatrix",   # <-- Named Query path
        {}                               # <-- no parameters (all contracts)
    )

    pds = system.dataset.toPyDataSet(ds)
    if len(pds) == 0:
        return {"json": {"ok": True, "rows": []}}

    col_names = list(ds.getColumnNames())

    # include contract_id + all columns that start with "contract_"
    contract_cols = [
        c for c in col_names
        if c == "contract_id" or c.startswith("contract_")
    ]
    # all subcontract_* columns
    subcontract_cols = [
        c for c in col_names
        if c.startswith("subcontract_")
    ]

    # --- group rows by contract_id --------------------------------------
    contracts_by_id = {}

    for r in pds:
        # get contract_id for grouping
        contract_id = r["contract_id"]

        # if this contract_id not yet created, build contract object
        if contract_id not in contracts_by_id:
            contract_obj = {}
            for c in contract_cols:
                v = r[c]
                # convert java.util.Date/Timestamp to string
                if hasattr(v, "isoformat"):
                    v = str(v)
                contract_obj[c] = v

            # nested subcontracts list
            contract_obj["subcontracts"] = []
            contracts_by_id[contract_id] = contract_obj

        # always append subcontract row (if there are subcontract_* columns)
        sub = {}
        for c in subcontract_cols:
            v = r[c]
            if hasattr(v, "isoformat"):
                v = str(v)
            sub[c] = v

        contracts_by_id[contract_id]["subcontracts"].append(sub)

    # --- final list of contracts ----------------------------------------
    rows = list(contracts_by_id.values())

    return {
        "json": {
            "ok": True,
            "rows": rows
        }
    }