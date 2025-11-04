// src/pages/LoginPage.jsx
import React from "react";
import LoginForm from "../components/LoginForm";

const LoginPage = ({ onLoginSuccess }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center mb-6">Login Guru</h2>
        <LoginForm onLoginSuccess={onLoginSuccess} />
      </div>
    </div>
  );
};

export default LoginPage;
