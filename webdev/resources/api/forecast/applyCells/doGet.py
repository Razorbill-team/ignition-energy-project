def doGet(request, session):

	return {
		"status": 200,
		"headers": {"Content-Type": "application/json"},
		"body": system.util.jsonEncode({"ok": True, "msg": "applyCells is reachable"})
	}