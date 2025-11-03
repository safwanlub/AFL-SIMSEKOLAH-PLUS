// src/components/Sidebar.jsx
import React from "react";
import "./Sidebar.css"; // Kita akan buat file CSS-nya nanti

const Sidebar = ({ userRole }) => {
  // Menu untuk Admin/Kepala Sekolah
  const adminMenu = [
    { name: "Dashboard", icon: "🏠" },
    { name: "Data Siswa", icon: "🧑‍🎓" },
    { name: "Data Guru", icon: "👨‍🏫" },
    { name: "Data Kelas", icon: "📘" },
    { name: "Nilai", icon: "📊" },
    { name: "Absensi", icon: "📅" },
    { name: "Keuangan", icon: "💰" },
    { name: "Pengumuman", icon: "📢" },
  ];

  // Menu untuk Guru
  const guruMenu = [
    { name: "Dashboard", icon: "🏠" },
    { name: "Input Nilai", icon: "📝" },
    { name: "Rekap Absensi", icon: "📋" },
    { name: "Catatan Sikap", icon: "📄" },
    { name: "Raport Saya", icon: "🧾" },
  ];

  // Menu untuk Siswa/Ortu
  const siswaMenu = [
    { name: "Dashboard", icon: "🏠" },
    { name: "Nilai & Raport", icon: "📈" },
    { name: "Jadwal Pelajaran", icon: "📅" },
    { name: "Kehadiran", icon: "✅" },
    { name: "Tagihan SPP", icon: "💳" },
  ];

  // Pilih menu berdasarkan role
  let menuItems = [];
  if (userRole === "admin_kepala" || userRole === "tu") {
    menuItems = adminMenu;
  } else if (userRole === "guru") {
    menuItems = guruMenu;
  } else if (userRole === "siswa" || userRole === "ortu") {
    menuItems = siswaMenu;
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h3>AFL-SIMSEKOLAH+</h3>
      </div>
      <ul className="sidebar-menu">
        {menuItems.map((item, index) => (
          <li key={index} className="menu-item">
            <a href="#">
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-text">{item.name}</span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
