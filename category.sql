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
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `Category_id` char(5) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Description` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`Category_id`, `Name`, `Description`) VALUES
('C001', 'Economy', 'Articles related to economic trends, financial markets, and national economy.'),
('C002', 'Literature', 'Articles about modern literature, authors, and literary analysis.'),
('C003', 'Culture', 'Articles covering cultural diversity, festivals, and heritage.'),
('C004', 'Journalism', 'Articles discussing journalism, media ethics, and reporting.'),
('C005', 'Education', 'Articles on educational policies, reforms, and learning trends.'),
('C006', 'Technology', 'Articles on technology, AI, and digital innovations.'),
('C007', 'Environment', 'Articles on environmental protection, wildlife, and sustainability.'),
('C008', 'Business', 'Articles about startups, international business, and financial literacy.'),
('C009', 'Health', 'Articles on public health, campaigns, and awareness.'),
('C010', 'Arts', 'Articles about arts, cultural heritage, and creative initiatives.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`Category_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
