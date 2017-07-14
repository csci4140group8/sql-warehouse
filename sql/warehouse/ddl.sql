CREATE TABLE `dw_animals` (
  `animal_id` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `scientificname` text CHARACTER SET utf8,
  `vernacularname` text CHARACTER SET utf8,
  `length` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `life_stage` text CHARACTER SET utf8,
  `age` text CHARACTER SET utf8,
  `sex` text CHARACTER SET utf8,
  PRIMARY KEY (`animal_id`)
);

CREATE TABLE `dw_location` (
  `location_id` int(11) NOT NULL AUTO_INCREMENT,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`location_id`)
);

CREATE TABLE `dw_projects` (
  `project_id` varchar(255) CHARACTER SET utf8 NOT NULL,
  `name` text CHARACTER SET utf8,
  `abstract` text CHARACTER SET utf8,
  `geospatial_lat_max` double DEFAULT NULL,
  `geospatial_lat_min` double DEFAULT NULL,
  `geospatial_lon_max` double DEFAULT NULL,
  `geospatial_lon_min` double DEFAULT NULL,
  PRIMARY KEY (`project_id`)
);

CREATE TABLE `dw_time` (
  `time_id` datetime NOT NULL,
  `year` int(4) DEFAULT NULL,
  `month` int(2) DEFAULT NULL,
  `week` int(2) DEFAULT NULL,
  `day` int(2) DEFAULT NULL,
  `hour` int(2) DEFAULT NULL,
  `minute` int(2) DEFAULT NULL,
  `second` int(2) DEFAULT NULL,
  PRIMARY KEY (`time_id`)
);

CREATE TABLE `dw_depth` (
  `depth_id` double NOT NULL,
  PRIMARY KEY (`depth_id`)
);

CREATE TABLE `dw_detections_fact` (
  `project_id` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `location_id` int(11) NOT NULL DEFAULT '0',
  `animal_id` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `time_id` datetime NOT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0',
  PRIMARY KEY (`project_id`,`location_id`,`animal_id`,`time_id`),
  KEY `fk_dw_detections_fact_project` (`project_id`),
  KEY `fk_dw_detections_fact_location` (`location_id`),
  KEY `fk_dw_detections_fact_animal` (`animal_id`),
  KEY `fk_dw_detections_fact_time` (`time_id`),
  CONSTRAINT `fk_dw_detections_fact_project` FOREIGN KEY (`project_id`) REFERENCES `dw_projects` (`project_id`),
  CONSTRAINT `fk_dw_detections_fact_location` FOREIGN KEY (`location_id`) REFERENCES `dw_location` (`location_id`),
  CONSTRAINT `fk_dw_detections_fact_animal` FOREIGN KEY (`animal_id`) REFERENCES `dw_animals` (`animal_id`),
  CONSTRAINT `fk_dw_detections_fact_time` FOREIGN KEY (`time_id`) REFERENCES `dw_time` (`time_id`)
);

CREATE TABLE `dw_platform_fact` (
  `project_id` varchar(255) CHARACTER SET utf8 NOT NULL,
  `location_id` int(11) NOT NULL,
  `depth_id` double NOT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0',
  PRIMARY KEY (`project_id`, `location_id`, `depth_id`),
  KEY `fk_dw_platform_fact_project` (`project_id`),
  CONSTRAINT `fk_dw_platform_fact_project` FOREIGN KEY (`project_id`) REFERENCES `dw_projects` (`project_id`),
  KEY `fk_dw_platform_fact_location` (`location_id`),
  CONSTRAINT `fk_dw_platform_fact_location` FOREIGN KEY (`location_id`) REFERENCES `dw_location` (`location_id`),
  KEY `fk_dw_platform_fact_depth` (`depth_id`),
  CONSTRAINT `fk_dw_platform_fact_depth` FOREIGN KEY (`depth_id`) REFERENCES `dw_depth` (`depth_id`)
);