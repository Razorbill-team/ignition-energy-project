SELECT
    contract_typeid            AS id,
    contracttype_description   AS name
FROM
    contract.contract_type
ORDER BY
    contract_typeid;

