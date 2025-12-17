select 
--hour,
f.interval_minutes
  --  concat(ts.hour, ':', lpad(f.interval_minutes::text, 2, '0')) as hour_interval,
   -- f.forecasted_power_kw,
   -- f.source_name
from FORECAST.calendar_timeslot_15m ts
left join integration_schema.FORECAST f 
    on ts.slot_ts = f.slot_ts
where f.siteid = 1 
  and f.farmid = 1
order by f.source_name, ts.slot_ts;

