// src/components/LoginForm.jsx

import { useState } from "react";
import axios from "axios";
import { getAuthToken } from "../utils";
import "./LoginForm.css";

// <--- PERHATIKAN BAGIAN INI! NAMA PROP-NYA HARUS 'onLogin' --->
const LoginForm = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    role: "siswa",
  });
  const apiClient = axios.create();

  const token = getAuthToken();
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    withCredentials: true,
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log("📤 LoginForm: Akan mengirim data ini ke server:", formData);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/login/",
        formData
      );

      console.log("✅ LoginForm: Server merespon sukses!", response.data);

      // <--- DAN PERHATIKAN BAGIAN INI! YANG DIPANGGIL HARUS 'onLogin' --->
      onLogin(response.data.user);
    } catch (error) {
      console.error(
        "❌ LoginForm: Terjadi error saat login:",
        error.response?.data || error.message
      );
      alert("Login gagal! Periksa username dan password Anda.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <h1>AFL-SIMSEKOLAH-PLUS</h1>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <h2>Silakan Login</h2>

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">Login Sebagai</label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
            >
              <option value="admin_kepala">Admin / Kepala Sekolah</option>
              <option value="guru">Guru / Wali Kelas</option>
              <option value="siswa">Siswa</option>
              <option value="ortu">Orang Tua / Wali Murid</option>
            </select>
          </div>

          <button type="submit" className="login-button">
            🔒 Login
          </button>
        </form>

        <div className="login-footer">
          <p>
            &copy; 2025 AFL-SIMSEKOLAH-PLUS — Melayani Digitalisasi Sekolah
            Indonesia
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
