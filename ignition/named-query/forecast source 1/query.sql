select 
    round(avg(f.forecasted_power_kw), 2) as avgpower
from integration_schema.FORECAST f
where f.siteid = 1 
  and f.farmid = 1
  and f.source_name = 'Source 1'
  and f.forecasted_power_kw <> 0;
