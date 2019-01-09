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
-- Table structure for table `reuse_cat_tag`
--

DROP TABLE IF EXISTS `reuse_cat_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reuse_cat_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reuse_cat_tag_05e7bb57` (`cat_id`),
  KEY `reuse_cat_tag_76f094bc` (`tag_id`),
  CONSTRAINT `reuse_cat_tag_cat_id_98a9035e_fk_reuse_category_id` FOREIGN KEY (`cat_id`) REFERENCES `reuse_category` (`id`),
  CONSTRAINT `reuse_cat_tag_tag_id_fd9b7ebd_fk_reuse_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `reuse_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reuse_cat_tag`
--

LOCK TABLES `reuse_cat_tag` WRITE;
/*!40000 ALTER TABLE `reuse_cat_tag` DISABLE KEYS */;
INSERT INTO `reuse_cat_tag` VALUES (1,1,1),(2,1,2),(3,1,3),(4,2,6),(5,2,1),(6,2,7),(7,2,9);
/*!40000 ALTER TABLE `reuse_cat_tag` ENABLE KEYS */;
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
-- Dumping data for table `reuse_category`
--

LOCK TABLES `reuse_category` WRITE;
/*!40000 ALTER TABLE `reuse_category` DISABLE KEYS */;
INSERT INTO `reuse_category` VALUES (1,'unlinkMe','Heap:Double Free',1,'<li>In this lab, students can get first-hand experience on exploiting heap-based vulnerability.<br>\r\n<li>In a series of stepwise challenges, students can understand how the heap is managed by glibc malloc and exploit the unlink() function after figuring out \"double free\" vulnerbilities.'),(2,'ropeman','Stack:Buffer Overflow+ROP',1,'<li>In this lab, students can get first-hand experience on exploiting buffer-overflow vulnerability with ROP techniques.<br><li>In a series of stepwise challenges, students will learn different scanerios after exploiting a stack overflow vulnerbility.'),(4,'basic','Basic Reverse',3,'Test basic reverse'),(5,'Format_String','Format_String',1,'TBD'),(7,'Sql_injection','Web:SQL',2,'<li>SQL-Injection is one of the top attacks for web applications.<br>\r\n<li>In this lab, students can get experience on exploiting SQL-Injection vulnerability.<br>\r\n<li>In a series of stepwise challenges, student will learn different SQL-Injection techniques. Useful skills for web analysis are also helpful.<br>\r\n<li>Try find out the vulnerabilities in the challenge website and make your evil inputs.'),(8,'web_basic','Web:Basic',2,'Enjoy the basic web challenges requiring different web analysis skills.');
/*!40000 ALTER TABLE `reuse_category` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `reuse_ctf_info`
--

LOCK TABLES `reuse_ctf_info` WRITE;
/*!40000 ALTER TABLE `reuse_ctf_info` DISABLE KEYS */;
INSERT INTO `reuse_ctf_info` VALUES (1,'unlink_me',1,'0','1','/ctfs/unlinkMe/unlink_me/for_guest/','/ctfs/unlinkMe/unlink_me/generate.sh','/ctfs/unlinkMe/unlink_me/conf.json','\"Lie to the glibc and pass the security checking\"<br>\r\nThere is a double free vulnerbility in the challenge program. However, the program will normally crashed by detecting the double free issue or data corruption.',1),(2,'use_after_unlink',2,'0','1','/ctfs/unlinkMe/use_after_unlink/for_guest/','/ctfs/unlinkMe/use_after_unlink/generate.sh','/ctfs/unlinkMe/use_after_unlink/conf.json','\"Use the unlink() to build your arms\"<br>\r\nAgain, pass the glibc checking to call the unlink(). See how you can take advantage of the program after a fake unlink() happened.',1),(3,'reuse_stack',0,'0','1','/ctfs/reuse_buffer_overflow/for_guest/','/ctfs/reuse_buffer_overflow/generate.sh','/ctfs/reuse_buffer_overflow/conf.json','A demo challenge on our reusable work on stack buffer overflow.<br>\r\n Try find the vulnerbility and call the help function provided in the program to launch a shell. <br>Also a tutorial for how to use pwntools,',2),(5,'ropeman',1,'1','1','/ctfs/ropeman/1/for_guest/','/ctfs/ropeman/1/generate.sh','/ctfs/ropeman/1/conf.json','\"Rewrite the target value\"<br>Use buffer overflow to rewrite value of function variables.',2),(6,'ropeman',2,'1','1','/ctfs/ropeman/2/for_guest/','/ctfs/ropeman/2/generate.sh','/ctfs/ropeman/2/conf.json','\"Rewrite the stack return address\"<br>A traditional method in Stack Overflow is to jump to a program unintended place by rewriting the stack return address.',2),(7,'ropeman',3,'1','1','/ctfs/ropeman/3/for_guest/','/ctfs/ropeman/3/generate.sh','/ctfs/ropeman/3/conf.json','\"Rewrite the return address and pass arbitrary arguments\"<br>Set up your stack to call a help function and provide a proper argument.',2),(8,'ropeman',4,'0','1','/ctfs/ropeman/4/for_guest/','/ctfs/ropeman/4/generate.sh','/ctfs/ropeman/4/conf.json','\"Chain more than one functions\" <br>With simple gadgets like \"pop-ret\", you can build a simple chain to call a second function right after running the first function.',2),(9,'ropeman',5,'0','1','/ctfs/ropeman/5/for_guest/','/ctfs/ropeman/5/generate.sh','/ctfs/ropeman/5/conf.json','\"Build a ROP gadget chain\" <br>With ROP, you can do far more powerful things than calling a single function.<br>(Hint: Tools like \"ROPgadget\" can help you find a useful gadget chain. <br>The environment we provided has ROPgadget installed.)',2),(10,'ropeman',6,'0','1','/ctfs/ropeman/6/for_guest/','/ctfs/ropeman/6/generate.sh','/ctfs/ropeman/6/conf.json','\"Combine the skills above\" <br>Test your skills with a real iCTF challenge! Find anything that may help you in the program.',2),(11,'basic0',0,'0','1','/reverse/binary/0.pdf','not_a_gen','/ctfs/reverse/binary/conf0.json','Don\'t get fooled by the file name.',4),(12,'fs_guess',1,'0','1','/ctfs/format_string/fs1/for_guest/','/ctfs/format_string/fs1/generate.sh','/ctfs/format_string/fs1/conf.json','Guess the number.',5),(13,'fs_format_write',2,'0','1','/ctfs/format_string/fs2/for_guest/','/ctfs/format_string/fs2/generate.sh','/ctfs/format_string/fs2/conf.json','Try use format string skills to write a value into a target variable.',5),(14,'fs_format_write(2)',3,'0','1','/ctfs/format_string/fs3/for_guest/','/ctfs/format_string/fs3/generate.sh','/ctfs/format_string/fs3/conf.json','Again, try to write a value into the target variable, but we added a little input checking this time.',5),(15,'SQL1-top secrets',1,'0','1','/ctfs/www/sql1/for_guest/','/ctfs/www/sql1/generate.sh','/ctfs/www/sql1/conf.json','The secret is stored in the website, see if you can find it.',7),(16,'SQL2-top secrets(2)',2,'0','1','/ctfs/www/sql2/for_guest/','/ctfs/www/sql2/generate.sh','/ctfs/www/sql2/conf.json','Again, there is secret in the website, we have secured the site, advanced skills are required.',7),(17,'basic1',1,'0','1','/reverse/binary/challenge1.1','not_a_gen','/ctfs/reverse/binary/conf1.json','Find the key inside the program.<br>\r\n(The flag starts with \"Key=\")',4),(18,'SQL3-top secrets(3)',3,'0','1','/ctfs/www/sql3/for_guest/','/ctfs/www/sql3/generate.sh','/ctfs/www/sql3/conf.json','Once again, we improved the website. See if you can find a way to login again.',7),(19,'webbasic1',1,'0','1','/ctfs/www/web1/for_guest/','/ctfs/www/web1/generate.sh','/ctfs/www/web1/conf.json','Get the flag!',8),(20,'webbasic2',2,'0','1','/ctfs/www/web2/for_guest/','/ctfs/www/web2/generate.sh','/ctfs/www/web2/conf.json','Get the flag!',8),(21,'basic2',2,'0','1','/reverse/binary/challenge1.2','not_a_gen','/ctfs/reverse/binary/conf2.json','Find the key inside the program.<br>\r\n(The flag starts with \"Key=\")',4),(22,'basic3',3,'0','1','/reverse/binary/challenge1.3','not_a_gen','/ctfs/reverse/binary/conf3.json','Find the key inside the program.<br>\r\n(The flag starts with \"Key=\")',4),(23,'webbasic3',3,'0','1','/ctfs/www/web3/for_guest/','/ctfs/www/web3/generate.sh','/ctfs/www/web3/conf.json','Get the flag!',8),(24,'webbasic4',4,'0','1','/ctfs/www/web4/for_guest/','/ctfs/www/web4/generate.sh','/ctfs/www/web4/conf.json','Get the flag!<br>\r\nEnjoy the cookie!',8);
/*!40000 ALTER TABLE `reuse_ctf_info` ENABLE KEYS */;
UNLOCK TABLES;

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
