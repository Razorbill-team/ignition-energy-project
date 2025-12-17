select 
    to_char(ts.slot_ts, 'HH24:MI') as time_label,
    f.forecasted_power_kw,
    f.source_name
    --avg(f.forecasted_power_kw) over (partition by f.source_name,ts.slot_ts) as avg_power_kw
from FORECAST.calendar_timeslot_15m ts
left join integration_schema.FORECAST f 
    on ts.slot_ts = f.slot_ts
where f.farmid=ANY(string_to_array(:param_farmids, ',')::int[])  
order by f.source_name, ts.slot_ts;
