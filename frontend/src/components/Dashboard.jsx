// src/components/Dashboard.jsx

import React from "react";
import GuruDashboard from "./dashboard/GuruDashboard"; // <--- SUDAH DIPERBAIKI
import axios from "axios";

function Dashboard({ user, onLogout }) {
  const renderDashboardContent = () => {
    if (!user) {
      return <div>Silakan login terlebih dahulu.</div>;
    }

    switch (user.role) {
      case "guru":
        return <GuruDashboard user={user} onLogout={onLogout} />; // <--- SUDAH DIAKTIFKAN
      case "admin_kepala":
        return <div>Dashboard Admin Kepala Sekolah (Coming Soon)</div>;
      case "tu":
        return <div>Dashboard Tata Usaha (Coming Soon)</div>;
      case "siswa":
        return <div>Dashboard Siswa (Coming Soon)</div>;
      default:
        return <div>Dashboard untuk role {user.role} belum tersedia.</div>;
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 text-white">
        <div className="p-4">
          <h2 className="text-2xl font-bold">Sistem Sekolah</h2>
        </div>
        <nav className="mt-4">
          <a href="#" className="block py-2 px-4 hover:bg-gray-700">
            Dashboard
          </a>
          <a href="#" className="block py-2 px-4 hover:bg-gray-700">
            Data Siswa
          </a>
          <a href="#" className="block py-2 px-4 hover:bg-gray-700">
            Data Guru
          </a>
          <a href="#" className="block py-2 px-4 hover:bg-gray-700">
            Input Nilai
          </a>
          <a href="#" className="block py-2 px-4 hover:bg-gray-700">
            Laporan
          </a>
        </nav>
        <div className="absolute bottom-0 w-64 p-4">
          <div className="text-sm">
            <p>Logged in as:</p>
            <p className="font-semibold">{user?.nama || "Guest"}</p>
          </div>
          <button
            onClick={onLogout}
            className="mt-2 w-full bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded text-sm"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <h1 className="text-xl font-semibold text-gray-800">
              Welcome, {user?.nama}!
            </h1>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-x-auto overflow-y-auto bg-gray-200 p-6">
          {renderDashboardContent()}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
