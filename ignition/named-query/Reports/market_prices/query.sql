--select * from forecast.trader_output
--select * from  forecast.priority_forecast_indicators
with forex as (
select 
		fx_date
		, max(case when fx_code=978 then rate_to_mdl else 0 END) CCY_EUR 
		, max(case when fx_code=840 then rate_to_mdl else 0 END) CCY_USD 
		, max(case when fx_code=946 then rate_to_mdl else 0 END) CCY_RON 
		, max(case when fx_code=980 then rate_to_mdl else 0 END) CCY_UAH 
from contract.currency
where fx_date between :DateFrom and :DateTo
group by fx_Date 
)

, OPCOM AS( 
		SELECT 
	        'OPCOM'::text AS market,
	        data,
	        interval_hour AS hour_slot,
	        currencyid,
	        case 
	        	 when  opcom.currencyid='978' then fx.CCY_EUR
	        	 when  opcom.currencyid='498' then 1
	        	 when  opcom.currencyid='840' then fx.CCY_USD
	        	 when  opcom.currencyid='946' then fx.CCY_RON
	        	 when  opcom.currencyid='980' then fx.CCY_UAH
	        end CURRENCY_FX_EQ_MDL,
	        forecast_price_closed,
	        case 
	        	 when  opcom.currencyid='978' then opcom.forecast_price_closed*fx.CCY_EUR
	        	 when  opcom.currencyid='498' then opcom.forecast_price_closed*1
	        	 when  opcom.currencyid='840' then opcom.forecast_price_closed*fx.CCY_USD
	        	 when  opcom.currencyid='946' then opcom.forecast_price_closed*fx.CCY_RON
	        	 when  opcom.currencyid='980' then opcom.forecast_price_closed*fx.CCY_UAH
	        end as forecast_price_closed_eq
	    FROM forecast.forecast_p_q_opcom opcom
	    left join forex fx on opcom.data=fx.fx_date
	    WHERE "data" BETWEEN :DateFrom AND :DateTo
    )
--    select * from OPCOM
    , RDN AS( 
    	SELECT 
	        'RDN'::text AS market,
	        data, 
	        interval_hour AS hour_slot,
	        currencyid,
	        case 
	        	 when  rdn.currencyid='978' then fx.CCY_EUR
	        	 when  rdn.currencyid='498' then 1
	        	 when  rdn.currencyid='840' then fx.CCY_USD
	        	 when  rdn.currencyid='946' then fx.CCY_RON
	        	 when  rdn.currencyid='980' then fx.CCY_UAH
	        end CURRENCY_FX_EQ_MDL,
	        forecast_price_closed,
	        case 
	        	 when  rdn.currencyid='978' then rdn.forecast_price_closed*fx.CCY_EUR
	        	 when  rdn.currencyid='498' then rdn.forecast_price_closed*1
	        	 when  rdn.currencyid='840' then rdn.forecast_price_closed*fx.CCY_USD
	        	 when  rdn.currencyid='946' then rdn.forecast_price_closed*fx.CCY_RON
	        	 when  rdn.currencyid='980' then rdn.forecast_price_closed*fx.CCY_UAH
	        end as forecast_price_closed_eq
	    FROM forecast.forecast_p_q_rdn rdn
	    left join forex fx on rdn.data=fx.fx_date
	    WHERE "data" BETWEEN :DateFrom AND :DateTo
	)
--    select * from RDN
, OPEM AS( 
    	SELECT 
	        'OPEM'::text AS market,
	        data, 
	        interval_hour AS hour_slot,
	        currencyid,
	        case 
	        	 when  opem.currencyid='978' then fx.CCY_EUR
	        	 when  opem.currencyid='498' then 1
	        	 when  opem.currencyid='840' then fx.CCY_USD
	        	 when  opem.currencyid='946' then fx.CCY_RON
	        	 when  opem.currencyid='980' then fx.CCY_UAH
	        end CURRENCY_FX_EQ_MDL,
	        forecast_price_closed,
	        case 
	        	 when  opem.currencyid='978' then opem.forecast_price_closed*fx.CCY_EUR
	        	 when  opem.currencyid='498' then opem.forecast_price_closed*1
	        	 when  opem.currencyid='840' then opem.forecast_price_closed*fx.CCY_USD
	        	 when  opem.currencyid='946' then opem.forecast_price_closed*fx.CCY_RON
	        	 when  opem.currencyid='980' then opem.forecast_price_closed*fx.CCY_UAH
	        end as forecast_price_closed_eq
	    FROM forecast.forecast_p_q_opem opem
	    left join forex fx on opem.data=fx.fx_date
	    WHERE "data" BETWEEN :DateFrom AND :DateTo
	)
	select 
		  MARKET
		  , data
		  , hour_slot
		  , currencyid
		  , CURRENCY_FX_EQ_MDL
		  , AVG(forecast_price_closed) as forecast_price_closed
		  , AVG(forecast_price_closed_eq) as forecast_price_closed_eqalter 
	from (	  
	select * from OPCOM
	union all 
	select * from RDN
	union all
	select * from OPEM
    )
    group by MARKET
		  , data
		  , hour_slot
		  , currencyid
		  , CURRENCY_FX_EQ_MDL
	