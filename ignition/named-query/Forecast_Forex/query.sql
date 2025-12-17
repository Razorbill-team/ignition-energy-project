SELECT day_date, currency_id, exchange_rate, eq_value
FROM forecast.forex
WHERE day_date BETWEEN :DateFrom AND :DateTo