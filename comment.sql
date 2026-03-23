-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2026 at 11:33 AM
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
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `Article_id` char(5) NOT NULL,
  `User_id` char(5) NOT NULL,
  `Comment_id` varchar(10) NOT NULL,
  `Content` text NOT NULL,
  `Comment_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`Article_id`, `User_id`, `Comment_id`, `Content`, `Comment_date`) VALUES
('A001', 'U001', 'C001', 'Very informative article about the economy.', '2025-01-11'),
('A001', 'U002', 'C002', 'Good explanation of current challenges.', '2025-01-12'),
('A002', 'U003', 'C003', 'Nice overview of modern literature trends.', '2025-02-16'),
('A002', 'U004', 'C004', 'Helpful insights for students.', '2025-02-17'),
('A003', 'U005', 'C005', 'Well explained cultural diversity.', '2025-03-06'),
('A003', 'U006', 'C006', 'This article reflects real Sri Lankan society.', '2025-03-07'),
('A004', 'U007', 'C007', 'Important discussion on journalism.', '2025-03-21'),
('A005', 'U008', 'C008', 'Great summary of literary contributions.', '2025-04-03'),
('A006', 'U009', 'C009', 'Language and identity topic is very relevant.', '2025-04-19'),
('A010', 'U010', 'C010', 'Investigative journalism is crucial for truth.', '2025-06-21');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`Article_id`,`User_id`,`Comment_id`),
  ADD KEY `User_id` (`User_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`Article_id`) REFERENCES `article` (`Article_id`),
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`User_id`) REFERENCES `user` (`User_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
