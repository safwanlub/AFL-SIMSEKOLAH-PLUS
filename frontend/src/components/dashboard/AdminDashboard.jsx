// src/components/dashboard/AdminDashboard.jsx
import React from "react";
import "../Dashboard.css"; // Kita pakai CSS yang sama

const AdminDashboard = ({ stats, loading }) => {
  return (
    <div className="dashboard-content admin-content">
      <h1>Dashboard Admin / Kepala Sekolah</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>👩‍🎓 Siswa Aktif</h3>
          <p>{loading ? "..." : stats.total_siswa}</p>
        </div>
        <div className="stat-card">
          <h3>👨‍🏫 Guru</h3>
          <p>{loading ? "..." : stats.total_guru}</p>
        </div>
        <div className="stat-card">
          <h3>📘 Kelas</h3>
          <p>{loading ? "..." : stats.total_kelas}</p>
        </div>
        <div className="stat-card">
          <h3>📅 Kehadiran Hari Ini (%)</h3>
          <p>95%</p> {/* Ini masih statis, nanti bisa diambil dari API */}
        </div>
        <div className="stat-card">
          <h3>💰 Pemasukan Bulan Ini</h3>
          <p>Rp 45.000.000</p>{" "}
          {/* Ini masih statis, nanti bisa diambil dari API */}
        </div>
      </div>
      <div className="charts-section">
        <h2>Grafik Kehadiran Mingguan</h2>
        <div className="chart-placeholder">[Chart Kehadiran]</div>
      </div>
    </div>
  );
};

export default AdminDashboard;
