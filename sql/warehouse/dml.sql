INSERT INTO dw_animals (animal_id, scientificname, vernacularname, length, weight, life_stage, age, sex)
SELECT animal_reference_id as 'animal_id', scientificname, vernacularname, length, weight, life_stage, age, sex
FROM animals;

INSERT INTO dw_location (latitude, longitude)
SELECT DISTINCT latitude, longitude
FROM detections;

INSERT INTO dw_projects (project_id, name, abstract, geospatial_lat_max, geospatial_lat_min, geospatial_lon_max, geospatial_lon_min)
SELECT project_reference as 'project_id', project_name as 'name', project_abstract as 'abstract', project_geospatial_lat_max as 'geospatial_lat_max', project_geospatial_lat_min as 'geospatial_lat_min', project_geospatial_lon_max as 'geospatial_lon_max', project_geospatial_lon_min as 'geospatial_lon_min'
FROM projects;

INSERT INTO dw_platform (platform_id, project_id, type, depth, name, latitude, longitude)
SELECT platform_guid as 'platform_id', platform_project_reference as 'project_id', platform_type as 'type', platform_depth as 'depth', platform_name as 'name', latitude, longitude
FROM platforms;

INSERT INTO dw_time (time_id, year, month, week, day, hour, minute, second)
SELECT DISTINCT time as 'time_id', YEAR(time) as 'year', MONTH(time) as 'month', WEEK(time) as 'week', DAY(time) as 'day', HOUR(time) as 'hour', MINUTE(time) as 'minute', SECOND(time) as 'second'
FROM detections;

INSERT INTO dw_detections_fact (project_id, location_id, animal_id, time_id, count)
SELECT detection_project_reference AS 'project_id', location_id, detection_reference_id AS 'animal_id', time AS 'time_id', count(*) as count
FROM detections, dw_location
WHERE detections.latitude = dw_location.latitude AND detections.longitude = dw_location.longitude
GROUP BY detection_project_reference, animal_id, time, dw_location.location_id;
