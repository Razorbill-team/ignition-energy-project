select hour,
minute_in_hour,
forecasted_power_kw,
source_name

from  FORECAST.calendar_timeslot_15m ts     left
 join integration_schema.FORECAST f on (ts.slot_ts=f.slot_ts)    where siteid=1 and farmid=1    order by f.source_name, ts.slot_ts