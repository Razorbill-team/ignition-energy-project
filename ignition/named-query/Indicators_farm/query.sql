select * 
FROM integration_schema.farm_indicators a
inner join integration_schema.farms b on a.farmid=b.farmid