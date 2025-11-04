import { useState } from "react";
import axios from "axios";
import api from "../utils/axios";
import "./LoginForm.css";

const LoginForm = ({ onLogin }) => {
  // State untuk form data
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    role: "siswa",
  });

  // Fungsi untuk menangani perubahan input
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  // Fungsi untuk menangani submit form
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("📤 LoginForm: Akan mengirim data ini ke server:", formData);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/login/",
        formData
      );

      console.log("✅ LoginForm: Server merespon sukses!", response.data);

      // Simpan token ke localStorage
      localStorage.setItem("token", response.data.token);

      // Panggil fungsi onLogin dengan data user
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
              <option value="tu">Tata Usaha</option>
            </select>
          </div>

          <button type="submit" className="login-button">
            🔒 Login
          </button>
        </form>

        <div className="login-footer">
          <p>© 2023 AFL-SIMSEKOLAH-PLUS. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
