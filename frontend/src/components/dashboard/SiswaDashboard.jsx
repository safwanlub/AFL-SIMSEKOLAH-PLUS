// src/components/dashboard/SiswaDashboard.jsx
import React from "react";
import "../Dashboard.css";

const SiswaDashboard = ({ user }) => {
  return (
    <div className="dashboard-content siswa-content">
      <h1>Dashboard Siswa</h1>
      <p>Selamat datang, {user.nama}!</p>
      <div className="info-card">
        <h3>Kelas: 4A</h3>
        <h3>NIS: 12345</h3>
      </div>
      <div className="recent-activity">
        <h3>Aktivitas Terkini</h3>
        <ul>
          <li>Raport Semester Ganjil sudah tersedia.</li>
          <li>Tagihan SPP Bulan Januari sudah Lunas.</li>
        </ul>
      </div>
    </div>
  );
};

export default SiswaDashboard;
