SELECT DISTINCT
	CASE 
		WHEN  :farms_sites=0 THEN site_id 
		ELSE farmid 
	END as value
	, CASE 
		WHEN  :farms_sites=0 THEN location 
		ELSE farm_name 
	END as label
	
FROM 
(
SELECT  farmid, farm_name, sites.siteid as site_id, location
FROM sites
LEFT JOIN farms ON sites.siteid = farms.siteid
WHERE 
  (
    :param1 IS NULL
    OR :param1 = ''
    OR LOWER(:param1) = 'null'
    OR LOWER(:param1) = 'none'
    OR farm_type = ANY(string_to_array(:param1, ','))
  )
and farmid = ANY(string_to_array(:farmid, ',')::int[])  

)
ORDER BY value
