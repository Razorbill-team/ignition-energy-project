def doGet(request, session):
    from java.text import SimpleDateFormat
    from java.util import TimeZone
    url = "/system/webdev/LAST_PROJECT_VERSION_D1_12-August_0823_2025-08-12_0835/test_calendar/events?farms=" + ",".join(session.custom.list_of_farms)
    system.net.httpGet(url)
    """
    def toISO8601(date):
        if date is None:
            return None
        sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
        sdf.setTimeZone(TimeZone.getTimeZone("UTC"))
        return sdf.format(date)"""
        
    # Get session custom properties
    #session_id = request.getSessionId() 
    #custom_props = session_dict.get("custom", {})  # get the "custom" dict, default to empty dict
    #list_of_farms = custom_props.get("list_of_farms", []) 

    # Pass it as a parameter to the named query
    #query_params = {"farm_id_list": list_of_farms}  # make sure your named query expects this param

    # Run the named query
    #results = system.db.runNamedQuery("events_table", query_params)

    events = []
    #for row in results:
    #    events.append({
    #        "id": row["setpointid"],
    #        "title": row["setpoint_name"],
    #        "start": toISO8601(row["action_from"]),
    #        "end": toISO8601(row["action_to"])
    #    })

    return {"json": request}