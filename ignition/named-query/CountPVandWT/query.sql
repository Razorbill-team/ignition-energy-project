SELECT 
    COUNT(*) AS assetCount, 
    COUNT(DISTINCT sites.siteid) AS siteCount
FROM 
    sites
LEFT JOIN 
    farms ON sites.siteid = farms.siteid
WHERE 
    farm_NAME LIKE 'WT%';


