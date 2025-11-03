import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

console.log("Rendering App component..."); // <-- TAMBAHKAN INI
ReactDOM.createRoot(document.getElementById("root")).render(<App />);
console.log("App component rendered successfully."); // <-- TAMBAHKAN INI

// const root = createRoot(document.getElementById("root"));
// root.render(<App />);
