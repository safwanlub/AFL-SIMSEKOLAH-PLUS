import React, { useState, useEffect } from "react";
import axios from "axios";
import api from "../utils/axios"; // Ganti dengan instance axios yang sudah dikonfigurasi

function NilaiSelector({ user, onSelectionComplete }) {
  const [tahunAjaranList, setTahunAjaranList] = useState([]);
  const [guruMapelList, setGuruMapelList] = useState([]);
  const [selectedTahunAjaran, setSelectedTahunAjaran] = useState("");
  const [selectedGuruMapel, setSelectedGuruMapel] = useState("");
  const [loading, setLoading] = useState(false);

  // Ambil data Tahun Ajaran saat komponen dimuat
  useEffect(() => {
    const fetchTahunAjaran = async () => {
      try {
        const response = await api.get("/get-tahun-ajaran-list/");
        console.log("✅ Tahun Ajaran data:", response.data);
        setTahunAjaranList(response.data.data || []);
      } catch (error) {
        console.error("❌ Gagal ambil tahun ajaran:", error);
      }
    };

    fetchTahunAjaran();
  }, []);

  // Ambil data GuruMapel saat komponen dimuat
  useEffect(() => {
    const fetchGuruMapel = async () => {
      if (!user?.id) return;

      setLoading(true);
      try {
        const response = await api.post("/get-guru-mapel-list/", {
          guru_id: user.id,
        });
        console.log("✅ GuruMapel data:", response.data);
        setGuruMapelList(response.data.data || []);
      } catch (error) {
        console.error("❌ Gagal ambil guru mapel:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchGuruMapel();
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
