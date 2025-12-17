SELECT location, farm_name, farmid, sites.siteid as site_id
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
