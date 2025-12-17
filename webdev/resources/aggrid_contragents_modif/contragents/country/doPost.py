def doPost(request, session):
	query = "SELECT country_name FROM contract.country ORDER BY country_name"
	rows = system.db.runQuery(query)
	
	# rows is a PyDataset; jsonEncode will turn it into a list of dicts
	return system.util.jsonEncode(rows)