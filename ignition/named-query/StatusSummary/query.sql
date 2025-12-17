SELECT distinct id as statusId ,
status_name as status,
count (farmid) cnt
,'Statuses'   AS rp 
FROM status_summary
group by id, status_name
ORDER BY status;
