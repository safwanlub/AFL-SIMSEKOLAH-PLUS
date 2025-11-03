// src/App.jsx

import React, { useState } from "react";
import axios from "axios"; // Ini masih diperlukan untuk useEffect nanti
import LoginForm from "./components/LoginForm";
import Dashboard from "./components/Dashboard";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);

  // Fungsi ini TIDAK BOLEH MEMANGGIL API LAGI
  const handleLogin = (loggedInUser) => {
    console.log(
      "🧑‍💼 App: Menerima user yang sudah login dari LoginForm:",
      loggedInUser
    );

    // Simpan ke localStorage
    localStorage.setItem("user", JSON.stringify(loggedInUser));

    // Update state di App
    setUser(loggedInUser);
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
  };

  // Cek localStorage saat pertama kali load
  React.useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      console.log("🔄 App: Menemukan user di localStorage, auto-login...");
      setUser(JSON.parse(savedUser));
    }
  }, []);

  return (
    <div className="App">
      {user ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <LoginForm onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
