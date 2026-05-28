
-- Locations with unknown country
SELECT location_name, country
FROM dim_location
WHERE country = 'Unknown'
ORDER BY location_name;

-- Update country
UPDATE dim_location
SET country = ''
WHERE location_name = '';


-- Tags without category
SELECT tag_name, tag_category
FROM dim_tag
WHERE tag_category = 'other'
ORDER BY tag_name;

-- Update tag_category
UPDATE dim_tag
SET tag_category = 'technology'
WHERE tag_name IN ('', '', '');

