UPDATE contract.contracts
   SET contragent_id          = :contragent_id,
       dealno                 = :dealno,
       contract_code          = :contract_code,
       price_mwh              = :price_mwh,
       price_eq_mdl           = :price_eq_mdl,
       quantity_kwh           = :quantity_kwh,
       x_border_costs         = :x_border_costs,
       x_border_cost_ccyid    = :x_border_cost_ccyid,
       contragent_countryid   = :contragent_countryid,
       date_from              = :date_from,
       date_to                = :date_to,
       sign_date              = :sign_date,
       "datetime"             = COALESCE(:datetime, "datetime")
 WHERE contract_id = :contract_id;