WITH rng AS (
  SELECT ts.slot_ts, ts.date, ts.hour, ts.minute_in_hour as interval_minutes
  FROM FORECAST.calendar_timeslot_15m  ts
  WHERE ts.slot_ts BETWEEN :date_from AND :date_to
)
, farms as (select 
				  s.siteid
				  , s.location as site_name
				  , f.farmid
				  , f.farm_name 
				  , 1 as Source_1
				  , 2 as Source_2
				  , 3 as Source_3
				  , 4 as AVG_Sources
				  , 5 as Auto_correction
				  , 6 as Manual_correction
				  , 7 as Final_Setpoint
			from integration_schema.sites s
			left join integration_schema.farms f on s.siteid=f.siteid
			)
, cte_rng_1 as (
SELECT
	  r.slot_ts,
	  r.date,
	  r.hour,
	  r.interval_minutes,
	  mfs.siteid, 
	  mfs.farmid,
	  mfs.manual_correction,
	  mfs.userid,
	  mfs.datetime AS corrected_at
FROM  forecast.manual_forecast_settings mfs 
LEFT JOIN rng r on mfs.slot_ts = r.slot_ts
)
select 
		 a.slot_ts 
		, a.date
		, a.hour
		, a.interval_minutes
		, a.siteid
		, a.site_name
		, a.farmid
		, a.farm_name
		, stat.ID as status_id
		, stat.status_name
		
--		, a.indicator_name
		, b.last_forecast_datetime
		, b.data_forecast
		, b.ora_forecast
		
		, b.id_source
		, b.source_name
		, b.irradiation
		, b.wind_speed
		, b.forecasted_power_kw
		, 0 as AVG_Sources
		, 0 as Auto_correction
		, c.manual_correction
		, 0 as Final_forecast
		, 125 as Total_General
		
from (rng 
	  cross join farms
	  ) a
left join integration_schema.FORECAST b on a.farmid=b.farmid and a.slot_ts=b.slot_ts
left join cte_rng_1 c on a.farmid=c.farmid and a.slot_ts=c.slot_ts
left join integration_schema.status_summary stat on a.farmid=stat.farmid
where 
	a."farmid"=ANY(string_to_array(:param_farmids, ',')::int[])  
	and 
	a.slot_ts between :date_from and :date_to
--	                  and a.farmid=1