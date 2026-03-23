-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2026 at 11:01 AM
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
-- Table structure for table `author`
--

CREATE TABLE `author` (
  `Author_Id` char(5) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Bio` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `author`
--

INSERT INTO `author` (`Author_Id`, `Name`, `Bio`) VALUES
('Au001', 'Ashok Ferrey', 'Contemporary Sri Lankan novelist known for humorous and insightful storytelling. His works often explore modern Sri Lankan society and culture.'),
('Au002', 'Carl Muller', 'A well-known Sri Lankan author recognized for his novels depicting Burgher life and multicultural aspects of Sri Lanka.'),
('Au003', 'Michael Ondaatje', 'Internationally acclaimed author born in Sri Lanka, best known for The English Patient, blending history, poetry, and fiction.'),
('Au004', 'Saman Wickramarachchi', 'A contemporary Sri Lankan writer contributing to Sinhala literature with novels and short stories reflecting social themes.'),
('Au005', 'Chitra Fernando', 'Sri Lankan writer and academic known for contributions to English literature and linguistic studies.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `author`
--
ALTER TABLE `author`
  ADD PRIMARY KEY (`Author_Id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
