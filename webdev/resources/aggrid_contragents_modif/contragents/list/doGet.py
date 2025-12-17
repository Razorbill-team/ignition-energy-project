def doGet(request, session):
	import system
	
	# Use your updated Named Query here
	ds = system.db.runNamedQuery("Contragent/contragent")
	
	rows = []
	for row in ds:
	    rows.append({
	        # basic info
	        "contragentid": row["contragentid"],
	        "client_name":  row["client_name"],
	        "idno":         row["idno"],
	        "country":      row["country"],
	        "open_date":    row["open_date"],
	        "close_date":   row["close_date"],
	
	        # status / address
	        "is_active":    row["is_active"],
	        "address":      row["address"],
	
	        # admin contact (and generic phone/email for grid)
	        "admin_name":   row["admin_name"],
	        "admin_phone":  row["admin_phone"],
	        "admin_email":  row["admin_email"],
	        "phone":        row["phone"],   # alias from SQL
	        "email":        row["email"],   # alias from SQL
	
	        # CONTACT PERSON 1
	        "contact_person_1_role_id":   row["contact_person_1_role_id"],
	        "contact_person_1_role_name": row["contact_person_1_role_name"],
	        "contact_person_1_name":      row["contact_person_1_name"],
	        "contact_person_1_phone":     row["contact_person_1_phone"],
	        "contact_person_1_email":     row["contact_person_1_email"],
	
	        # CONTACT PERSON 2
	        "contact_person_2_role_id":   row["contact_person_2_role_id"],
	        "contact_person_2_role_name": row["contact_person_2_role_name"],
	        "contact_person_2_name":      row["contact_person_2_name"],
	        "contact_person_2_phone":     row["contact_person_2_phone"],
	        "contact_person_2_email":     row["contact_person_2_email"],
	
	        # CONTACT PERSON 3
	        "contact_person_3_role_id":   row["contact_person_3_role_id"],
	        "contact_person_3_role_name": row["contact_person_3_role_name"],
	        "contact_person_3_name":      row["contact_person_3_name"],
	        "contact_person_3_phone":     row["contact_person_3_phone"],
	        "contact_person_3_email":     row["contact_person_3_email"],
	
	        # audit fields
	        "created_at":         row["created_at"],
	        "created_by_id_user": row["created_by_id_user"],   # note: lowercase, matches SQL
	        "created_by":         row["created_by"],
	        "created_role_name":  row["created_role_name"],
	        "updated_at":         row["updated_at"],
	        "updated_by_id_user": row["updated_by_id_user"],   # lowercase
	        "updated_by":         row["updated_by"],
	        "updated_role_name":  row["updated_role_name"],
	    })
	
	return {"json": rows}