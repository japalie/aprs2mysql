DROP DATABASE `aprs`;
CREATE DATABASE IF NOT EXISTS `aprs`;
USE `aprs`;
DROP TABLE IF EXISTS `packets`;
CREATE TABLE `packets` (
  `ins_timestamp` timestamp NULL DEFAULT current_timestamp(),
  
  `format` varchar(32) DEFAULT NULL,
  
  `from` varchar(32) DEFAULT NULL,
  `to` varchar(32) DEFAULT NULL,
  `symbol_table` varchar(32) DEFAULT NULL,
  `symbol` varchar(32) DEFAULT NULL,
  
  `via` varchar(256) DEFAULT NULL,
  `path` varchar(1024) DEFAULT NULL,
  
  `messagecapable` varchar(32) DEFAULT NULL,
  
  `latitude` varchar(32) DEFAULT NULL,
  `longitude` varchar(32) DEFAULT NULL,
  `gpsfixstatus` varchar(32) DEFAULT NULL,
  `posAmbiguity` varchar(32) DEFAULT NULL,
  `altitude` varchar(32) DEFAULT NULL,
  `speed` varchar(32) DEFAULT NULL,
  `course` varchar(32) DEFAULT NULL,
    
  `comment` varchar(1024) DEFAULT NULL,
  `text` varchar(1024) DEFAULT NULL,
  `commentb64` varchar(1024) DEFAULT NULL,
  `textb64` varchar(1024) DEFAULT NULL,
  
  `phg` varchar(32) DEFAULT NULL,
  `rng` varchar(32) DEFAULT NULL,

  `humidity` varchar(32) DEFAULT NULL,
  `pressure` varchar(32) DEFAULT NULL,
  `rain_1h` varchar(32) DEFAULT NULL,
  `rain_24h` varchar(32) DEFAULT NULL,
  `rain_since_midnight` varchar(32) DEFAULT NULL,
  `temperature` varchar(32) DEFAULT NULL,
  `wind_direction` varchar(32) DEFAULT NULL,
  `wind_gust` varchar(32) DEFAULT NULL,
  `wind_speed` varchar(32) DEFAULT NULL,

  `addresse` varchar(32) DEFAULT NULL,
  `message_text` varchar(1024) DEFAULT NULL,
  `message_textb64` varchar(1024) DEFAULT NULL,
  `msgNo` varchar(32) DEFAULT NULL,
  `response` varchar(32) DEFAULT NULL,
 
  `bid` varchar(32) DEFAULT NULL,
  `identifier` varchar(32) DEFAULT NULL,
  
  `raw_timestamp` varchar(32) DEFAULT NULL,
  `timestamp` varchar(32) DEFAULT NULL,
  
  `seq` varchar(32) DEFAULT NULL,
  `bits` varchar(32) DEFAULT NULL,
  `analog1` varchar(32) DEFAULT NULL,
  `analog2` varchar(32) DEFAULT NULL,
  `analog3` varchar(32) DEFAULT NULL,
  `analog4` varchar(32) DEFAULT NULL,
  `analog5` varchar(32) DEFAULT NULL,
  
  `mbits` varchar(32) DEFAULT NULL,
  `mtype` varchar(32) DEFAULT NULL,
  `daodatumbyte` varchar(32) DEFAULT NULL,
  
  `alive` varchar(32) DEFAULT NULL,
  
  `raw` varchar(1024) NOT NULL,
  `rawb64` varchar(1024) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

ALTER TABLE `packets`
  ADD KEY `ind_from` (`from`),
  ADD KEY `ind_ins_timestamp` (`ins_timestamp`),
  ADD KEY `ind_via` (`via`(255)),
  ADD KEY `ind_latitude` (`latitude`),
  ADD KEY `ind_longitude` (`longitude`),
  ADD KEY `ind_format` (`format`),
  ADD KEY `ind_addresse` (`addresse`),
  ADD KEY `ind_to` (`to`);
COMMIT;
