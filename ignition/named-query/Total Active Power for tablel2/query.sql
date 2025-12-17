select * from (select * from (SELECT
  s.location ,
  f.farm_name ,
  r."ActivePower" active_power,
  -- r.rated_power rated_power ,
  r."ReactivePower" reactive_power,
 -- r."Voltage_U12",
 -- r."Current_I1",
  r."PowerFactor", 
  r."Frequency",
  r."ActivePowerAvailable",
  r."SolarIrradiation" ,
  r.t_stamp
--  case when farm_name like 'PV%' then irradiance  else windspeed end as meteo
FROM
    integration_schema.sites s
JOIN integration_schema.farms f
    ON s.siteid = f.siteid
JOIN integration_schema.link_farm_rawdata m
    ON f.farmid = m.farmid   
JOIN integration_schema.raw_realtime_data r
    ON r.id_site = m.rawdata_farm_id
join (select id_site, max(t_stamp) ttime from integration_schema.raw_realtime_data m group by id_site) t1
on (t1.id_site=r.id_site and r.t_stamp=t1.ttime)
WHERE
    --f.farm_name in('PV1_Ungheni','PV1_Negureni','PV1_Radeni') 
    f.farmid = ANY(string_to_array(:list_of_farms, ',')::integer[])
    ) 
 union 
 select * from (SELECT
  s.location ,
  f.farm_name ,
  r."ActivePower" active_power,
  -- r.rated_power rated_power ,
  r."ReactivePower" reactive_power,
 -- r."Voltage_U12",
 -- r."Current_I1",
  r."PowerFactor", 
  r."Frequency",
  r."ActivePowerAvailable",
  r."SolarIrradiation" ,
  r.t_stamp
--  case when farm_name like 'PV%' then irradiance  else windspeed end as meteo
FROM
    integration_schema.sites s
JOIN integration_schema.farms f
    ON s.siteid = f.siteid
JOIN integration_schema.link_farm_rawdata m
    ON f.farmid = m.farmid   
JOIN integration_schema.raw_fake_realtime_data r
    ON r.id_site = m.rawdata_farm_id
join (select id_site, max(t_stamp) ttime from integration_schema.raw_fake_realtime_data m group by id_site) t1
on (t1.id_site=r.id_site and r.t_stamp=t1.ttime)
WHERE
    --f.farm_name in('PV1_Ungheni','PV1_Negureni','PV1_Radeni') 
    f.farmid = ANY(string_to_array(:list_of_farms, ',')::integer[])
    ) ) order by location; 