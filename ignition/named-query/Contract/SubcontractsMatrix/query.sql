SELECT
    -- CONTRACT side (for column group "contract")
    c.contract_id                           AS contract_id,
    c.contragentid                          AS contract_contragentid,
    c.dealno                                AS contract_dealno,
    c.contract_currencyid                   AS contract_currencyid,
    c.contragent_countryid                  AS contract_country,
    c.date_from                             AS contract_date_from,
    c.date_to                               AS contract_date_to,
    c.sign_date                             AS contract_sign_date,
    c.created_at                            AS contract_created_at,
    c.created_by                            AS contract_created_by,
    c.updated_at                            AS contract_updated_at,
    c.updated_by                            AS contract_updated_by,
    c.notes                                 AS contract_notes,

    -- SUBCONTRACT side (for column group "subcontract")
    s.subcontract_id                        AS subcontract_id,
    s.contragentid                          AS subcontract_contragentid,
    s.dealno                                AS subcontract_dealno,
    s.subcontract_currencyid                AS subcontract_currencyid,
    s.slot_date                             AS subcontract_slot_date,
    s.slot_hour                             AS subcontract_slot_hour,
    s.datetime_from                         AS subcontract_datetime_from,
    s.datetime_to                           AS subcontract_datetime_to,
    s.price_type                            AS subcontract_price_type,
    s.price_mwh                             AS subcontract_price_mwh,
    s.quantity_type                         AS subcontract_quantity_type,
    s.quantity_kwh                          AS subcontract_quantity_kwh,
    s.index_type                            AS subcontract_index_type,
    s.index_currency                        AS subcontract_index_currency,
    s.margin                                AS subcontract_margin,
    s.margin_currency                       AS subcontract_margin_currency,
    s.border_costs                          AS subcontract_border_costs,
    s.transport_costs                       AS subcontract_transport_costs,
    s.import_costs                          AS subcontract_import_costs,
    s.export_costs                          AS subcontract_export_costs,
    s.created_at                            AS subcontract_created_at,
    s.created_by                            AS subcontract_created_by,
    s.updated_at                            AS subcontract_updated_at,
    s.updated_by                            AS subcontract_updated_by,
    s.notes                                 AS subcontract_notes,
    s.sign_date                             AS subcontract_sign_date

FROM contract.contracts_new c
LEFT JOIN contract.subcontracts_new s
       ON s.contract_id = c.contract_id
          and s.contragentid =c.contragentid  



ORDER BY
    c.contract_id,
    s.slot_date,
    s.slot_hour,
    s.subcontract_id;
