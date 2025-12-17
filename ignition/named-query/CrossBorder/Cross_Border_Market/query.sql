WITH sec_ro AS (
    SELECT
        currencyid,
        date_from,
        date_to,
        hour,
        AVG(forecast_price_section_import)    AS forecast_price_section_import,
        AVG(forecast_price_section_export)    AS forecast_price_section_export,
        AVG(forecast_quantity_section_import) AS forecast_quantity_section_import,
        AVG(forecast_quantity_section_export) AS forecast_quantity_section_export
    FROM forecast.forecast_section_ro
    WHERE data BETWEEN :DateFrom AND :DateTo
    GROUP BY currencyid, date_from, date_to, hour
),
sec_ua AS (
    SELECT
        currencyid,
        date_from,
        date_to,
        hour,
        AVG(forecast_price_section_import)    AS forecast_price_section_import,
        AVG(forecast_price_section_export)    AS forecast_price_section_export,
        AVG(forecast_quantity_section_import) AS forecast_quantity_section_import,
        AVG(forecast_quantity_section_export) AS forecast_quantity_section_export
    FROM forecast.forecast_section_ua
    WHERE data BETWEEN :DateFrom AND :DateTo
    GROUP BY currencyid, date_from, date_to, hour
)

SELECT
    'RO' AS area,
    currencyid,
    forecast_price_section_import,
    forecast_price_section_export,
    forecast_quantity_section_import,
    forecast_quantity_section_export,
    hour,
    date_from,
    date_to
FROM sec_ro

UNION ALL

SELECT
    'UA' AS area,
    currencyid,
    forecast_price_section_import,
    forecast_price_section_export,
    forecast_quantity_section_import,
    forecast_quantity_section_export,
    hour,
    date_from,
    date_to
FROM sec_ua

ORDER BY hour, area, date_from;
