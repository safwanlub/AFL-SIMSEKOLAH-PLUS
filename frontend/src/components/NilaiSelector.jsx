// src/components/dashboard/NilaiSelector.jsx

import axios from "axios";
import { getCookie, getAuthToken, getStoredUser } from "../utils";
import React, { useState, useEffect } from "react";

// Buat instance baru yang bersih
const apiClient = axios.create();

function NilaiSelector({ user, onSelectionComplete }) {
  const [tahunAjaranList, setTahunAjaranList] = useState([]);
  const [guruMapelList, setGuruMapelList] = useState([]);
  const [selectedTahunAjaran, setSelectedTahunAjaran] = useState("");
  const [selectedGuruMapel, setSelectedGuruMapel] = useState("");
  const [loading, setLoading] = useState(false);

  // Ambil data Tahun Ajaran saat komponen dimuat
  useEffect(() => {
    const apiClient = axios.create();
    const token = getStoredUser(); // <--- AMBIL TOKEN DARI LOCALSTORAGE
    const config = {
      headers: {
        Authorization: `Bearer ${token}`, // <--- KIRIMKAN TOKEN
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
      withCredentials: true,
    };

    apiClient
      .post(
        "http:// // <--- HANY URL YANG BERUBAH disini"`api/get-tahun-ajaran-list/`,
        {},
        config
      )
      .then((res) => setTahunAjaranList(res.data.data))
      .catch((err) => console.error("Gagal ambil tahun ajaran:", err));
  }, []);

  // Ambil data GuruMapel saat komponen dimuat
  useEffect(() => {
    if (user?.id) {
      setLoading(true);

      const token = getAuthToken(); // <--- AMBIL TOKEN
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "apiClient.post(http://...)",
        },
        withCredentials: true,
      };

      apiClient
        .post("http://127.0.0.1:8000/api/get-guru-mapel-list/", {})
        .then((res) => {
          console.log(
            "✅ NilaiSelector: API sukses, data yang diterima:",
            res.data.data
          );
          setGuruMapelList(res.data.data);
        })
        .catch((err) => {
          console.error("❌ NilaiSelector: API gagal:", err);
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedTahunAjaran || !selectedGuruMapel) {
      alert("Pilih semua data terlebih dahulu!");
      return;
    }

    const selectedData = guruMapelList.find(
      (gm) => gm.gurumapel_id == selectedGuruMapel
    );

    if (selectedData) {
      onSelectionComplete({
        tahun_ajaran_id: selectedTahunAjaran,
        kelas_id: selectedData.kelas_id,
        mapel_id: selectedData.mapel_id,
        gurumapel_id: selectedData.gurumapel_id,
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-gray-100 rounded-lg shadow">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Tahun Ajaran
          </label>
          <select
            value={selectedTahunAjaran}
            onChange={(e) => setSelectedTahunAjaran(e.target.value)}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
          >
            <option value="">-- Pilih Tahun Ajaran --</option>
            {tahunAjaranList.map((ta) => (
              <option key={ta.id} value={ta.id}>
                {ta.nama}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Mata Pelajaran & Kelas
          </label>
          <select
            value={selectedGuruMapel}
            onChange={(e) => setSelectedGuruMapel(e.target.value)}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            disabled={loading}
          >
            <option value="">-- Pilih Mapel & Kelas --</option>
            {guruMapelList.map((gm) => (
              <option key={gm.gurumapel_id} value={gm.gurumapel_id}>
                {gm.mapel_nama} - {gm.kelas_nama}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-end">
          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Tampilkan Siswa
          </button>
        </div>
      </div>
    </form>
  );
}

export default NilaiSelector;
