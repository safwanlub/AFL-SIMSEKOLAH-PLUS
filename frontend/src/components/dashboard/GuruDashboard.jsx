// src/components/dashboard/GuruDashboard.jsx

import React, { useState, useEffect } from "react";
import axios from "axios";
import NilaiSelector from "../NilaiSelector"; // Asumsi ini lokasi file NilaiSelector

// <--- PERUBAHAN 1: Terima 'user' dari props di sini --->
function GuruDashboard({ user }) {
  const [selectedData, setSelectedData] = useState(null);
  const [students, setStudents] = useState([]);
  const [nilaiData, setNilaiData] = useState({});
  const [loading, setLoading] = useState(false);

  // Fungsi untuk dipanggil oleh NilaiSelector saat selesai memilih
  const handleSelectionComplete = async (data) => {
    console.log("📥 Data diterima dari NilaiSelector:", data);
    setSelectedData(data);
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/get-students-with-nilai/",
        data
      );
      console.log("✅ Data siswa berhasil diambil:", response.data);
      setStudents(response.data.data);

      // Inisialisasi state nilaiData dari data yang ada
      const initialNilai = {};
      response.data.data.forEach((s) => {
        initialNilai[s.siswa_id] = {
          nilai_pengetahuan: s.nilai_details["Nilai Pengetahuan"] || "",
          nilai_keterampilan: s.nilai_details["Nilai Keterampilan"] || "",
        };
      });
      setNilaiData(initialNilai);
    } catch (error) {
      console.error("❌ Gagal mengambil data siswa:", error);
      alert("Gagal mengambil data siswa. Coba lagi.");
    } finally {
      setLoading(false);
    }
  };

  // Handler untuk perubahan input nilai
  const handleNilaiChange = (siswaId, type, value) => {
    setNilaiData((prev) => ({
      ...prev,
      [siswaId]: {
        ...prev[siswaId],
        [type]: value,
      },
    }));
  };

  // Handler untuk menyimpan nilai
  const handleSaveNilai = async () => {
    if (!selectedData || Object.keys(nilaiData).length === 0) {
      alert("Tidak ada data untuk disimpan.");
      return;
    }

    const dataArray = Object.keys(nilaiData).map((siswaId) => ({
      siswa_id: siswaId,
      ...nilaiData[siswaId],
    }));

    console.log("📤 Nilai yang akan disimpan:", nilaiData);

    // <--- PERUBAHAN PENTING DI SINI --->
    const payload = {
      gurumapel_id: selectedData.gurumapel_id, // Kirim gurumapel_id
      tahun_ajaran_id: selectedData.tahun_ajaran_id,
      data: dataArray,
    };

    console.log("📦 Payload dikirim ke backend:", payload);

    try {
      // Hanya satu blok try...catch yang dibutuhkan
      const response = await axios.post(
        "http://127.0.0.1:8000/api/save-nilai/",
        payload,
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      console.log("✅ Berhasil menyimpan nilai:", response.data);
      alert("Nilai berhasil disimpan!");
    } catch (error) {
      console.error("❌ Error simpan nilai:", error);
      const errorMessage =
        error.response?.data?.message ||
        "Terjadi kesalahan saat menyimpan nilai.";
      alert(errorMessage);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Dashboard Guru</h2>
      //{" "}
      <NilaiSelector
        user={user}
        onSelectionComplete={handleSelectionComplete}
      />
      {loading && <p>Memuat data siswa...</p>}
      {!loading && students.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-3">Input Nilai Siswa</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full table-auto">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-2 text-left">Nama Siswa</th>
                  <th className="px-4 py-2 text-center">Nilai Pengetahuan</th>
                  <th className="px-4 py-2 text-center">Nilai Keterampilan</th>
                </tr>
              </thead>
              <tbody>
                {students.map((siswa) => (
                  <tr key={siswa.siswa_id} className="border-b">
                    <td className="px-4 py-2">{siswa.nama}</td>
                    <td className="px-4 py-2 text-center">
                      <input
                        type="number"
                        className="w-20 px-2 py-1 border rounded text-center"
                        value={
                          nilaiData[siswa.siswa_id]?.nilai_pengetahuan || ""
                        }
                        onChange={(e) =>
                          handleNilaiChange(
                            siswa.siswa_id,
                            "nilai_pengetahuan",
                            e.target.value
                          )
                        }
                      />
                    </td>
                    <td className="px-4 py-2 text-center">
                      <input
                        type="number"
                        className="w-20 px-2 py-1 border rounded text-center"
                        value={
                          nilaiData[siswa.siswa_id]?.nilai_keterampilan || ""
                        }
                        onChange={(e) =>
                          handleNilaiChange(
                            siswa.siswa_id,
                            "nilai_keterampilan",
                            e.target.value
                          )
                        }
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button
            onClick={handleSaveNilai}
            className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Simpan Nilai
          </button>
        </div>
      )}
    </div>
  );
}

export default GuruDashboard;
