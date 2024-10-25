-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: argbroker
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `acciones`
--

DROP TABLE IF EXISTS `acciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acciones` (
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `precio_compra` decimal(10,2) DEFAULT NULL,
  `precio_venta` decimal(10,2) DEFAULT NULL,
  `cantidad_disponible` int DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acciones`
--

LOCK TABLES `acciones` WRITE;
/*!40000 ALTER TABLE `acciones` DISABLE KEYS */;
INSERT INTO `acciones` VALUES ('AAPL','Apple',300.00,320.00,1500),('DIS','The Walt Disney Co.',180.25,181.00,1000),('GOOGL','Google',1500.00,1550.00,300),('GOOGLE','google',56.80,57.20,1000),('KO','Coca-Cola Co.',56.80,57.20,1000),('MCD','McDonald\'s',200.00,210.00,1000),('NFLX','Netflix Inc.',590.70,595.00,1000),('NKE','Nike Inc.',156.50,157.20,1000),('pepino','pepe',56.80,57.20,1000),('SAMS','Samsung Electronics',78.50,79.00,1000);
/*!40000 ALTER TABLE `acciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cotizaciones`
--

DROP TABLE IF EXISTS `cotizaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cotizaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo_accion` varchar(10) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `codigo_accion` (`codigo_accion`),
  CONSTRAINT `cotizaciones_ibfk_1` FOREIGN KEY (`codigo_accion`) REFERENCES `acciones` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotizaciones`
--

LOCK TABLES `cotizaciones` WRITE;
/*!40000 ALTER TABLE `cotizaciones` DISABLE KEYS */;
INSERT INTO `cotizaciones` VALUES (1,'MCD',210.00,'2024-10-22 11:13:01'),(2,'AAPL',320.00,'2024-10-22 11:13:01'),(3,'GOOGL',1550.00,'2024-10-22 11:13:01'),(4,'AAPL',150.25,'2024-10-22 14:42:21');
/*!40000 ALTER TABLE `cotizaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inversores`
--

DROP TABLE IF EXISTS `inversores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inversores` (
  `cuit` varchar(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `saldo` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`cuit`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inversores`
--

LOCK TABLES `inversores` WRITE;
/*!40000 ALTER TABLE `inversores` DISABLE KEYS */;
INSERT INTO `inversores` VALUES ('20304050607','Juan','Perez','juan.perez@gmail.com','hashed_password',1000000.00),('30102030405','Maria','Lopez','maria.lopez@gmail.com','hashed_password',1000000.00);
/*!40000 ALTER TABLE `inversores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacciones`
--

DROP TABLE IF EXISTS `transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transacciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cuit` varchar(11) DEFAULT NULL,
  `codigo_accion` varchar(10) DEFAULT NULL,
  `tipo` enum('compra','venta') DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `total` decimal(15,2) DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `cuit` (`cuit`),
  KEY `codigo_accion` (`codigo_accion`),
  CONSTRAINT `transacciones_ibfk_1` FOREIGN KEY (`cuit`) REFERENCES `inversores` (`cuit`),
  CONSTRAINT `transacciones_ibfk_2` FOREIGN KEY (`codigo_accion`) REFERENCES `acciones` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacciones`
--

LOCK TABLES `transacciones` WRITE;
/*!40000 ALTER TABLE `transacciones` DISABLE KEYS */;
INSERT INTO `transacciones` VALUES (1,'20304050607','MCD','compra',10,200.00,2000.00,'2024-10-22 11:14:32'),(2,'30102030405','AAPL','compra',5,300.00,1500.00,'2024-10-22 11:14:32');
/*!40000 ALTER TABLE `transacciones` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-25 11:46:17
