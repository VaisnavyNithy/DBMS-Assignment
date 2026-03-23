-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2026 at 11:38 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbms_programming`
--

-- --------------------------------------------------------

--
-- Table structure for table `article_view`
--

CREATE TABLE `article_view` (
  `Article_id` char(5) NOT NULL,
  `User_id` char(5) NOT NULL,
  `View_Id` char(5) NOT NULL,
  `Viewdate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `article_view`
--

INSERT INTO `article_view` (`Article_id`, `User_id`, `View_Id`, `Viewdate`) VALUES
('A001', 'U001', 'V001', '2025-01-10'),
('A001', 'U002', 'V002', '2025-01-10'),
('A002', 'U003', 'V003', '2025-02-15'),
('A002', 'U004', 'V004', '2025-02-16'),
('A003', 'U005', 'V005', '2025-03-05'),
('A003', 'U006', 'V006', '2025-03-06'),
('A004', 'U007', 'V007', '2025-03-20'),
('A005', 'U008', 'V008', '2025-04-02'),
('A006', 'U009', 'V009', '2025-04-18'),
('A010', 'U010', 'V010', '2025-06-20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `article_view`
--
ALTER TABLE `article_view`
  ADD PRIMARY KEY (`Article_id`,`User_id`,`View_Id`),
  ADD KEY `User_id` (`User_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `article_view`
--
ALTER TABLE `article_view`
  ADD CONSTRAINT `article_view_ibfk_1` FOREIGN KEY (`Article_id`) REFERENCES `article` (`Article_id`),
  ADD CONSTRAINT `article_view_ibfk_2` FOREIGN KEY (`User_id`) REFERENCES `user` (`User_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
