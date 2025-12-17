select
	sum(r."ActivePower") as active_power_per_site
FROM
    integration_schema.raw_realtime_data r
JOIN
    integration_schema.link_farm_rawdata m
    ON r.id_site = m.rawdata_farm_id
JOIN
    integration_schema.farms s
    ON s.farmid = m.farmid
WHERE
    s.farm_name in('PV1_Ungheni','PV1_Negureni','PV1_Radeni') 
    and s.siteid = :site_id
    --AND s.farmid = ANY(string_to_array(:farm_id_list, ',')::int[])
group by s.siteid,t_stamp 
order by t_stamp desc
limit 1