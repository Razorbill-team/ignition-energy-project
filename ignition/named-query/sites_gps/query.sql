select * from integration_schema.sites
WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  AND siteid = ANY(string_to_array(:site_ids, ',')::int[])