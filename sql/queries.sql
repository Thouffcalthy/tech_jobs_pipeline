
-- Locations sin mapear
SELECT location_name, country
FROM dim_location
WHERE country = 'Unknown'
ORDER BY location_name;

-- Actualizar country
UPDATE dim_location
SET country = ''
WHERE location_name = '';


-- Tags sin clasificar
SELECT tag_name, tag_category
FROM dim_tag
WHERE tag_category = 'other'
ORDER BY tag_name;