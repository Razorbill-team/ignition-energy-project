SELECT
    f.farmid        AS farmId,
    f.farm_name     AS farmName,
    s.siteid        AS siteId,
    s.location      AS siteLocation,
    ss.id           AS statusId,
    ss.status_name  AS statusName
FROM   sites s
JOIN   farms f           ON f.siteid = s.siteid
JOIN   status_summary ss ON ss.farmid = f.farmid
WHERE  (:statusCnt = 0)                                         -- show everything
   OR  ss.id = ANY( string_to_array(:statusList, ',')::int[] )  -- filter when list not empty
ORDER  BY f.farmid;




