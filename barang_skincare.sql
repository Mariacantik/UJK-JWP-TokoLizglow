-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 21 Apr 2026 pada 14.15
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `barang_skincare`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `barang`
--

CREATE TABLE `barang` (
  `id` int(11) NOT NULL,
  `nama` varchar(150) NOT NULL,
  `stok` int(11) NOT NULL DEFAULT 0,
  `kategori_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `barang`
--

INSERT INTO `barang` (`id`, `nama`, `stok`, `kategori_id`) VALUES
(1, 'Vaseline', 134, 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `kategori_barang`
--

CREATE TABLE `kategori_barang` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kategori_barang`
--

INSERT INTO `kategori_barang` (`id`, `nama`) VALUES
(1, 'Lipbalm'),
(3, 'Sunscreen');

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier`
--

CREATE TABLE `supplier` (
  `id` int(11) NOT NULL,
  `nama_pt` varchar(255) NOT NULL,
  `username` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `supplier`
--

INSERT INTO `supplier` (`id`, `nama_pt`, `username`, `password`) VALUES
(1, 'PT Maju Mundur', 'supplier1', 'supplier1'),
(2, 'PT Barokah', 'supplier2', 'supplier2'),
(3, 'PT Indah Jaya', 'supplier3', 'supplier3');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi_keluar`
--

CREATE TABLE `transaksi_keluar` (
  `id` int(11) NOT NULL,
  `barang_id` int(11) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `tanggal` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `transaksi_keluar`
--

INSERT INTO `transaksi_keluar` (`id`, `barang_id`, `jumlah`, `tanggal`) VALUES
(2, 1, 12, '2025-01-11 16:33:44');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi_masuk`
--

CREATE TABLE `transaksi_masuk` (
  `id` int(11) NOT NULL,
  `barang_id` int(11) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `tanggal` datetime DEFAULT current_timestamp(),
  `supplier_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `transaksi_masuk`
--

INSERT INTO `transaksi_masuk` (`id`, `barang_id`, `jumlah`, `tanggal`, `supplier_id`) VALUES
(1, 1, 123, '2025-01-11 16:30:22', 1),
(2, 1, 13, '2025-01-11 16:30:50', 2);

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','Karyawan') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', 'from werkzeug.security import generate_password_hash, check_password_hash\nfrom flask import Blueprint, render_template, redirect, url_for, flash, request, session, Response\nfrom reportlab.pdfgen import canvas\nfrom io import BytesIO\nfrom .db import db_conn', 'Admin'),
(2, 'karyawan1', 'karyawan1', 'Karyawan');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kategori_id` (`kategori_id`);

--
-- Indeks untuk tabel `kategori_barang`
--
ALTER TABLE `kategori_barang`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nama` (`nama`);

--
-- Indeks untuk tabel `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `transaksi_keluar`
--
ALTER TABLE `transaksi_keluar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `barang_id` (`barang_id`);

--
-- Indeks untuk tabel `transaksi_masuk`
--
ALTER TABLE `transaksi_masuk`
  ADD PRIMARY KEY (`id`),
  ADD KEY `barang_id` (`barang_id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `barang`
--
ALTER TABLE `barang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `kategori_barang`
--
ALTER TABLE `kategori_barang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `supplier`
--
ALTER TABLE `supplier`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `transaksi_keluar`
--
ALTER TABLE `transaksi_keluar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `transaksi_masuk`
--
ALTER TABLE `transaksi_masuk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `barang`
--
ALTER TABLE `barang`
  ADD CONSTRAINT `barang_ibfk_1` FOREIGN KEY (`kategori_id`) REFERENCES `kategori_barang` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `transaksi_keluar`
--
ALTER TABLE `transaksi_keluar`
  ADD CONSTRAINT `transaksi_keluar_ibfk_1` FOREIGN KEY (`barang_id`) REFERENCES `barang` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `transaksi_masuk`
--
ALTER TABLE `transaksi_masuk`
  ADD CONSTRAINT `transaksi_masuk_ibfk_1` FOREIGN KEY (`barang_id`) REFERENCES `barang` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transaksi_masuk_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `supplier` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
