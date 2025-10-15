-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: database-qms.cz4k2g48gx5h.ap-south-1.rds.amazonaws.com    Database: QMS
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `factor` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','password',0.6,23.12446,72.54559,'2025-10-13 18:32:38','2025-10-11 13:13:13');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `time_slot` time NOT NULL,
  `is_booked` tinyint(1) NOT NULL DEFAULT '0',
  `token_id` int unsigned DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `token_id` (`token_id`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,'09:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-05 13:10:38'),(3,'09:30:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(5,'10:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-13 17:53:09'),(7,'10:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-11 06:55:40'),(9,'11:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(11,'11:30:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(13,'12:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(15,'12:30:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(17,'13:00:00',1,56,'2025-09-28 10:59:04','2025-10-14 06:54:29'),(19,'13:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-13 17:53:09'),(21,'14:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-11 06:55:40'),(23,'14:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-11 06:55:40'),(25,'15:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(27,'15:30:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(29,'16:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(31,'16:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-13 17:53:09'),(33,'17:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing`
--

DROP TABLE IF EXISTS `billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing`
--

LOCK TABLES `billing` WRITE;
/*!40000 ALTER TABLE `billing` DISABLE KEYS */;
INSERT INTO `billing` VALUES (1,0,61,'00:00:00','2025-10-14 09:22:12','2025-10-14 09:22:12'),(2,1,63,'00:00:24','2025-10-14 09:40:38','2025-10-14 09:40:38'),(3,2,64,'00:00:48','2025-10-14 09:42:58','2025-10-14 09:42:58');
/*!40000 ALTER TABLE `billing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaint`
--

DROP TABLE IF EXISTS `complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint`
--

LOCK TABLES `complaint` WRITE;
/*!40000 ALTER TABLE `complaint` DISABLE KEYS */;
INSERT INTO `complaint` VALUES (14,2,32,'00:00:59','2025-10-13 17:42:14','2025-10-13 17:42:14'),(15,3,41,'00:01:17','2025-10-14 02:08:14','2025-10-14 02:08:14'),(16,4,47,'00:01:43','2025-10-14 02:27:40','2025-10-14 02:27:40'),(17,5,46,'00:02:09','2025-10-14 02:28:33','2025-10-14 02:28:33'),(18,5,48,'00:02:10','2025-10-14 06:54:13','2025-10-14 06:54:13');
/*!40000 ALTER TABLE `complaint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consumer`
--

DROP TABLE IF EXISTS `consumer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consumer` (
  `consumer_id` varchar(100) DEFAULT NULL,
  `email_id` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consumer`
--

LOCK TABLES `consumer` WRITE;
/*!40000 ALTER TABLE `consumer` DISABLE KEYS */;
INSERT INTO `consumer` VALUES ('C1234','krishnabhatiya211@gmail.com'),('C4321','tirthkavathiya@gmail.com');
/*!40000 ALTER TABLE `consumer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `consumer_id` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `service_id` int unsigned DEFAULT NULL,
  `token_id` int unsigned DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  KEY `fk_customer_service` (`service_id`),
  CONSTRAINT `fk_customer_service` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`),
  CONSTRAINT `fk_customer_token` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (34,'Swapnil ',NULL,'swapnilpatil24680@gmail.com',2,34,'2025-10-13 18:09:38','2025-10-13 18:09:39'),(36,'Ahir Hevin',NULL,'hevinahir179@gmail.com',3,36,'2025-10-13 18:10:37','2025-10-13 18:17:13'),(41,'BHATIYA KAVYA BHAVIN',NULL,'krishnabhatiya211@gmail.com',2,41,'2025-10-14 02:06:00','2025-10-14 02:06:01'),(44,'Ynk',NULL,'tirthkavathiya@gmail.com',1,44,'2025-10-14 02:07:49','2025-10-14 02:07:50'),(46,'Rahul',NULL,'swapnilpatil3075@gmail.com',2,46,'2025-10-14 02:21:46','2025-10-14 02:21:46'),(47,'Rahul',NULL,'swapnil1282patil@gmail.com',2,47,'2025-10-14 02:25:05','2025-10-14 02:25:06'),(48,'Krupal',NULL,'swapnilpatil3075@gmail.com',2,48,'2025-10-14 02:29:29','2025-10-14 06:54:13'),(49,'Aditya',NULL,'prajapatian1533@gmail.com',2,49,'2025-10-14 02:29:39','2025-10-14 02:29:40'),(51,'Jay',NULL,'swapnilpatil3075@gmail.com',3,51,'2025-10-14 02:33:55','2025-10-14 02:33:56'),(52,'Sahil',NULL,'prajapatian1533@gmail.com',3,52,'2025-10-14 02:37:54','2025-10-14 02:37:55'),(53,'Ketan',NULL,'swapnilpatil24680@gmail.com',1,53,'2025-10-14 06:42:37','2025-10-14 06:42:38'),(54,'Sanjay',NULL,'prajapatian1533@gmail.com',3,54,'2025-10-14 06:44:11','2025-10-14 06:44:12'),(55,'Arjun',NULL,'Swapnilpatil24680@gmail.com',1,55,'2025-10-14 06:45:03','2025-10-14 06:45:04'),(56,'Ketan',NULL,'swapnilpatil24680@gmail.com',1,56,'2025-10-14 06:52:46','2025-10-14 06:52:47'),(57,'adsa',NULL,'tirthkavathiya@gmail.com',3,57,'2025-10-14 07:46:56','2025-10-14 08:11:17'),(58,'fdsf',NULL,'tirthkavathiya@gmail.com',1,58,'2025-10-14 09:07:01','2025-10-14 09:07:02'),(59,'Hevin',NULL,'hevinahir179@gmail.com',2,59,'2025-10-14 09:12:31','2025-10-14 09:12:32'),(60,'Hevi ',NULL,'hevinahir179@gmail.com',2,60,'2025-10-14 09:14:59','2025-10-14 09:15:00'),(61,'Hai yyd',NULL,'swapnilpatil24680@gmail.com',1,61,'2025-10-14 09:20:55','2025-10-14 09:20:55'),(64,'adsa',NULL,'tirthkavathiya@gmail.com',1,62,'2025-10-14 09:31:27','2025-10-14 09:31:29'),(65,'ads',NULL,'tirthkavathiya@gmail.com',1,63,'2025-10-14 09:39:44','2025-10-14 09:39:47'),(66,'sdsa',NULL,'tirthkavathiya@gmail.com',1,64,'2025-10-14 09:40:57','2025-10-14 09:41:01'),(67,'tirth',NULL,'tirthkavathiya@gmail.com',1,65,'2025-10-14 09:41:47','2025-10-14 09:41:48');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `details transfer`
--

DROP TABLE IF EXISTS `details transfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `details transfer` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `details transfer`
--

LOCK TABLES `details transfer` WRITE;
/*!40000 ALTER TABLE `details transfer` DISABLE KEYS */;
/*!40000 ALTER TABLE `details transfer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general enquiry`
--

DROP TABLE IF EXISTS `general enquiry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `general enquiry` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general enquiry`
--

LOCK TABLES `general enquiry` WRITE;
/*!40000 ALTER TABLE `general enquiry` DISABLE KEYS */;
/*!40000 ALTER TABLE `general enquiry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identity verification`
--

DROP TABLE IF EXISTS `identity verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `identity verification` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identity verification`
--

LOCK TABLES `identity verification` WRITE;
/*!40000 ALTER TABLE `identity verification` DISABLE KEYS */;
/*!40000 ALTER TABLE `identity verification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kyc`
--

DROP TABLE IF EXISTS `kyc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kyc` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kyc`
--

LOCK TABLES `kyc` WRITE;
/*!40000 ALTER TABLE `kyc` DISABLE KEYS */;
INSERT INTO `kyc` VALUES (3,2,36,'00:00:51','2025-10-13 18:17:13','2025-10-14 06:52:41'),(6,0,51,'00:00:00','2025-10-14 02:35:02','2025-10-14 06:52:41'),(7,1,52,'00:00:25','2025-10-14 02:39:42','2025-10-14 06:52:41'),(8,3,54,'00:01:17','2025-10-14 06:46:39','2025-10-14 06:52:41'),(9,4,29,'00:01:44','2025-10-14 06:56:40','2025-10-14 06:56:40'),(10,5,57,'00:01:52','2025-10-14 08:11:17','2025-10-14 08:11:17');
/*!40000 ALTER TABLE `kyc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `late_tokens`
--

DROP TABLE IF EXISTS `late_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `late_tokens` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `token_id` int unsigned NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `late_tokens`
--

LOCK TABLES `late_tokens` WRITE;
/*!40000 ALTER TABLE `late_tokens` DISABLE KEYS */;
INSERT INTO `late_tokens` VALUES (1,14,'2025-10-11 16:56:37'),(2,17,'2025-10-11 16:59:04');
/*!40000 ALTER TABLE `late_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `log` time DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'00:00:04'),(2,'00:02:04'),(3,'00:00:03'),(4,'00:00:25'),(5,'00:02:22'),(6,'00:00:04'),(7,'00:00:06'),(8,'00:00:24'),(9,'00:00:39'),(10,'00:00:06'),(11,'00:00:02'),(12,'00:00:04'),(13,'00:00:02'),(14,'00:00:06'),(15,'00:00:11'),(16,'00:00:11'),(17,'00:00:29'),(18,'00:00:08'),(19,'00:00:11'),(20,'00:00:11'),(21,'00:00:11'),(22,'00:00:11'),(23,'00:00:58');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meter related`
--

DROP TABLE IF EXISTS `meter related`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meter related` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meter related`
--

LOCK TABLES `meter related` WRITE;
/*!40000 ALTER TABLE `meter related` DISABLE KEYS */;
/*!40000 ALTER TABLE `meter related` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `otp_verification`
--

DROP TABLE IF EXISTS `otp_verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `otp_verification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int unsigned NOT NULL,
  `otp_code` varchar(6) NOT NULL,
  `expires_at` datetime NOT NULL,
  `verified` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `otp_verification_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `otp_verification`
--

LOCK TABLES `otp_verification` WRITE;
/*!40000 ALTER TABLE `otp_verification` DISABLE KEYS */;
INSERT INTO `otp_verification` VALUES (77,64,'244991','2025-10-14 15:06:43',0,'2025-10-14 09:31:43');
/*!40000 ALTER TABLE `otp_verification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (0,'Revoked','2025-10-11 18:56:28','2025-10-11 19:00:39'),(1,'Billing','2025-09-26 12:17:13','2025-09-26 12:17:13'),(2,'Complaint','2025-09-26 12:17:13','2025-10-11 08:11:38'),(3,'KYC','2025-09-26 12:17:13','2025-10-11 08:11:38'),(15,'Meter Related','2025-10-14 09:30:28','2025-10-14 09:30:28'),(16,'Details Transfer','2025-10-14 09:30:28','2025-10-14 09:30:28'),(17,'General Enquiry','2025-10-14 09:30:28','2025-10-14 09:30:28'),(18,'Network Infrastructure','2025-10-14 09:30:28','2025-10-14 09:30:28'),(19,'Service disconnection','2025-10-14 09:30:28','2025-10-14 09:30:28'),(20,'Identity verification','2025-10-14 09:30:28','2025-10-14 09:30:28');
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service disconnection`
--

DROP TABLE IF EXISTS `service disconnection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service disconnection` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service disconnection`
--

LOCK TABLES `service disconnection` WRITE;
/*!40000 ALTER TABLE `service disconnection` DISABLE KEYS */;
/*!40000 ALTER TABLE `service disconnection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_provider`
--

DROP TABLE IF EXISTS `service_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_provider` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `service_id` int unsigned NOT NULL,
  `officerID` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`officerID`),
  KEY `fk_service_provider_service` (`service_id`),
  CONSTRAINT `fk_service_provider_service` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_provider`
--

LOCK TABLES `service_provider` WRITE;
/*!40000 ALTER TABLE `service_provider` DISABLE KEYS */;
INSERT INTO `service_provider` VALUES (37,'Rajiv Kumar',1,'SP001','scrypt:32768:8:1$Vt8hN2A8Tt2JP1b9$405817b5265fa053cd240a49ec01fa006f258bfd9aa39c1ab78c55237cc9188f07498337a89a15dbaadcf113990bc45acdb8402555c3dd3198569b22cb260277','2025-09-26 12:24:36','2025-10-13 18:11:00'),(39,'Anjali Sharma',2,'SP002','scrypt:32768:8:1$ISYhCd66iRejJRSB$bc278a87a1102b655e731612a21e76637c3dd64daf23fe6183a45c09128c4bc57e8bb33c5079f469a7132557f0bd6eb682e193c042053e718cea1b38048ab690','2025-09-26 12:24:36','2025-10-11 08:12:31'),(41,'Suresh Gupta',3,'SP003','scrypt:32768:8:1$PkjKPq3KcN9r4w7I$b232694560ef8649cd702abd46cfe9af83d981a7e5a4ebabd8048c750cf90502a9df1fd3e89bb72ae1741718ea95098b7c11b68caa0f8e6fc0f12340df0b1cfa','2025-09-26 12:24:36','2025-10-12 06:09:35'),(51,'Rakesh Patel ',15,'SP004','scrypt:32768:8:1$Yax2FjkScikK2skL$3f24ae98ed2cbb05d623f070f572563e552649c166cb4c5ebef8ddc0818750f72d90baa115bf3201c29b2119cc8c317274df53f9914de3aaae7d9fce6a1f773e','2025-10-14 09:40:34','2025-10-14 09:40:34'),(52,'Rahul Patel ',16,'SP005','scrypt:32768:8:1$Ybf8IrUXFo5AN7DY$55ce472e8b985f4af5ae2709e01fff81c80e84d98f646aff9f768f22f0e895547f63361ebbdd4b2436afb5d38524e5d6668d84c804ad1805c2193123c3af18cf','2025-10-14 09:40:57','2025-10-14 09:40:57');
/*!40000 ALTER TABLE `service_provider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `position` tinyint unsigned NOT NULL,
  `token_id` int unsigned NOT NULL,
  `ETR` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token` (`token_id`),
  CONSTRAINT `fk_ticket_token` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  `customer_id` int unsigned NOT NULL,
  `type` enum('appointment','1','2','3') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_id` (`customer_id`),
  CONSTRAINT `fk_token_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
INSERT INTO `token` VALUES (34,'A00',34,'2','2025-10-13 18:09:38','2025-10-13 18:09:38'),(36,'A02',36,'3','2025-10-13 18:10:38','2025-10-13 18:17:13'),(41,'A05',41,'2','2025-10-14 02:06:01','2025-10-14 02:06:01'),(44,'A08',44,'1','2025-10-14 02:07:50','2025-10-14 02:07:50'),(46,'A10',46,'2','2025-10-14 02:21:46','2025-10-14 02:21:46'),(47,'A11',47,'2','2025-10-14 02:25:06','2025-10-14 02:25:06'),(48,'A12',48,'2','2025-10-14 02:29:29','2025-10-14 06:54:13'),(49,'A13',49,'2','2025-10-14 02:29:40','2025-10-14 02:29:40'),(51,'A15',51,'3','2025-10-14 02:33:56','2025-10-14 02:33:56'),(52,'A16',52,'3','2025-10-14 02:37:55','2025-10-14 02:37:55'),(53,'A17',53,'1','2025-10-14 06:42:38','2025-10-14 06:42:38'),(54,'A18',54,'3','2025-10-14 06:44:12','2025-10-14 06:44:12'),(55,'A19',55,'1','2025-10-14 06:45:04','2025-10-14 06:45:04'),(56,'A20',56,'appointment','2025-10-14 06:52:47','2025-10-14 06:54:29'),(57,'A21-Billing',57,'3','2025-10-14 07:46:58','2025-10-14 08:11:17'),(58,'A22-Billing',58,'1','2025-10-14 09:07:02','2025-10-14 09:07:02'),(59,'A23-Complaint',59,'2','2025-10-14 09:12:32','2025-10-14 09:12:32'),(60,'A24-Complaint',60,'2','2025-10-14 09:15:00','2025-10-14 09:15:00'),(61,'A25-Billing',61,'1','2025-10-14 09:20:55','2025-10-14 09:20:55'),(62,'A26-Billing',64,'1','2025-10-14 09:31:29','2025-10-14 09:31:29'),(63,'A27-Billing',65,'1','2025-10-14 09:39:47','2025-10-14 09:39:47'),(64,'A28-Billing',66,'1','2025-10-14 09:41:00','2025-10-14 09:41:00'),(65,'A29-Billing',67,'1','2025-10-14 09:41:48','2025-10-14 09:41:48');
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-15 16:55:29
