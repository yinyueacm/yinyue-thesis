-- MySQL dump 10.13  Distrib 5.5.53, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: djdb
-- ------------------------------------------------------
-- Server version	5.5.53-0ubuntu0.14.04.1

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
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'/reuse','SR-CTF');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reuse_category`
--

DROP TABLE IF EXISTS `reuse_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reuse_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `typename` varchar(100) NOT NULL,
  `ctype_id` int(11) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reuse_category_961f60d2` (`ctype_id`),
  CONSTRAINT `reuse_category_ctype_id_35ad0133_fk_reuse_type_id` FOREIGN KEY (`ctype_id`) REFERENCES `reuse_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `reuse_ctf_info`
--

DROP TABLE IF EXISTS `reuse_ctf_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reuse_ctf_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `level` int(11) NOT NULL,
  `status` varchar(10) NOT NULL,
  `author` varchar(50) NOT NULL,
  `src_path` varchar(200) NOT NULL,
  `gen_path` varchar(200) NOT NULL,
  `config_path` varchar(200) NOT NULL,
  `desc` longtext NOT NULL,
  `cat_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reuse_ctf_info_cat_id_9ce03ec9_fk_reuse_category_id` (`cat_id`),
  CONSTRAINT `reuse_ctf_info_cat_id_9ce03ec9_fk_reuse_category_id` FOREIGN KEY (`cat_id`) REFERENCES `reuse_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `reuse_ctf_tag`
--

DROP TABLE IF EXISTS `reuse_ctf_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reuse_ctf_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ctf_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reuse_ctf_tag_ctf_id_149eceab_fk_reuse_ctf_info_id` (`ctf_id`),
  KEY `reuse_ctf_tag_76f094bc` (`tag_id`),
  CONSTRAINT `reuse_ctf_tag_ctf_id_149eceab_fk_reuse_ctf_info_id` FOREIGN KEY (`ctf_id`) REFERENCES `reuse_ctf_info` (`id`),
  CONSTRAINT `reuse_ctf_tag_tag_id_4179d392_fk_reuse_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `reuse_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reuse_ctf_tag`
--

LOCK TABLES `reuse_ctf_tag` WRITE;
/*!40000 ALTER TABLE `reuse_ctf_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `reuse_ctf_tag` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `reuse_tag`
--

DROP TABLE IF EXISTS `reuse_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reuse_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reuse_tag`
--

LOCK TABLES `reuse_tag` WRITE;
/*!40000 ALTER TABLE `reuse_tag` DISABLE KEYS */;
INSERT INTO `reuse_tag` VALUES (1,'Linux',''),(2,'Heap',''),(3,'glibc-2.23 malloc',''),(4,'x86',''),(5,'x86-64',''),(6,'Stack','TBD'),(7,'No Canary','no'),(8,'Canary','TBD'),(9,'Buffer Overflow','TBD');
/*!40000 ALTER TABLE `reuse_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reuse_type`
--

DROP TABLE IF EXISTS `reuse_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reuse_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reuse_type`
--

LOCK TABLES `reuse_type` WRITE;
/*!40000 ALTER TABLE `reuse_type` DISABLE KEYS */;
INSERT INTO `reuse_type` VALUES (1,'Pwn','binary exploitation'),(2,'Web',''),(3,'Reverse','');
/*!40000 ALTER TABLE `reuse_type` ENABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-07 15:05:36
