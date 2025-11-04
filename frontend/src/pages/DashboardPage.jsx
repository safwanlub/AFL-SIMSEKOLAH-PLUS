// src/pages/DashboardPage.jsx
import React from "react";
import Dashboard from "../components/Dashboard"; // Komponen Dashboard lama kamu

const DashboardPage = ({ user, onLogout }) => {
  return <Dashboard user={user} onLogout={onLogout} />;
};

export default DashboardPage;
