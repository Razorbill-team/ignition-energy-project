SELECT
  --DISTINCT ON (t1.farmid, t1.setpointid)
  *
FROM setpoints_historical_table t1
LEFT JOIN integration_schema.SETPOINTS_INDICATORS t2 ON t1.setpointid = t2.id
LEFT JOIN farms f ON t1.farmid = f.farmid
WHERE t1.farmid = ANY(string_to_array(:farm_id_list, ',')::int[])
  AND t1.action_from < (:today_date::date + INTERVAL '2 day')   -- starts before end of tomorrow
  AND t1.action_to   >=  :today_date::date                      -- ends after start of today
ORDER BY t1.setpointid, f.farm_name, t1.event_time DESC