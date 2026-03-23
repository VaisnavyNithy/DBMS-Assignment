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
-- Table structure for table `article`
--

CREATE TABLE `article` (
  `Article_id` char(5) NOT NULL,
  `Title` varchar(200) NOT NULL,
  `Content` text NOT NULL,
  `Published_Date` date NOT NULL,
  `Author_id` char(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `article`
--

INSERT INTO `article` (`Article_id`, `Title`, `Content`, `Published_Date`, `Author_id`) VALUES
('A001', 'Economic Trends in 2025', 'An analysis of the key economic indicators shaping the national economy in 2025, including inflation, GDP growth, and market performance.', '2025-01-10', 'Au001'),
('A002', 'Modern Literature and Its Impact', 'A comprehensive review of contemporary literary works in Sri Lanka, highlighting emerging authors and cultural influences.', '2025-02-15', 'Au002'),
('A003', 'Cultural Diversity Across Sri Lanka', 'Examining the cultural, ethnic, and linguistic diversity of Sri Lanka and its impact on social cohesion.', '2025-03-05', 'Au003'),
('A004', 'Journalism Ethics in the Modern Era', 'Discussion on the role of ethical journalism in promoting transparency, accountability, and public trust.', '2025-03-20', 'Au004'),
('A005', 'Contributions of Sri Lankan Literature', 'An overview of significant literary contributions by Sri Lankan authors across genres and their influence on society.', '2025-04-02', 'Au005'),
('A006', 'Language and National Identity', 'Exploring the relationship between language policies and national identity, including implications for education and communication.', '2025-04-18', 'Au006'),
('A007', 'Public Health Awareness Initiatives', 'Assessment of recent health campaigns and strategies implemented to improve public health outcomes.', '2025-05-05', 'Au007'),
('A008', 'Environmental Protection Efforts', 'Review of government and community-led initiatives to reduce pollution and protect natural resources.', '2025-05-15', 'Au008'),
('A009', 'Startup Ecosystem in Sri Lanka', 'Analysis of the growth of startups, investment trends, and challenges facing emerging businesses.', '2025-06-01', 'Au009'),
('A010', 'Investigative Journalism: Role and Importance', 'Highlighting the critical role of investigative journalism in uncovering issues and fostering informed public discourse.', '2025-06-20', 'Au010'),
('A011', 'Advances in Technology and AI', 'An exploration of new technological innovations and artificial intelligence applications across industries.', '2025-06-25', 'Au001'),
('A012', 'Educational Reforms and Policy Updates', 'A detailed look at recent reforms in the education sector, focusing on curriculum development and accessibility.', '2025-07-05', 'Au002'),
('A013', 'Tourism Development Strategies', 'Analysis of tourism initiatives, emerging destinations, and their impact on the local economy.', '2025-07-15', 'Au003'),
('A014', 'Celebrating Cultural Festivals', 'An overview of traditional and contemporary cultural festivals across Sri Lanka, emphasizing community engagement.', '2025-07-25', 'Au004'),
('A015', 'Financial Literacy for Citizens', 'Guidelines and strategies for improving personal financial management and awareness among citizens.', '2025-08-05', 'Au005'),
('A016', 'Urban Development and Infrastructure', 'Evaluation of ongoing urban development projects and their implications for city planning and sustainability.', '2025-08-15', 'Au006'),
('A017', 'Trends in Online Learning', 'A study of digital education platforms and the evolving landscape of online learning opportunities.', '2025-08-25', 'Au007'),
('A018', 'Wildlife Conservation Projects', 'Insight into conservation programs aimed at protecting endangered species and promoting biodiversity.', '2025-09-05', 'Au008'),
('A019', 'International Business Expansion', 'Examination of local companies expanding overseas, including challenges and success stories.', '2025-09-15', 'Au009'),
('A020', 'Art and Cultural Heritage', 'Exploring the preservation of traditional arts and the promotion of cultural heritage through modern initiatives.', '2025-09-25', 'Au010');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`Article_id`),
  ADD KEY `fk_article_author` (`Author_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `article`
--
ALTER TABLE `article`
  ADD CONSTRAINT `fk_article_author` FOREIGN KEY (`Author_id`) REFERENCES `author` (`Author_Id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
