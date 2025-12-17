select 
    to_char(ts.slot_ts, 'HH24:MI') as time_label,
    round(avg(f.forecasted_power_kw),0) as avg_power
from FORECAST.calendar_timeslot_15m ts
left join integration_schema.FORECAST f 
    on ts.slot_ts = f.slot_ts
where f.farmid=ANY(string_to_array(:param_farmids, ',')::int[])  
group by ts.slot_ts
order by ts.slot_ts;
