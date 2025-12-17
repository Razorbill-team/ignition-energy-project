WITH forex AS (
    SELECT 
        fx_date,
        MAX(CASE WHEN fx_code = 978 THEN rate_to_mdl ELSE 0 END) AS CCY_EUR,
        MAX(CASE WHEN fx_code = 840 THEN rate_to_mdl ELSE 0 END) AS CCY_USD,
        MAX(CASE WHEN fx_code = 946 THEN rate_to_mdl ELSE 0 END) AS CCY_RON,
        MAX(CASE WHEN fx_code = 980 THEN rate_to_mdl ELSE 0 END) AS CCY_UAH
    FROM contract.currency
    WHERE fx_date BETWEEN :DateFrom AND :DateTo
    GROUP BY fx_date
),

OPCOM AS (
    SELECT 
        'OPCOM'::text AS market,
        data,
        interval_hour AS hour_slot,
        currencyid,
        CASE 
            WHEN opcom.currencyid = '978' THEN fx.CCY_EUR
            WHEN opcom.currencyid = '498' THEN 1
            WHEN opcom.currencyid = '840' THEN fx.CCY_USD
            WHEN opcom.currencyid = '946' THEN fx.CCY_RON
            WHEN opcom.currencyid = '980' THEN fx.CCY_UAH
        END AS CURRENCY_FX_EQ_MDL,
        forecast_price_closed,
        CASE 
            WHEN opcom.currencyid = '978' THEN opcom.forecast_price_closed * fx.CCY_EUR
            WHEN opcom.currencyid = '498' THEN opcom.forecast_price_closed * 1
            WHEN opcom.currencyid = '840' THEN opcom.forecast_price_closed * fx.CCY_USD
            WHEN opcom.currencyid = '946' THEN opcom.forecast_price_closed * fx.CCY_RON
            WHEN opcom.currencyid = '980' THEN opcom.forecast_price_closed * fx.CCY_UAH
        END AS forecast_price_closed_eq,
        opcom.created_at,
        opcom.created_by_userid,
        opcom.updated_at,
        opcom.updated_by_userid,
        opcom.date_from,
        opcom.date_to
    FROM forecast.forecast_p_q_opcom opcom
    LEFT JOIN forex fx 
        ON opcom.data = fx.fx_date
    WHERE opcom.data BETWEEN :DateFrom AND :DateTo
),

RDN AS (
    SELECT 
        'RDN'::text AS market,
        data,
        interval_hour AS hour_slot,
        currencyid,
        CASE 
            WHEN rdn.currencyid = '978' THEN fx.CCY_EUR
            WHEN rdn.currencyid = '498' THEN 1
            WHEN rdn.currencyid = '840' THEN fx.CCY_USD
            WHEN rdn.currencyid = '946' THEN fx.CCY_RON
            WHEN rdn.currencyid = '980' THEN fx.CCY_UAH
        END AS CURRENCY_FX_EQ_MDL,
        forecast_price_closed,
        CASE 
            WHEN rdn.currencyid = '978' THEN rdn.forecast_price_closed * fx.CCY_EUR
            WHEN rdn.currencyid = '498' THEN rdn.forecast_price_closed * 1
            WHEN rdn.currencyid = '840' THEN rdn.forecast_price_closed * fx.CCY_USD
            WHEN rdn.currencyid = '946' THEN rdn.forecast_price_closed * fx.CCY_RON
            WHEN rdn.currencyid = '980' THEN rdn.forecast_price_closed * fx.CCY_UAH
        END AS forecast_price_closed_eq,
        rdn.created_at,
        rdn.created_by_userid,
        rdn.updated_at,
        rdn.updated_by_userid,
        rdn.date_from,
        rdn.date_to
    FROM forecast.forecast_p_q_rdn rdn
    LEFT JOIN forex fx 
        ON rdn.data = fx.fx_date
    WHERE rdn.data BETWEEN :DateFrom AND :DateTo
),

OPEM AS (
    SELECT 
        'OPEM'::text AS market,
        data,
        interval_hour AS hour_slot,
        currencyid,
        CASE 
            WHEN opem.currencyid = '978' THEN fx.CCY_EUR
            WHEN opem.currencyid = '498' THEN 1
            WHEN opem.currencyid = '840' THEN fx.CCY_USD
            WHEN opem.currencyid = '946' THEN fx.CCY_RON
            WHEN opem.currencyid = '980' THEN fx.CCY_UAH
        END AS CURRENCY_FX_EQ_MDL,
        forecast_price_closed,
        CASE 
            WHEN opem.currencyid = '978' THEN opem.forecast_price_closed * fx.CCY_EUR
            WHEN opem.currencyid = '498' THEN opem.forecast_price_closed * 1
            WHEN opem.currencyid = '840' THEN opem.forecast_price_closed * fx.CCY_USD
            WHEN opem.currencyid = '946' THEN opem.forecast_price_closed * fx.CCY_RON
            WHEN opem.currencyid = '980' THEN opem.forecast_price_closed * fx.CCY_UAH
        END AS forecast_price_closed_eq,
        opem.created_at,
        opem.created_by_userid,
        opem.updated_at,
        opem.updated_by_userid,
        opem.date_from,
        opem.date_to
    FROM forecast.forecast_p_q_opem opem
    LEFT JOIN forex fx 
        ON opem.data = fx.fx_date
    WHERE opem.data BETWEEN :DateFrom AND :DateTo
)

SELECT 
    t.market,
    t.data,
    t.hour_slot,
    t.currencyid,
    t.CURRENCY_FX_EQ_MDL,
    ROUND(AVG(t.forecast_price_closed), 1)    AS forecast_price_closed,
    ROUND(AVG(t.forecast_price_closed_eq), 1) AS forecast_price_closed_eq,
    t.created_at,
    t.created_by_userid,
    us_create.USER_ROLE_NAME  AS user_role_created,
    us_create.Display_name    AS create_user_name,
    t.updated_at,
    t.updated_by_userid,
    us_update.USER_ROLE_NAME  AS user_role_updated,
    us_update.Display_name    AS updated_user_name,
    t.date_from,
    t.date_to
FROM (
    SELECT * FROM OPCOM
    UNION ALL 
    SELECT * FROM RDN
    UNION ALL
    SELECT * FROM OPEM
) AS t
LEFT JOIN user_schema.user_names us_create 
    ON t.created_by_userid = us_create.ID
LEFT JOIN user_schema.user_names us_update 
    ON t.updated_by_userid = us_update.ID   -- <<< FIXED
WHERE
    t.market     = COALESCE(:Market, t.market)
    AND t.currencyid = COALESCE(:Currency, t.currencyid)
    AND t.hour_slot  = COALESCE(:Hour, t.hour_slot)
GROUP BY 
    t.market,
    t.data,
    t.hour_slot,
    t.currencyid,
    t.CURRENCY_FX_EQ_MDL,
    t.created_at,
    t.created_by_userid,
    us_create.USER_ROLE_NAME,
    us_create.Display_name,
    t.updated_at,
    t.updated_by_userid,
    us_update.USER_ROLE_NAME,
    us_update.Display_name,
    t.date_from,
    t.date_to
ORDER BY
    t.data,
    t.hour_slot,
    t.market,
    t.currencyid;
