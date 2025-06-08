-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 31, 2025 at 02:55 PM
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
-- Database: `tes`
--

-- --------------------------------------------------------

--
-- Table structure for table `dosen`
--

CREATE TABLE `dosen` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dosen`
--

INSERT INTO `dosen` (`username`, `password`, `nama`) VALUES
('dos1', '123', 'Dr. Andi'),
('dos2', '123', 'Dr. Agus');

-- --------------------------------------------------------

--
-- Table structure for table `dosen_mengajar`
--

CREATE TABLE `dosen_mengajar` (
  `id` int(11) NOT NULL,
  `username_dosen` varchar(50) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dosen_mengajar`
--

INSERT INTO `dosen_mengajar` (`id`, `username_dosen`, `kode_mk`) VALUES
(1, 'dos1', 'IF201'),
(2, 'dos1', 'IF202'),
(3, 'dos2', 'IF203'),
(4, 'dos2', 'IF402');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL,
  `nilai` int(11) DEFAULT NULL,
  `komentar` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `username`, `kode_mk`, `nilai`, `komentar`) VALUES
(1, 'udin', 'IF202', 4, 'Materi mudah dipahami'),
(2, 'siti', 'IF201', 5, 'Dosen sangat interaktif');

-- --------------------------------------------------------

--
-- Table structure for table `hasil_studi`
--

CREATE TABLE `hasil_studi` (
  `id` int(11) NOT NULL,
  `nim` varchar(10) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL,
  `tugas` float DEFAULT NULL,
  `uts` float DEFAULT NULL,
  `uas` float DEFAULT NULL,
  `akhir` float DEFAULT NULL,
  `huruf` char(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hasil_studi`
--

INSERT INTO `hasil_studi` (`id`, `nim`, `kode_mk`, `tugas`, `uts`, `uas`, `akhir`, `huruf`) VALUES
(1, 'U00151', 'IF201', 100, 100, 100, 100, 'A'),
(2, 'U00151', 'IF202', 100, 70, 90, 86.67, 'B'),
(3, 'U00151', 'IF203', 80, 85, 90, 85, 'A'),
(4, 'U00152', 'IF201', 100, 80, 100, 93.33, 'A'),
(5, 'U00152', 'IF202', 80, 100, 90, 90, 'A'),
(6, 'U00152', 'IF203', 80, 85, 90, 85, 'A'),
(7, 'U00101', 'IF401', 80, 85, 90, 85, 'A'),
(8, 'U00101', 'IF402', 80, 85, 90, 85, 'A'),
(9, 'U00101', 'IF403', 80, 85, 90, 85, 'A');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal_kuliah`
--

CREATE TABLE `jadwal_kuliah` (
  `id` int(11) NOT NULL,
  `semester_id` int(11) DEFAULT NULL,
  `hari` varchar(20) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL,
  `waktu` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal_kuliah`
--

INSERT INTO `jadwal_kuliah` (`id`, `semester_id`, `hari`, `kode_mk`, `waktu`) VALUES
(1, 2, 'Senin', 'IF201', '08:00-10:00'),
(2, 2, 'Senin', 'IF202', '10:00-12:00'),
(3, 2, 'Rabu', 'IF203', '08:00-10:00'),
(4, 4, 'Selasa', 'IF401', '08:00-10:00'),
(5, 4, 'Selasa', 'IF402', '10:00-12:00'),
(6, 4, 'Kamis', 'IF403', '08:00-10:00');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal_ujian`
--

CREATE TABLE `jadwal_ujian` (
  `id` int(11) NOT NULL,
  `semester_id` int(11) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL,
  `tanggal` date DEFAULT NULL,
  `waktu` varchar(20) DEFAULT NULL,
  `ruangan` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal_ujian`
--

INSERT INTO `jadwal_ujian` (`id`, `semester_id`, `kode_mk`, `tanggal`, `waktu`, `ruangan`) VALUES
(1, 2, 'IF201', '2025-06-15', '09:00-10.00', 'Ruang A101'),
(2, 2, 'IF202', '2025-06-17', '13:00-14.00', 'Ruang B202'),
(3, 2, 'IF203', '2025-06-18', '10:00-11.00', 'Ruang C303'),
(4, 4, 'IF401', '2025-06-17', '10:00-11.00', 'Ruang C208'),
(5, 4, 'IF402', '2025-06-18', '08:00-09.30', 'Ruang C208'),
(6, 4, 'IF403', '2025-06-16', '09:00-10.30', 'Ruang A101');

-- --------------------------------------------------------

--
-- Table structure for table `krs`
--

CREATE TABLE `krs` (
  `id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL,
  `semester` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `krs`
--

INSERT INTO `krs` (`id`, `username`, `kode_mk`, `semester`, `status`) VALUES
(7, 'udin', 'IF301', 3, 'Diajukan'),
(8, 'udin', 'IF302', 3, 'Diajukan');

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `nim` varchar(10) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `semester` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`nim`, `username`, `password`, `nama`, `semester`) VALUES
('U00101', 'budi', '123', 'Budi Ari', 4),
('U00151', 'udin', '123', 'Udin Safrudin', 2),
('U00152', 'siti', '123', 'Siti Anisa', 2);

-- --------------------------------------------------------

--
-- Table structure for table `mata_kuliah`
--

CREATE TABLE `mata_kuliah` (
  `kode` varchar(10) NOT NULL,
  `nama` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mata_kuliah`
--

INSERT INTO `mata_kuliah` (`kode`, `nama`) VALUES
('IF201', 'Algoritma dan Pemrograman'),
('IF202', 'Struktur Data'),
('IF203', 'Matematika Diskrit'),
('IF301', 'Pemrograman Web'),
('IF302', 'Elektronika'),
('IF401', 'Pemrograman Lanjut'),
('IF402', 'Jaringan Komputer'),
('IF403', 'Sistem Operasi');

-- --------------------------------------------------------

--
-- Table structure for table `paket_semester`
--

CREATE TABLE `paket_semester` (
  `id` int(11) NOT NULL,
  `semester_id` int(11) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `paket_semester`
--

INSERT INTO `paket_semester` (`id`, `semester_id`, `kode_mk`) VALUES
(1, 2, 'IF201'),
(2, 2, 'IF202'),
(3, 2, 'IF203'),
(4, 4, 'IF401'),
(5, 4, 'IF402'),
(6, 4, 'IF403'),
(7, 3, 'IF301'),
(8, 3, 'IF302');

-- --------------------------------------------------------

--
-- Table structure for table `pengajuan_surat`
--

CREATE TABLE `pengajuan_surat` (
  `id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `jenis_surat` varchar(50) DEFAULT NULL,
  `alasan` text DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengajuan_surat`
--

INSERT INTO `pengajuan_surat` (`id`, `username`, `jenis_surat`, `alasan`, `status`) VALUES
(1, 'udin', 'Surat Aktif Kuliah', 'Untuk keperluan beasiswa', 'Diproses'),
(2, 'budi', 'Surat Cuti', 'Alasan keluarga', 'Diajukan');

-- --------------------------------------------------------

--
-- Table structure for table `semester`
--

CREATE TABLE `semester` (
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `semester`
--

INSERT INTO `semester` (`id`) VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dosen`
--
ALTER TABLE `dosen`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `dosen_mengajar`
--
ALTER TABLE `dosen_mengajar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username_dosen` (`username_dosen`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `hasil_studi`
--
ALTER TABLE `hasil_studi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `nim` (`nim`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `jadwal_kuliah`
--
ALTER TABLE `jadwal_kuliah`
  ADD PRIMARY KEY (`id`),
  ADD KEY `semester_id` (`semester_id`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `jadwal_ujian`
--
ALTER TABLE `jadwal_ujian`
  ADD PRIMARY KEY (`id`),
  ADD KEY `semester_id` (`semester_id`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `krs`
--
ALTER TABLE `krs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`nim`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  ADD PRIMARY KEY (`kode`);

--
-- Indexes for table `paket_semester`
--
ALTER TABLE `paket_semester`
  ADD PRIMARY KEY (`id`),
  ADD KEY `semester_id` (`semester_id`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indexes for table `pengajuan_surat`
--
ALTER TABLE `pengajuan_surat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `semester`
--
ALTER TABLE `semester`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dosen_mengajar`
--
ALTER TABLE `dosen_mengajar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `hasil_studi`
--
ALTER TABLE `hasil_studi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `jadwal_kuliah`
--
ALTER TABLE `jadwal_kuliah`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `jadwal_ujian`
--
ALTER TABLE `jadwal_ujian`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `krs`
--
ALTER TABLE `krs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `paket_semester`
--
ALTER TABLE `paket_semester`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `pengajuan_surat`
--
ALTER TABLE `pengajuan_surat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dosen_mengajar`
--
ALTER TABLE `dosen_mengajar`
  ADD CONSTRAINT `dosen_mengajar_ibfk_1` FOREIGN KEY (`username_dosen`) REFERENCES `dosen` (`username`),
  ADD CONSTRAINT `dosen_mengajar_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode`);

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`username`) REFERENCES `mahasiswa` (`username`),
  ADD CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode`);

--
-- Constraints for table `hasil_studi`
--
ALTER TABLE `hasil_studi`
  ADD CONSTRAINT `hasil_studi_ibfk_1` FOREIGN KEY (`nim`) REFERENCES `mahasiswa` (`nim`),
  ADD CONSTRAINT `hasil_studi_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode`);

--
-- Constraints for table `jadwal_kuliah`
--
ALTER TABLE `jadwal_kuliah`
  ADD CONSTRAINT `jadwal_kuliah_ibfk_1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`id`),
  ADD CONSTRAINT `jadwal_kuliah_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode`);

--
-- Constraints for table `jadwal_ujian`
--
ALTER TABLE `jadwal_ujian`
  ADD CONSTRAINT `jadwal_ujian_ibfk_1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`id`),
  ADD CONSTRAINT `jadwal_ujian_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode`);

--
-- Constraints for table `krs`
--
ALTER TABLE `krs`
  ADD CONSTRAINT `krs_ibfk_1` FOREIGN KEY (`username`) REFERENCES `mahasiswa` (`username`),
  ADD CONSTRAINT `krs_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode`);

--
-- Constraints for table `paket_semester`
--
ALTER TABLE `paket_semester`
  ADD CONSTRAINT `paket_semester_ibfk_1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`id`),
  ADD CONSTRAINT `paket_semester_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode`);

--
-- Constraints for table `pengajuan_surat`
--
ALTER TABLE `pengajuan_surat`
  ADD CONSTRAINT `pengajuan_surat_ibfk_1` FOREIGN KEY (`username`) REFERENCES `mahasiswa` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
