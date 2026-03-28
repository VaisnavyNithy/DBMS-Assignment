-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2026 at 08:17 AM
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
-- Database: `uomnewsportaldbtest`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `User_id` char(5) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `DOB` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`User_id`, `Name`, `Email`, `DOB`) VALUES
('U001', 'Nimal Perera', 'nimalperera@gmail.com', '1982-05-12'),
('U002', 'Kavindi Silva', 'kavindisilva@yahoo.com', '1995-08-23'),
('U003', 'Ramesh Fernando', 'rameshfernando@hotmail.com', '1978-03-17'),
('U004', 'Hasini Jayawardena', 'hasinijaya@gmail.com', '2001-11-04'),
('U005', 'Tharindu Kumara', 'tharindukumara@gmail.com', '1992-07-29'),
('U006', 'Dilan Abeysekara', 'dilanabey@gmail.com', '1985-01-15'),
('U007', 'Isuri Nadeeshani', 'isuri34@gmail.com', '1996-09-08'),
('U008', 'Chamika Rathnayake', 'chamika87@gmail.com', '1974-12-31'),
('U009', 'Lakshan Perera', 'lakshan23@yahoo.com', '2003-06-20'),
('U010', 'Sanduni Fernando', 'sanduni12@gmail.com', '2005-02-14');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`User_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
