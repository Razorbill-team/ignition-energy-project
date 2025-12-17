select 
    to_char(ts.slot_ts, 'HH24:MI') as time_label,
    f.irradiation
from FORECAST.calendar_timeslot_15m ts
left join integration_schema.FORECAST f 
    on ts.slot_ts = f.slot_ts
where f.farmid=ANY(string_to_array(:param_farmids, ',')::int[])  
  and f.id_source=1
group by ts.slot_ts,f.irradiation
order by ts.slot_ts;
