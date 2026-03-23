-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2026 at 06:41 PM
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
-- Table structure for table `article_tag`
--

CREATE TABLE `article_tag` (
  `ARTICLE_ID` char(5) NOT NULL,
  `TAG_ID` char(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `article_tag`
--

INSERT INTO `article_tag` (`ARTICLE_ID`, `TAG_ID`) VALUES
('A001', 'T001'),
('A001', 'T002'),
('A002', 'T003'),
('A002', 'T004'),
('A003', 'T005'),
('A003', 'T014'),
('A004', 'T006'),
('A004', 'T013'),
('A005', 'T003'),
('A005', 'T016'),
('A006', 'T005'),
('A006', 'T014'),
('A007', 'T010'),
('A008', 'T009'),
('A008', 'T019'),
('A009', 'T001'),
('A009', 'T011'),
('A010', 'T006'),
('A010', 'T013'),
('A011', 'T008'),
('A011', 'T018'),
('A012', 'T007'),
('A012', 'T020'),
('A013', 'T005'),
('A013', 'T012'),
('A014', 'T005'),
('A014', 'T016'),
('A015', 'T002'),
('A015', 'T011'),
('A016', 'T015'),
('A016', 'T020'),
('A017', 'T005'),
('A017', 'T007'),
('A018', 'T009'),
('A018', 'T019'),
('A019', 'T011'),
('A019', 'T012'),
('A020', 'T015'),
('A020', 'T017');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `article_tag`
--
ALTER TABLE `article_tag`
  ADD PRIMARY KEY (`ARTICLE_ID`,`TAG_ID`),
  ADD KEY `fk_at_tag` (`TAG_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `article_tag`
--
ALTER TABLE `article_tag`
  ADD CONSTRAINT `fk_at_article` FOREIGN KEY (`ARTICLE_ID`) REFERENCES `article` (`Article_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_at_tag` FOREIGN KEY (`TAG_ID`) REFERENCES `tag` (`Tag_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
