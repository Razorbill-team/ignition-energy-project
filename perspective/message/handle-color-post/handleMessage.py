def handleMessage(session, payload):
	system.perspective.sendMessage("handle-color-post-local", payload, scope="session")