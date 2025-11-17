-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: ql_vatlieuxaydung
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chitiethoadon`
--

DROP TABLE IF EXISTS `chitiethoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chitiethoadon` (
  `mahd` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mavl` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `soluong` int DEFAULT '1',
  `dongia` decimal(15,2) NOT NULL,
  `giamgia` decimal(15,2) DEFAULT '0.00',
  `thanhtien` decimal(15,2) NOT NULL,
  PRIMARY KEY (`mahd`,`mavl`),
  KEY `fk_CTHD_VATLIEU` (`mavl`),
  CONSTRAINT `fk_CTHD_HOADON` FOREIGN KEY (`mahd`) REFERENCES `hoadon` (`mahd`) ON DELETE CASCADE,
  CONSTRAINT `fk_CTHD_VATLIEU` FOREIGN KEY (`mavl`) REFERENCES `vatlieu` (`mavl`),
  CONSTRAINT `chitiethoadon_chk_1` CHECK ((`soluong` > 0)),
  CONSTRAINT `chitiethoadon_chk_2` CHECK ((`dongia` >= 0)),
  CONSTRAINT `chitiethoadon_chk_3` CHECK ((`giamgia` >= 0)),
  CONSTRAINT `chitiethoadon_chk_4` CHECK ((`thanhtien` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chitiethoadon`
--

LOCK TABLES `chitiethoadon` WRITE;
/*!40000 ALTER TABLE `chitiethoadon` DISABLE KEYS */;
INSERT INTO `chitiethoadon` VALUES ('a','a',12,12.00,12.00,132.00);
/*!40000 ALTER TABLE `chitiethoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoadon`
--

DROP TABLE IF EXISTS `hoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoadon` (
  `mahd` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `manv` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `makh` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ngaylap` datetime DEFAULT CURRENT_TIMESTAMP,
  `tongtien` decimal(15,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`mahd`),
  KEY `fk_HOADON_KHACHHANG` (`makh`),
  KEY `fk_HOADON_NHANVIEN` (`manv`),
  CONSTRAINT `fk_HOADON_KHACHHANG` FOREIGN KEY (`makh`) REFERENCES `khachhang` (`makh`),
  CONSTRAINT `fk_HOADON_NHANVIEN` FOREIGN KEY (`manv`) REFERENCES `nhanvien` (`manv`),
  CONSTRAINT `hoadon_chk_1` CHECK ((`tongtien` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoadon`
--

LOCK TABLES `hoadon` WRITE;
/*!40000 ALTER TABLE `hoadon` DISABLE KEYS */;
INSERT INTO `hoadon` VALUES ('a','a','a','2025-11-15 17:02:08',132.00);
/*!40000 ALTER TABLE `hoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khachhang`
--

DROP TABLE IF EXISTS `khachhang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khachhang` (
  `makh` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tenkh` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `diachi` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `sdt` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`makh`),
  CONSTRAINT `khachhang_chk_1` CHECK (regexp_like(`sdt`,_utf8mb4'^0[0-9]{9}$'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khachhang`
--

LOCK TABLES `khachhang` WRITE;
/*!40000 ALTER TABLE `khachhang` DISABLE KEYS */;
INSERT INTO `khachhang` VALUES ('a','a','a','0123456789');
/*!40000 ALTER TABLE `khachhang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhanvien`
--

DROP TABLE IF EXISTS `nhanvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhanvien` (
  `manv` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tennv` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `gioitinh` enum('nam','nu') COLLATE utf8mb4_unicode_ci DEFAULT 'nam',
  `chucvu` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `sdt` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `diachi` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`manv`),
  CONSTRAINT `nhanvien_chk_1` CHECK (regexp_like(`sdt`,_utf8mb4'^0[0-9]{9}$'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhanvien`
--

LOCK TABLES `nhanvien` WRITE;
/*!40000 ALTER TABLE `nhanvien` DISABLE KEYS */;
INSERT INTO `nhanvien` VALUES ('a','a','nam','a','0123456789','a');
/*!40000 ALTER TABLE `nhanvien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vatlieu`
--

DROP TABLE IF EXISTS `vatlieu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vatlieu` (
  `mavl` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tenvl` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `loaivl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `donvitinh` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `dongia` decimal(15,2) NOT NULL,
  `soluong` int DEFAULT '0',
  PRIMARY KEY (`mavl`),
  CONSTRAINT `vatlieu_chk_1` CHECK ((`dongia` >= 0)),
  CONSTRAINT `vatlieu_chk_2` CHECK ((`soluong` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vatlieu`
--

LOCK TABLES `vatlieu` WRITE;
/*!40000 ALTER TABLE `vatlieu` DISABLE KEYS */;
INSERT INTO `vatlieu` VALUES ('a','a','a','a',12.00,2),('b','a','a','a',12.00,2);
/*!40000 ALTER TABLE `vatlieu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-17 14:10:12
