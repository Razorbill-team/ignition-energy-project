SELECT
    ag.contragentid,
    ag.client_name,
    ag.idno,
    ag.country,
    to_char(ag.open_date,  'YYYY-MM-DD') AS open_date,
    to_char(ag.close_date, 'YYYY-MM-DD') AS close_date,

    ag.is_active,
    ag.address,

    -- admin contact (and aliases for grid)
    ag.admin_name,
    ag.admin_phone,
    ag.admin_email,
    ag.admin_phone AS phone,   -- optional: keep old column name
    ag.admin_email AS email,   -- optional: keep old column name

    -- CONTACT PERSON 1
    ag.contact_person_1_role_id,
    cr1.contragent_user_role_name AS contact_person_1_role_name,
    ag.contact_person_1_name,
    ag.contact_person_1_phone,
    ag.contact_person_1_email,

    -- CONTACT PERSON 2
    ag.contact_person_2_role_id,
    cr2.contragent_user_role_name AS contact_person_2_role_name,
    ag.contact_person_2_name,
    ag.contact_person_2_phone,
    ag.contact_person_2_email,

    -- CONTACT PERSON 3
    ag.contact_person_3_role_id,
    cr3.contragent_user_role_name AS contact_person_3_role_name,
    ag.contact_person_3_name,
    ag.contact_person_3_phone,
    ag.contact_person_3_email,

    ag.created_at,
    ag.created_by  AS created_by_id_user,
    us_created.display_name   AS created_by,
    us_created.user_role_name AS created_role_name,
    ag.updated_at,
    ag.updated_by  AS updated_by_id_user,
    us_updated.display_name   AS updated_by,
    us_updated.user_role_name AS updated_role_name

FROM contract.contragents_new ag
LEFT JOIN user_schema.user_names us_created
       ON ag.created_by = us_created.id
LEFT JOIN user_schema.user_names us_updated
       ON ag.updated_by = us_updated.id

LEFT JOIN contract.contragent_roles cr1
       ON cr1.contragent_user_role_id = ag.contact_person_1_role_id
LEFT JOIN contract.contragent_roles cr2
       ON cr2.contragent_user_role_id = ag.contact_person_2_role_id
LEFT JOIN contract.contragent_roles cr3
       ON cr3.contragent_user_role_id = ag.contact_person_3_role_id

ORDER BY ag.contragentid;
