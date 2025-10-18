-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: QMS
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

--
-- Table structure for table `Billing`
--

DROP TABLE IF EXISTS `Billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Billing` (
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
-- Dumping data for table `Billing`
--

LOCK TABLES `Billing` WRITE;
/*!40000 ALTER TABLE `Billing` DISABLE KEYS */;
/*!40000 ALTER TABLE `Billing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Complaint`
--

DROP TABLE IF EXISTS `Complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Complaint` (
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
-- Dumping data for table `Complaint`
--

LOCK TABLES `Complaint` WRITE;
/*!40000 ALTER TABLE `Complaint` DISABLE KEYS */;
/*!40000 ALTER TABLE `Complaint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `KYC`
--

DROP TABLE IF EXISTS `KYC`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `KYC` (
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
-- Dumping data for table `KYC`
--

LOCK TABLES `KYC` WRITE;
/*!40000 ALTER TABLE `KYC` DISABLE KEYS */;
/*!40000 ALTER TABLE `KYC` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Revoked`
--

DROP TABLE IF EXISTS `Revoked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Revoked` (
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
-- Dumping data for table `Revoked`
--

LOCK TABLES `Revoked` WRITE;
/*!40000 ALTER TABLE `Revoked` DISABLE KEYS */;
/*!40000 ALTER TABLE `Revoked` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `admin` VALUES (1,'admin','scrypt:32768:8:1$Jy3wWgY8PXVVCJOQ$770572106f8cfb72fc01f8dd8effdd3edb3f8369b73350b3dc2cd9d120fc1cebf4b5a6ba0365b21db8e4f9fad5803d40157eb6183caedc85bd2af0dc9cd39240',0.5,23.12446,72.54559,'2025-10-18 14:05:08','2025-10-11 13:13:13');
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
INSERT INTO `appointment` VALUES (1,'09:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-18 14:23:05'),(3,'09:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-18 14:23:05'),(5,'10:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-18 14:23:05'),(7,'10:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-18 14:23:05'),(9,'11:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-18 14:23:05'),(11,'11:30:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(13,'12:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(15,'12:30:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(17,'13:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-18 14:23:05'),(19,'13:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-18 13:46:25'),(21,'14:00:00',0,NULL,'2025-09-28 10:59:04','2025-10-11 06:55:40'),(23,'14:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-11 06:55:40'),(25,'15:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(27,'15:30:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(29,'16:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04'),(31,'16:30:00',0,NULL,'2025-09-28 10:59:04','2025-10-13 17:53:09'),(33,'17:00:00',0,NULL,'2025-09-28 10:59:04','2025-09-28 10:59:04');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (5,'Peter Jones',NULL,'peter.jones@example.com',1,5,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(7,'Mary Johnson',NULL,'mary.johnson@example.com',2,7,'2025-10-18 10:53:03','2025-10-18 13:58:49'),(9,'David Williams',NULL,'david.williams@example.com',1,9,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(11,'Susan Brown',NULL,'susan.brown@example.com',1,11,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(13,'Michael Davis',NULL,'michael.davis@example.com',1,13,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(15,'Linda Miller',NULL,'linda.miller@example.com',1,15,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(17,'Robert Wilson',NULL,'robert.wilson@example.com',1,17,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(19,'Patricia Moore',NULL,'patricia.moore@example.com',1,19,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(21,'James Taylor',NULL,'james.taylor@example.com',2,31,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(23,'Barbara Anderson',NULL,'barbara.anderson@example.com',2,33,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(25,'Thomas Hernandez',NULL,'thomas.hernandez@example.com',2,35,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(27,'Elizabeth Martin',NULL,'elizabeth.martin@example.com',2,37,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(29,'Christopher Garcia',NULL,'christopher.garcia@example.com',2,39,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(31,'Jessica Rodriguez',NULL,'jessica.rodriguez@example.com',2,41,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(33,'Daniel Martinez',NULL,'daniel.martinez@example.com',2,43,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(35,'Sarah Robinson',NULL,'sarah.robinson@example.com',2,45,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(37,'Matthew Clark',NULL,'matthew.clark@example.com',2,47,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(39,'Karen Lewis',NULL,'karen.lewis@example.com',2,49,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(41,'Paul Walker',NULL,'paul.walker@example.com',3,61,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(43,'Nancy Hall',NULL,'nancy.hall@example.com',3,63,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(45,'Mark Allen',NULL,'mark.allen@example.com',3,65,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(47,'Betty Young',NULL,'betty.young@example.com',3,67,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(49,'Steven King',NULL,'steven.king@example.com',3,69,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(51,'Donna Wright',NULL,'donna.wright@example.com',3,71,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(53,'Andrew Lopez',NULL,'andrew.lopez@example.com',3,73,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(55,'Sandra Hill',NULL,'sandra.hill@example.com',3,75,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(57,'Joshua Scott',NULL,'joshua.scott@example.com',3,77,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(59,'Cynthia Green',NULL,'cynthia.green@example.com',3,79,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(61,'Appointment User 1',NULL,'app1@example.com',NULL,91,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(63,'Appointment User 2',NULL,'app2@example.com',NULL,93,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(65,'Appointment User 3',NULL,'app3@example.com',NULL,95,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(67,'Appointment User 4',NULL,'app4@example.com',NULL,97,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(69,'Appointment User 5',NULL,'app5@example.com',NULL,99,'2025-10-18 10:53:03','2025-10-18 10:53:03'),(77,'Tirth',NULL,'tirthkavathiya@gmail.com',1,109,'2025-10-18 11:11:28','2025-10-18 11:11:28'),(85,'tirth','C4321','tirthkavathiya@gmail.com',1,115,'2025-10-18 13:47:37','2025-10-18 13:47:37'),(87,'tirth',NULL,'tirthkavathiya@gmail.com',2,117,'2025-10-18 13:48:48','2025-10-18 13:48:48'),(89,'sadsa',NULL,'tirthkavathiya@gmail.com',2,119,'2025-10-18 13:55:19','2025-10-18 13:55:19');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `otp_verification`
--

LOCK TABLES `otp_verification` WRITE;
/*!40000 ALTER TABLE `otp_verification` DISABLE KEYS */;
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
INSERT INTO `service` VALUES (0,'Revoked','2025-10-11 18:56:28','2025-10-11 19:00:39'),(1,'Billing','2025-09-26 12:17:13','2025-09-26 12:17:13'),(2,'Complaint','2025-09-26 12:17:13','2025-10-11 08:11:38'),(3,'KYC','2025-09-26 12:17:13','2025-10-11 08:11:38');
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
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
INSERT INTO `service_provider` VALUES (37,'Rajiv Kumar',1,'SP001','scrypt:32768:8:1$Vt8hN2A8Tt2JP1b9$405817b5265fa053cd240a49ec01fa006f258bfd9aa39c1ab78c55237cc9188f07498337a89a15dbaadcf113990bc45acdb8402555c3dd3198569b22cb260277','2025-09-26 12:24:36','2025-10-13 18:11:00'),(39,'Anjali Sharma',2,'SP002','scrypt:32768:8:1$ISYhCd66iRejJRSB$bc278a87a1102b655e731612a21e76637c3dd64daf23fe6183a45c09128c4bc57e8bb33c5079f469a7132557f0bd6eb682e193c042053e718cea1b38048ab690','2025-09-26 12:24:36','2025-10-11 08:12:31'),(41,'Suresh Gupta',2,'SP003','scrypt:32768:8:1$PkjKPq3KcN9r4w7I$b232694560ef8649cd702abd46cfe9af83d981a7e5a4ebabd8048c750cf90502a9df1fd3e89bb72ae1741718ea95098b7c11b68caa0f8e6fc0f12340df0b1cfa','2025-09-26 12:24:36','2025-10-18 14:13:51');
/*!40000 ALTER TABLE `service_provider` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-18 19:56:45
