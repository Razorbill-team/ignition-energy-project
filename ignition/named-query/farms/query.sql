select location, farm_name 
from sites
left join farms on sites.siteid=farms.siteid