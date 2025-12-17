SELECT 
    SUM(fi.COUNT) AS "ERROR"
FROM 
    integration_schema.status_summary fi
JOIN 
    integration_schema.farms s ON fi.farmid = s.farmid
WHERE 
    s.farmid = :farm_id