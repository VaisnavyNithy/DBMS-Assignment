-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2026 at 06:40 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uomnewsportaldb`
--

-- --------------------------------------------------------

--
-- Table structure for table `article_category`
--

CREATE TABLE `article_category` (
  `Article_ID` char(5) NOT NULL,
  `Category_ID` char(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `article_category`
--

INSERT INTO `article_category` (`Article_ID`, `Category_ID`) VALUES
('A001', 'C001'),
('A002', 'C002'),
('A003', 'C003'),
('A004', 'C004'),
('A005', 'C002'),
('A006', 'C003'),
('A007', 'C009'),
('A008', 'C007'),
('A009', 'C008'),
('A010', 'C004'),
('A011', 'C006'),
('A012', 'C005'),
('A013', 'C003'),
('A014', 'C003'),
('A015', 'C008'),
('A016', 'C003'),
('A017', 'C005'),
('A018', 'C007'),
('A019', 'C008'),
('A020', 'C010');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `article_category`
--
ALTER TABLE `article_category`
  ADD PRIMARY KEY (`Article_ID`,`Category_ID`),
  ADD KEY `fk_ac_category` (`Category_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `article_category`
--
ALTER TABLE `article_category`
  ADD CONSTRAINT `fk_ac_article` FOREIGN KEY (`Article_ID`) REFERENCES `article` (`Article_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_ac_category` FOREIGN KEY (`Category_ID`) REFERENCES `category` (`Category_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
