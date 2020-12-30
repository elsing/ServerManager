-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 195.201.95.187
-- Generation Time: Sep 29, 2018 at 09:11 PM
-- Server version: 5.7.21-0ubuntu0.16.04.1
-- PHP Version: 7.1.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `servermanager`
--

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE `status` (
  `statusID` int(200) NOT NULL,
  `userID` int(11) DEFAULT NULL,
  `serverID` int(11) DEFAULT NULL,
  `IP` varchar(20) DEFAULT NULL,
  `state` varchar(20) NOT NULL,
  `lastseen` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `status`
--

INSERT INTO `status` (`statusID`, `userID`, `serverID`, `IP`, `state`, `lastseen`) VALUES
(445260218, 337965876, 256759103, '10.10.10.5', 'Up', '29-09-2018 20:48:32'),
(538660300, 337965876, 223880131, '10.10.10.1', 'Up', '29-09-2018 20:48:30'),
(727043861, 337965876, 829023988, '10.10.10.223', 'Down', '29-09-2018 20:46:56');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`statusID`),
  ADD KEY `status_ibfk_1` (`userID`),
  ADD KEY `status_ibfk_2` (`serverID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `status`
--
ALTER TABLE `status`
  ADD CONSTRAINT `status_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE,
  ADD CONSTRAINT `status_ibfk_2` FOREIGN KEY (`serverID`) REFERENCES `devices` (`serverID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
