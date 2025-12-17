def doPost(request, session):
	data = request.get("data", {})
	
	project = data.get("project")
	session = data.get("session")
	color = data.get("selectedColor")
	
	system.util.sendMessage(project, "handle-color-post", payload={"color": color}, scope="S", clientSessionId=session)
	
	return {"json": {"status": 201, "success": True}}