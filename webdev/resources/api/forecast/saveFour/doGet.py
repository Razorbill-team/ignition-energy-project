def doGet(request, session):
def doPost(request, session):
    import system
    from project import forecast_api

    try:
        payload = system.util.jsonDecode(request.get("body") or "{}")
    except:
        return {"status": 400, "body": "Bad JSON"}

    res = forecast_api.save_four_rows(
        payload,
        datasource="YourDS",   # <-- change to your DB connection name
        db_kind="oracle"       # or "postgres"
    )

    return {
        "status": 200 if not res["errors"] else 400,
        "headers": {"Content-Type":"application/json", "Access-Control-Allow-Origin":"*"},
        "body": system.util.jsonEncode(res)
    }

def doOptions(request, session):
    return {
        "status": 204,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
    }