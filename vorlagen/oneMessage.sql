-- MySQL dump 10.13  Distrib 5.5.59, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: FeuerwehrNotifications
-- ------------------------------------------------------
-- Server version	5.5.59-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Alarmdepesche`
--

DROP TABLE IF EXISTS `Alarmdepesche`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Alarmdepesche` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `dbIN` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `messageID` bigint(20) unsigned DEFAULT NULL,
  `Einsatzstichwort` varchar(512) DEFAULT NULL,
  `AlarmiertesEinsatzmittel` varchar(512) DEFAULT NULL,
  `Sondersignal` varchar(512) DEFAULT NULL,
  `Einsatzbeginn` varchar(512) DEFAULT NULL,
  `Einsatznummer` varchar(512) DEFAULT NULL,
  `Auftragsnummer` varchar(512) DEFAULT NULL,
  `Name` varchar(512) DEFAULT NULL,
  `Zusatz` varchar(512) DEFAULT NULL,
  `Sachverhalt` varchar(512) DEFAULT NULL,
  `Patientenname` varchar(512) DEFAULT NULL,
  `Target_Objekt` varchar(512) DEFAULT NULL,
  `Target_Objekttyp` varchar(512) DEFAULT NULL,
  `Target_StrasseHausnummer` varchar(512) DEFAULT NULL,
  `Target_Segment` varchar(512) DEFAULT NULL,
  `Target_PLZOrt` varchar(512) DEFAULT NULL,
  `Target_Region` varchar(512) DEFAULT NULL,
  `Target_Info` varchar(512) DEFAULT NULL,
  `Target_Geopositionen` varchar(256) DEFAULT NULL,
  `TransTarget_Transportziel` varchar(512) DEFAULT NULL,
  `TransTarget_Objekt` varchar(512) DEFAULT NULL,
  `TransTarget_Objekttyp` varchar(512) DEFAULT NULL,
  `TransTarget_StrasseHausnummer` varchar(512) DEFAULT NULL,
  `TransTarget_PLZOrt` varchar(512) DEFAULT NULL,
  `TransTarget_Segment` varchar(512) DEFAULT NULL,
  `TransTarget_Region` varchar(512) DEFAULT NULL,
  `TransTarget_Info` varchar(512) DEFAULT NULL,
  `TransTarget_Geopositionen` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Alarmdepesche`
--

LOCK TABLES `Alarmdepesche` WRITE;
/*!40000 ALTER TABLE `Alarmdepesche` DISABLE KEYS */;
INSERT INTO `Alarmdepesche` VALUES (1,'2018-02-10 07:39:02',12,'ü (Übung','Fl\r\n                Steinbach-Hallenberg 11','Nein','26.09.2017\r\n                10:51:29','19749','20626','','','Testalarmierung','Mustermann, Max\r\n                M','Grundschule/Sporthalle\r\n                Steinb.-H.','SCHULE','Hergeser Wiese 5','Hergeser Wiese','98587 Steinbach-Hallenberg','LK\r\n                Schmalkalden-Meiningen','DEZ 001','geogr. Länge\r\n                10,55958','','APH\r\n                Steinbach-Hallenberg','APH','Brunnenstraße 2','98587 Steinbach-Hallenberg','Brunnenstraße','LK\r\n                Schmalkalden-Meiningen','BMA 092\r\n                Evangelisches AHZ','geogr. Länge\r\n                10,57339');
/*!40000 ALTER TABLE `Alarmdepesche` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-10 14:04:38
