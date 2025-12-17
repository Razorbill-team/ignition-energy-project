UPDATE contract.contragents_new
SET
    client_name = :client_name,
    idno        = :idno,
    country     = :country,
    open_date   = CAST(:open_date AS date),
    close_date  = CAST(:close_date AS date),
    address     = :address,
    admin_name  = :admin_name,
    admin_phone = :admin_phone,
    admin_email = :admin_email,

    contact_person_1_role_id = :contact_person_1_role_id,
    contact_person_1_name    = :contact_person_1_name,
    contact_person_1_phone   = :contact_person_1_phone,
    contact_person_1_email   = :contact_person_1_email,

    contact_person_2_role_id = :contact_person_2_role_id,
    contact_person_2_name    = :contact_person_2_name,
    contact_person_2_phone   = :contact_person_2_phone,
    contact_person_2_email   = :contact_person_2_email,

    contact_person_3_role_id = :contact_person_3_role_id,
    contact_person_3_name    = :contact_person_3_name,
    contact_person_3_phone   = :contact_person_3_phone,
    contact_person_3_email   = :contact_person_3_email,

    updated_at  = now(),
    updated_by  = 200,
    is_active   = COALESCE(:is_active, 1)

WHERE contragentid = :contragentid
RETURNING contragentid;
