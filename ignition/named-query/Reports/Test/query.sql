WITH rng AS (
  SELECT ts.slot_ts, ts.date, ts.hour, ts.minute_in_hour as interval_minutes
  FROM FORECAST.calendar_timeslot_15m  ts
  WHERE ts.slot_ts BETWEEN :date_from AND :date_to
--  WHERE ts.slot_ts BETWEEN '2025-09-09 10:00:00' AND '2025-09-09 12:00:00'
)
select * from rng