def doPost(request, session):
    import system
    import json

    logger = system.util.getLogger("aggrid_contracts.save")

    try:
        # ---------- read body ----------
        raw = request.get("postData") or request.get("data") or ""
        if isinstance(raw, dict):
            payload = raw
        else:
            payload = json.loads(raw) if raw else {}

        def g(k):
            v = payload.get(k)
            return None if v in ("", None, u"", "") else v

        def gi(k):
            """int helper"""
            v = g(k)
            try:
                return int(v) if v is not None else None
            except:
                return None

        def gn(k, default=None):
            """numeric (float) helper, with default (for NOT NULL numeric columns)"""
            v = g(k)
            if v is None:
                return default
            try:
                return float(v)
            except:
                return default

        # ---------- collect params ----------
        params = {
            "contract_id":           gi("contract_id"),          # bigint PK
            "contragentid":          gi("contragentid"),         # bigint
            "dealno":                payload.get("dealno") or "",# NOT NULL
            "contract_typeid":       gi("contract_typeid"),
            "contract_currencyid":   gi("contract_currencyid"),
            "price_mwh":             gn("price_mwh", 0),         # numeric, default 0
            "price_eq_mdl":          gn("price_eq_mdl", 0),      # numeric, default 0
            "quantity_kwh":          gn("quantity_kwh", 0),      # numeric, default 0
            "x_border_costs":        gn("x_border_costs", 0),    # << important: default 0
            "x_border_cost_ccyid":   gi("x_border_cost_ccyid"),
            "contragent_countryid":  g("contragent_countryid"),
            "date_from":             g("date_from"),
            "date_to":               g("date_to"),
            "sign_date":             g("sign_date"),
            "datetime":              g("datetime"),
            "notes":                 g("notes"),
        }

        # simple server-side validation for required fields
        missing = []
        if not params["dealno"]:
            missing.append("dealno (contract code)")
        if params["contragentid"] is None:
            missing.append("contragentid")
        if params["contract_typeid"] is None:
            missing.append("contract_typeid")
        if params["contract_currencyid"] is None:
            missing.append("contract_currencyid")
        if params["date_from"] is None:
            missing.append("date_from")
        if params["date_to"] is None:
            missing.append("date_to")
        if params["sign_date"] is None:
            missing.append("sign_date")

        if missing:
            msg = "Missing required fields: " + ", ".join(missing)
            logger.warn("Validation failed: %s | payload=%s" % (msg, payload))
            return {"json": {"ok": False, "error": msg}}

        # ---------- INSERT ----------
        if params["contract_id"] is None:
            insert_sql = """
                INSERT INTO contract.contracts (
                    contragentid,
                    dealno,
                    contract_typeid,
                    contract_currencyid,
                    price_mwh,
                    price_eq_mdl,
                    quantity_kwh,
                    x_border_costs,
                    x_border_cost_ccyid,
                    contragent_countryid,
                    date_from,
                    date_to,
                    sign_date,
                    datetime,
                    notes
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?::date, ?::date, ?::date, ?::timestamp, ?
                )
                RETURNING contract_id
            """

            insert_args = [
                params["contragentid"],
                params["dealno"],
                params["contract_typeid"],
                params["contract_currencyid"],
                params["price_mwh"],
                params["price_eq_mdl"],
                params["quantity_kwh"],
                params["x_border_costs"],        # now 0 if empty
                params["x_border_cost_ccyid"],
                params["contragent_countryid"],
                params["date_from"],
                params["date_to"],
                params["sign_date"],
                params["datetime"],
                params["notes"],
            ]

            ds = system.db.runPrepQuery(insert_sql, insert_args, "postgresDB")

            new_id = None
            if ds is not None and ds.getRowCount() > 0:
                try:
                    new_id = ds.getValueAt(0, "contract_id")
                except:
                    new_id = ds.getValueAt(0, 0)

            return {"json": {"ok": True, "mode": "insert", "contract_id": new_id}}

        # ---------- UPDATE ----------
        update_sql = """
            UPDATE contract.contracts
            SET contragentid          = ?,
                dealno                = ?,
                contract_typeid       = ?,
                contract_currencyid   = ?,
                price_mwh             = ?,
                price_eq_mdl          = ?,
                quantity_kwh          = ?,
                x_border_costs        = ?,
                x_border_cost_ccyid   = ?,
                contragent_countryid  = ?,
                date_from             = ?::date,
                date_to               = ?::date,
                sign_date             = ?::date,
                datetime              = ?::timestamp,
                notes                 = ?,
                updated_at            = now()
            WHERE contract_id = ?
        """

        update_args = [
            params["contragentid"],
            params["dealno"],
            params["contract_typeid"],
            params["contract_currencyid"],
            params["price_mwh"],
            params["price_eq_mdl"],
            params["quantity_kwh"],
            params["x_border_costs"],          # 0 if empty
            params["x_border_cost_ccyid"],
            params["contragent_countryid"],
            params["date_from"],
            params["date_to"],
            params["sign_date"],
            params["datetime"],
            params["notes"],
            params["contract_id"],
        ]

        system.db.runPrepUpdate(update_sql, update_args, "postgresDB")

        return {"json": {"ok": True, "mode": "update", "contract_id": params["contract_id"]}}

    except Exception, e:
        # catch absolutely everything and ALWAYS return JSON
        logger.error("UNHANDLED save error: %s" % e)
        return {"json": {"ok": False, "error": str(e)}}