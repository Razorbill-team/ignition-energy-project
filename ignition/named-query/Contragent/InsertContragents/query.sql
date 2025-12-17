INSERT INTO contract.contragents_new (
    client_name,
    idno,
    country,
    open_date,
    close_date,
    address,
 	 admin_name,
    admin_phone,
    admin_email,
	contact_person_1_role_id,
    contact_person_1_name,
    contact_person_1_phone,
    contact_person_1_email,
    contact_person_2_role_id,
    contact_person_2_name,
    contact_person_2_phone,
    contact_person_2_email,
    contact_person_3_role_id,
    contact_person_3_name,
    contact_person_3_phone,
    contact_person_3_email,
    created_at,
    created_by,
    updated_at,
    updated_by,
    is_active
)
VALUES (
    :client_name,
    :idno,
    :country,
    CAST(:open_date AS date),
    CAST(:close_date AS date),
    :address,
    :admin_name,
    :admin_phone,
    :admin_email,
    :contact_person_1_role_id,
    :contact_person_1_name,
    :contact_person_1_phone,
    :contact_person_1_email,
    :contact_person_2_role_id,
    :contact_person_2_name,
    :contact_person_2_phone,
    :contact_person_2_email,
    :contact_person_3_role_id,
    :contact_person_3_name,
    :contact_person_3_phone,
    :contact_person_3_email,
    now(),          -- created_at
    100,            -- created_by (your requirement)
    now(),          -- updated_at
    200,            -- updated_by (your requirement)
    COALESCE(:is_active, 1)
)
RETURNING contragentid;
