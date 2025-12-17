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
    :contragentid,
    :dealno,
    :contract_typeid,
    :contract_currencyid,
    :price_mwh,
    :price_eq_mdl,
    :quantity_kwh,
    :x_border_costs,
    :x_border_cost_ccyid,
    :contragent_countryid,
    :date_from,
    :date_to,
    :sign_date,
    :datetime,
    :notes
)
RETURNING contract_id;
