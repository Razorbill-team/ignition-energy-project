-- Params: p_slot_ts (String), p_siteid (Int8), p_farmid (Int8), p_value (Float8), p_userid (Int8)
WITH t AS (
  SELECT
    to_timestamp(:p_slot_ts, 'YYYY-MM-DD HH24:MI:SS')::timestamp AS ts,
    now()                                                         AS "datetime",
    date_trunc('day', to_timestamp(:p_slot_ts, 'YYYY-MM-DD HH24:MI:SS'))::timestamp AS "data",
    EXTRACT(HOUR   FROM to_timestamp(:p_slot_ts, 'YYYY-MM-DD HH24:MI:SS'))::int     AS "hour",
    EXTRACT(MINUTE FROM to_timestamp(:p_slot_ts, 'YYYY-MM-DD HH24:MI:SS'))::int     AS interval_minutes,
    (:p_siteid)::int                                                AS siteid,
    (:p_farmid)::int                                                AS farmid,
    (:p_value)::numeric                                             AS avg_val,
    (:p_userid)::int                                                AS uid
)
INSERT INTO forecast.avg_source_forecast_settings
  (slot_ts, "datetime", "data", "hour", interval_minutes, siteid, farmid, avg_sources, userid)
SELECT t.ts, t."datetime", t."data", t."hour", t.interval_minutes, t.siteid, t.farmid, t.avg_val, t.uid
FROM t
ON CONFLICT (slot_ts, siteid, farmid) DO UPDATE SET
  avg_sources      = EXCLUDED.avg_sources,
  "datetime"       = now(),
  "data"           = EXCLUDED."data",
  "hour"           = EXCLUDED."hour",
  interval_minutes = EXCLUDED.interval_minutes,
  userid           = EXCLUDED.userid
RETURNING 1 AS ok;

