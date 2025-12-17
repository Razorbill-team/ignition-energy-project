SELECT
    subcontract_id,
    contract_id,
    slot_date,
    slot_hour,
    datetime_from,
    datetime_to,
    quantity_kwh,
    price_mwh,
    price_eq_mdl,
    contract_currencyid,
    x_border_costs,
    created_at,
    created_by,
    updated_at,
    updated_by,
    notes,
    sign_date,
    datetime
FROM contract.subcontracts
WHERE contract_id = :p_contract_id
ORDER BY slot_date, slot_hour;
