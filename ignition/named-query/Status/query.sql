select sites.SITEID, location, farms.farmID,farm_name, ss.id Status_ID, ss.STATUS_NAME, COUNT(ss.farmid) Nr_Assets
from sites
left join farms on sites.siteid = farms.siteid
left join integration_schema.status_summary2 ss on farms.farmid=ss.farmid
/*where farms.farm_type=(COALESCE(:param1,farms.farm_type))
	  and ss.status_name =COALESCE(:status, ss.status_name)*/
group by sites.SITEID, location, farms.farmID,farm_name, ss.id, ss.STATUS_NAME	  