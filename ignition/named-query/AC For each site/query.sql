SELECT 
    SUM(fi.rated_power) AS "Active Power"
FROM 
    integration_schema.farm_indicators fi
left JOIN 
    integration_schema.farms s ON fi.farmid = s.farmid
where
	s.farmid = :farm_id


