-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 17, 2024 at 03:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `librarymanagementsystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `genre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `author`, `genre`) VALUES
(1, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction'),
(5, '22222', 'sss', 'gggg'),
(6, 'Fiction', 'Dystopian', 'Classic'),
(7, 't1', 'a1', 'g1'),
(8, 'To Kil', '1984', 'The Great Gatsby'),
(9, 'tt', 'aaa', 'gggg'),
(10, 'www', 'aaaaaaaaaaa', 'zzzzzz'),
(11, '111', '2223', '333'),
(12, 'aaa', 'sss', 'xxx'),
(13, 'asdfg', 'sdfgh', 'werty'),
(14, 'dfghj', 'xcvb', 'wert'),
(15, 'aaaaaaa', 'aaaaaaaa', 'aaaaaaaa'),
(16, 'qqq', 'www', 'aaa'),
(17, 'zzz', 'zzz', 'zzzz'),
(18, '1141414', '141414', '141414'),
(19, 'qqqqqqqqqqqq', 'qqqqqqqqqqq', 'qqqqqqqqq'),
(21, 'aaa', 'aaa', 'aaa'),
(22, 't1111', 'a1111', 'g1111'),
(23, 't1111', 'a1111', 'g1111'),
(24, 't1111', 'a1111', 'g1111'),
(25, 't1111', 'a1111', 'g1111'),
(26, 't1111', 'a1111', 'g1111'),
(27, 't1111', 'a1111', 'g1111'),
(31, 'ttt1', 'aaa11', 'ggg11');

-- --------------------------------------------------------

--
-- Table structure for table `borrowings`
--

CREATE TABLE `borrowings` (
  `id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `borrow_date` text NOT NULL,
  `return_date` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `borrowings`
--

INSERT INTO `borrowings` (`id`, `member_id`, `book_id`, `borrow_date`, `return_date`) VALUES
(6, 2, 1, '1/1/2000', '1/2/2000'),
(8, 1, 1, '1/1/2000', '1/2/2000'),
(14, 2, 5, '1/1/200', '1/2/2000'),
(15, 2, 5, '1/1/200', '1/2/2000'),
(16, 2, 10, '6/7/2003', '6/8/2003'),
(17, 2, 10, '6/7/2003', '6/8/2003'),
(18, 2, 10, '6/7/2003', '6/8/2003');

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`id`, `name`, `phone`) VALUES
(1, 'a1111', '2323232'),
(2, 'a14', '012345'),
(3, 'nenen', '11111'),
(4, 'www', '11111111'),
(5, 'Moraa', '012345'),
(6, 'Moraa', '012345');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `borrowings`
--
ALTER TABLE `borrowings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `member_id` (`member_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `borrowings`
--
ALTER TABLE `borrowings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `borrowings`
--
ALTER TABLE `borrowings`
  ADD CONSTRAINT `borrowings_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `borrowings_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
