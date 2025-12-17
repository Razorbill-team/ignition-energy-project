SELECT 
    date_trunc('hour', t_stamp) AS t_stamp_sec,
    s."farmid",
  COUNT(*) AS reading_count,
  CAST(SUM("ActivePower") / COUNT(*) AS DECIMAL(20,1)) AS avg_power_kw,
  -- Since 1 hour × avg power = energy in kWh
  CAST(SUM("ActivePower") / COUNT(*) AS DECIMAL(20,0)) AS energy_kwh,
  CAST(SUM("SolarIrradiation") / COUNT(*) AS DECIMAL(20,0)) AS solarirradiance,
  CAST(max("Frequency") as DECIMAL (10,1)) max_freq	,
  CAST(min("Frequency") as DECIMAL (10,1)) min_freq,
  CAST(SUM("Voltage_U12") / COUNT(*) AS DECIMAL(20,1)) as avg_voltage,
  CAST(SUM("ReactivePower") / COUNT(*) as DECIMAL (10,1)) reactive_pw,
  CAST(max("Current_I1") as DECIMAL (10,1)) max_intensity	,
  CAST(min("Current_I1") as DECIMAL (10,1)) min_intensity,
  CAST(SUM("Current_I1") / COUNT(*) as DECIMAL (10,1)) avg_intensity
  
FROM	    integration_schema.raw_realtime_data r
		JOIN
		    integration_schema.link_farm_rawdata m
		    ON r.id_site = m.rawdata_farm_id
		JOIN
		    integration_schema.farms s
		    ON s.farmid = m.farmid
		    
	
WHERE t_stamp >  NOW() - INTERVAL '24 HOURS'

AND s."farmid"=ANY(string_to_array(:param_farmids, ',')::int[])  
GROUP BY  s."farmid",
		date_trunc('hour', t_stamp)
  
ORDER BY date_trunc('hour', t_stamp) ASC