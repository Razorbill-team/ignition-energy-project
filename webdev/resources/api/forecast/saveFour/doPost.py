def doPost(request, session):

    import system, traceback
    import forecast_api  # Project Library script

    log = system.util.getLogger("WebDev.saveFour")

    # Parse JSON body
    try:
        raw = request.get("body") or "{}"
        payload = system.util.jsonDecode(raw)
        log.info("Payload received: %s" % str(payload))
    except Exception, e:
        return {
            "status": 400,
            "headers": {"Content-Type":"application/json","Access-Control-Allow-Origin":"*"},
            "body": system.util.jsonEncode({"inserted":0, "errors":["Bad JSON", unicode(e)]})
        }

    # Call backend
    try:
        res = forecast_api.save_four_rows(
            payload,
            datasource="postgresDB",   # <-- CHANGE to your DB connection name
            db_kind="oracle"       # or "postgres"
        )
        log.info("Result: %s" % str(res))
        return {
            "status": 200 if not res.get("errors") else 400,
            "headers": {"Content-Type":"application/json","Access-Control-Allow-Origin":"*"},
            "body": system.util.jsonEncode(res)
        }
    except Exception, e:
        tb = traceback.format_exc()
        log.error("save_four_rows failed: %s" % unicode(e))
        log.error(tb)
        return {
            "status": 500,
            "headers": {"Content-Type":"application/json","Access-Control-Allow-Origin":"*"},
            "body": system.util.jsonEncode({"inserted":0, "errors":[unicode(e)], "trace": tb})
        }