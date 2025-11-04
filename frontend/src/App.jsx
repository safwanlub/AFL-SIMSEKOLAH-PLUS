// src/App.jsx (VERSI YANG SUDAH DIPERBAIKI)

import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";

// Import halaman-halaman (kita akan buat ini setelahnya)
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Logika auto-login dari localStorage (gua jaga baik-baik)
  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      console.log("🔄 App: Menemukan user di localStorage, auto-login...");
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  // Fungsi untuk handle login sukses (dipanggil oleh LoginPage)
  const handleLoginSuccess = (loggedInUser) => {
    setUser(loggedInUser);
    localStorage.setItem("user", JSON.stringify(loggedInUser));
  };

  // Fungsi untuk handle logout (dipanggil oleh DashboardPage)
  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  // Tampilkan loading sambil cek localStorage
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        Loading...
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* Route untuk Guest (User yang belum login) */}
        <Route
          path="/login"
          element={
            !user ? (
              <LoginPage onLoginSuccess={handleLoginSuccess} />
            ) : (
              <Navigate to="/dashboard" />
            )
          }
        />

        {/* Route untuk User yang sudah login */}
        <Route
          path="/dashboard"
          element={
            user ? (
              <DashboardPage user={user} onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        {/* Route Default: Arahkan ke login atau dashboard */}
        <Route
          path="*"
          element={
            user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
          }
        />
      </Routes>

      {/* Komponen Toaster untuk notifikasi */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: "#363636",
            color: "#fff",
          },
        }}
      />
    </BrowserRouter>
  );
}

export default App;
