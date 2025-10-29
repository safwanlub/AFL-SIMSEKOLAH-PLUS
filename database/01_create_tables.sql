-- =====================================================
-- FINAL DATABASE SCHEMA V1.1 - SIMSEKOLAH+ (The Holistic Version)
-- =====================================================
-- Skrip ini untuk membuat semua tabel yang diperlukan
-- untuk aplikasi manajemen sekolah skala yayasan/SaaS.
-- Versi ini mencakup semua fitur akademik, keuangan, dinamis kelas,
-- manajemen pegawai, dan kerangka kerja unit non-akademik.
-- =====================================================

-- -----------------------------------------------------
-- 1. FONDASI UTAMA (YAYASAN & SEKOLAH)
-- -----------------------------------------------------

-- Tabel Yayasan/Lembaga
CREATE TABLE yayasan (
    id SERIAL PRIMARY KEY,
    nama_yayasan VARCHAR(150) NOT NULL UNIQUE,
    alamat TEXT,
    no_telp VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Sekolah (dalam naungan satu yayasan)
CREATE TABLE sekolah (
    id SERIAL PRIMARY KEY,
    yayasan_id INTEGER REFERENCES yayasan(id),
    nama_sekolah VARCHAR(150) NOT NULL,
    npsn VARCHAR(20) UNIQUE,
    alamat TEXT,
    logo_sekolah VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- 2. KOMERSIAL & SAAS
-- -----------------------------------------------------

-- Tabel untuk mendefinisikan paket langganan
CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    nama_paket VARCHAR(50) NOT NULL UNIQUE,
    harga_bulanan INTEGER NOT NULL,
    max_siswa INTEGER, -- NULL untuk unlimited (Pro/Custom)
    fitur JSONB -- Contoh: {"nilai": true, "keuangan": false, "notif_wa": false}
);

-- Tabel untuk mencatat langganan setiap sekolah
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER UNIQUE NOT NULL REFERENCES sekolah(id),
    package_id INTEGER NOT NULL REFERENCES packages(id),
    tanggal_mulai DATE NOT NULL,
    tanggal_akhir DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled'))
);

-- Tabel untuk menyimpan pengaturan kustom per sekolah
CREATE TABLE sekolah_settings (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    setting_key VARCHAR(100) NOT NULL,
    setting_value TEXT,
    UNIQUE(sekolah_id, setting_key)
);

-- -----------------------------------------------------
-- 3. MANAJEMEN PENGGUNA & ROLE
-- -----------------------------------------------------

-- Tabel Users (sekarang terkait dengan sekolah)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    nama VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin_kepala', 'tu', 'guru', 'siswa', 'ortu', 'pegawai', 'alumni')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- 4. DATA MASTER AKADEMIK & NON-AKADEMIK
-- -----------------------------------------------------

-- Tabel untuk menyimpan data penerbit buku
CREATE TABLE penerbit (
    id SERIAL PRIMARY KEY,
    nama_penerbit VARCHAR(100) NOT NULL UNIQUE
);

-- Tabel untuk menyimpan data mata pelajaran
CREATE TABLE mapel (
    id SERIAL PRIMARY KEY,
    kode_mapel VARCHAR(10) NOT NULL UNIQUE,
    nama_mapel VARCHAR(100) NOT NULL UNIQUE,
    kelompok VARCHAR(50),
    kkm INTEGER NOT NULL DEFAULT 75,
    deskripsi TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabel untuk menyimpan data judul buku
CREATE TABLE buku (
    id SERIAL PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    penulis VARCHAR(100),
    penerbit_id INTEGER REFERENCES penerbit(id),
    mapel_id INTEGER REFERENCES mapel(id)
);

-- Tabel Master untuk Komponen Nilai
CREATE TABLE komponen_nilai (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    nama_komponen VARCHAR(100) NOT NULL,
    jenis VARCHAR(15) NOT NULL CHECK (jenis IN ('Pengetahuan', 'Keterampilan')),
    bobot INTEGER NOT NULL CHECK (bobot > 0),
    UNIQUE(sekolah_id, nama_komponen)
);

-- Tabel Master untuk Jenis Pembayaran/Tagihan
CREATE TABLE jenis_pembayaran (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    nama_jenis VARCHAR(100) NOT NULL,
    nominal_default INTEGER NOT NULL,
    is_recurring BOOLEAN NOT NULL DEFAULT FALSE
);

-- Tabel Master untuk Hobi
CREATE TABLE hobi (
    id SERIAL PRIMARY KEY,
    nama_hobi VARCHAR(100) NOT NULL UNIQUE,
    kategori VARCHAR(50) NOT NULL
);

-- Tabel Master untuk Cita-cita
CREATE TABLE cita_cita (
    id SERIAL PRIMARY KEY,
    nama_cita_cita VARCHAR(100) NOT NULL UNIQUE
);

-- Tabel Master untuk Jam Pelajaran
CREATE TABLE jam_pelajaran (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    nama_sesi VARCHAR(50) NOT NULL,
    jam_mulai TIME NOT NULL,
    jam_selesai TIME NOT NULL,
    urutan INTEGER NOT NULL,
    UNIQUE(sekolah_id, urutan)
);

-- Tabel Master untuk Unit (UKS, Perpustakaan, Ekskul, dll)
CREATE TABLE unit (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    nama_unit VARCHAR(100) NOT NULL,
    jenis_unit VARCHAR(20) NOT NULL,
    deskripsi TEXT,
    pembina_id INTEGER REFERENCES users(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE(sekolah_id, nama_unit)
);

-- -----------------------------------------------------
-- 5. DATA ENTITAS UTAMA (GURU, PEGAWAI, KELAS, SISWA)
-- -----------------------------------------------------

-- Tabel untuk menyimpan data guru (versi lengkap)
CREATE TABLE guru (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id),
    nip VARCHAR(20) UNIQUE NOT NULL,
    nuptk VARCHAR(20) UNIQUE,
    jenis_kelamin VARCHAR(10) NOT NULL CHECK (jenis_kelamin IN ('Laki-laki', 'Perempuan')),
    tempat_lahir VARCHAR(50),
    tanggal_lahir DATE,
    agama VARCHAR(20),
    alamat TEXT,
    no_hp VARCHAR(20),
    email VARCHAR(100),
    tanggal_mulai_kerja DATE,
    status_kepegawaian VARCHAR(20) NOT NULL CHECK (status_kepegawaian IN ('PNS', 'GTK Honorer', 'Guru Yayasan')),
    foto VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabel untuk riwayat pendidikan guru
CREATE TABLE riwayat_pendidikan_guru (
    id SERIAL PRIMARY KEY,
    guru_id INTEGER NOT NULL REFERENCES guru(id) ON DELETE CASCADE,
    tingkat VARCHAR(10) NOT NULL,
    jurusan VARCHAR(100),
    institusi VARCHAR(100),
    tahun_lulus INTEGER
);

-- Tabel untuk menyimpan data pegawai non-guru
CREATE TABLE pegawai (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id),
    nip VARCHAR(20) UNIQUE NOT NULL,
    jenis_kelamin VARCHAR(10) NOT NULL CHECK (jenis_kelamin IN ('Laki-laki', 'Perempuan')),
    tempat_lahir VARCHAR(50),
    tanggal_lahir DATE,
    alamat TEXT,
    no_hp VARCHAR(20),
    jabatan VARCHAR(100) NOT NULL,
    tanggal_mulai_kerja DATE,
    status_kepegawaian VARCHAR(20) NOT NULL CHECK (status_kepegawaian IN ('PNS', 'GTK Honorer', 'Karyawan Yayasan')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Tahun Ajaran
CREATE TABLE tahun_ajaran (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    nama VARCHAR(20) NOT NULL,
    tanggal_mulai DATE NOT NULL,
    tanggal_selesai DATE NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'Arsip' CHECK (status IN ('Aktif', 'Ditutup', 'Arsip')),
    UNIQUE(sekolah_id, nama)
);

-- Tabel untuk menyimpan data kelas
CREATE TABLE kelas (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    tingkat INTEGER NOT NULL,
    nama_kelas VARCHAR(10) NOT NULL,
    ruangan VARCHAR(50),
    wali_kelas_id INTEGER UNIQUE REFERENCES guru(id),
    UNIQUE(sekolah_id, tingkat, nama_kelas)
);

-- Tabel untuk menyimpan data siswa
CREATE TABLE siswa (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    user_id INTEGER UNIQUE REFERENCES users(id),
    nis VARCHAR(20) NOT NULL,
    nisn VARCHAR(20) UNIQUE,
    nama VARCHAR(100) NOT NULL,
    jenis_kelamin VARCHAR(10) NOT NULL CHECK (jenis_kelamin IN ('Laki-laki', 'Perempuan')),
    tempat_lahir VARCHAR(50),
    tanggal_lahir DATE,
    agama VARCHAR(20),
    alamat_jalan TEXT,
    rt_rw VARCHAR(10),
    kelurahan VARCHAR(50),
    kecamatan VARCHAR(50),
    kota_kabupaten VARCHAR(50),
    provinsi VARCHAR(50),
    kode_pos VARCHAR(10),
    no_hp_siswa VARCHAR(20),
    nama_kontak_darurat VARCHAR(100),
    nomor_kontak_darurat VARCHAR(20),
    foto VARCHAR(255),
    kelas_id INTEGER REFERENCES kelas(id),
    status_siswa VARCHAR(15) NOT NULL DEFAULT 'Aktif' CHECK (status_siswa IN ('Aktif', 'Pindah', 'Lulus', 'Cuti', 'Dikeluarkan')),
    tanggal_masuk DATE NOT NULL,
    tanggal_keluar DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Orang Tua/Wali Murid
CREATE TABLE ortu (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    nama_ayah VARCHAR(100),
    nama_ibu VARCHAR(100),
    alamat TEXT,
    no_hp VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Alumni
CREATE TABLE alumni (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    user_id INTEGER UNIQUE REFERENCES users(id),
    nis_lama VARCHAR(20),
    nama VARCHAR(100) NOT NULL,
    tahun_lulus INTEGER,
    no_hp VARCHAR(20),
    email VARCHAR(100),
    info_terkini TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- 6. TABEL PENGHUBUNG (MANY-TO-MANY)
-- -----------------------------------------------------

CREATE TABLE guru_mapel (
    id SERIAL PRIMARY KEY,
    guru_id INTEGER NOT NULL REFERENCES guru(id),
    mapel_id INTEGER NOT NULL REFERENCES mapel(id),
    buku_id INTEGER REFERENCES buku(id)
);

CREATE TABLE siswa_ortu (
    siswa_id INTEGER NOT NULL REFERENCES siswa(id) ON DELETE CASCADE,
    ortu_id INTEGER NOT NULL REFERENCES ortu(id) ON DELETE CASCADE,
    hubungan VARCHAR(10) CHECK (hubungan IN ('Ayah', 'Ibu', 'Wali')),
    PRIMARY KEY (siswa_id, ortu_id)
);

CREATE TABLE siswa_hobi (
    siswa_id INTEGER NOT NULL REFERENCES siswa(id) ON DELETE CASCADE,
    hobi_id INTEGER NOT NULL REFERENCES hobi(id) ON DELETE CASCADE,
    PRIMARY KEY (siswa_id, hobi_id)
);

CREATE TABLE siswa_cita_cita (
    siswa_id INTEGER NOT NULL REFERENCES siswa(id) ON DELETE CASCADE,
    cita_cita_id INTEGER NOT NULL REFERENCES cita_cita(id) ON DELETE CASCADE,
    PRIMARY KEY (siswa_id, cita_cita_id)
);

CREATE TABLE unit_anggota (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER NOT NULL REFERENCES unit(id) ON DELETE CASCADE,
    siswa_id INTEGER REFERENCES siswa(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    tanggal_bergabung DATE NOT NULL,
    jabatan_di_unit VARCHAR(50),
    CHECK ( (siswa_id IS NOT NULL AND user_id IS NULL) OR (siswa_id IS NULL AND user_id IS NOT NULL) )
);

-- -----------------------------------------------------
-- 7. FITUR DINAMIS PER KELAS & UNIT
-- -----------------------------------------------------

CREATE TABLE organisasi_kelas (
    id SERIAL PRIMARY KEY,
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    jabatan VARCHAR(50) NOT NULL,
    UNIQUE(kelas_id, tahun_ajaran_id, jabatan)
);

CREATE TABLE piket_kelas (
    id SERIAL PRIMARY KEY,
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    hari VARCHAR(10) NOT NULL,
    tugas VARCHAR(100),
    UNIQUE(kelas_id, tahun_ajaran_id, siswa_id, hari)
);

CREATE TABLE keuangan_kelas (
    id SERIAL PRIMARY KEY,
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    tanggal DATE NOT NULL,
    jenis VARCHAR(20) NOT NULL CHECK (jenis IN ('Pemasukan', 'Pengeluaran')),
    keterangan TEXT,
    nominal INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE program_kelas (
    id SERIAL PRIMARY KEY,
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    nama_program VARCHAR(150) NOT NULL,
    deskripsi TEXT,
    tanggal_mulai DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Rencana' CHECK (status IN ('Rencana', 'Berjalan', 'Selesai', 'Batal'))
);

CREATE TABLE log_kelas (
    id SERIAL PRIMARY KEY,
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    tanggal DATE NOT NULL,
    isi_log TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE jadwal_pelajaran (
    id SERIAL PRIMARY KEY,
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    hari VARCHAR(10) NOT NULL,
    jam_pelajaran_id INTEGER NOT NULL REFERENCES jam_pelajaran(id),
    mapel_id INTEGER NOT NULL REFERENCES mapel(id),
    guru_id INTEGER NOT NULL REFERENCES guru(id),
    UNIQUE(kelas_id, tahun_ajaran_id, hari, jam_pelajaran_id)
);

CREATE TABLE unit_kegiatan (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER NOT NULL REFERENCES unit(id) ON DELETE CASCADE,
    nama_kegiatan VARCHAR(200) NOT NULL,
    tanggal_mulai TIMESTAMP WITH TIME ZONE,
    tanggal_selesai TIMESTAMP WITH TIME ZONE,
    deskripsi TEXT
);

CREATE TABLE unit_log (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER NOT NULL REFERENCES unit(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    tanggal TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    aktivitas TEXT NOT NULL
);

-- -----------------------------------------------------
-- 8. TRANSAKSI AKADEMIK & KEUANGAN
-- -----------------------------------------------------

CREATE TABLE nilai (
    id SERIAL PRIMARY KEY,
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    mapel_id INTEGER NOT NULL REFERENCES mapel(id),
    guru_mapel_id INTEGER NOT NULL REFERENCES guru_mapel(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    nilai_akhir_pengetahuan INTEGER CHECK (nilai_akhir_pengetahuan >= 0 AND nilai_akhir_pengetahuan <= 100),
    nilai_akhir_keterampilan INTEGER CHECK (nilai_akhir_keterampilan >= 0 AND nilai_akhir_keterampilan <= 100),
    predikat_pengetahuan VARCHAR(10),
    predikat_keterampilan VARCHAR(10),
    deskripsi_pengetahuan TEXT,
    deskripsi_keterampilan TEXT,
    catatan_sikap TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(siswa_id, mapel_id, tahun_ajaran_id)
);

CREATE TABLE nilai_detail (
    id SERIAL PRIMARY KEY,
    nilai_id INTEGER NOT NULL REFERENCES nilai(id) ON DELETE CASCADE,
    komponen_nilai_id INTEGER NOT NULL REFERENCES komponen_nilai(id),
    skor INTEGER NOT NULL CHECK (skor >= 0 AND skor <= 100),
    UNIQUE(nilai_id, komponen_nilai_id)
);

CREATE TABLE absensi (
    id SERIAL PRIMARY KEY,
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    tanggal DATE NOT NULL,
    status VARCHAR(15) NOT NULL CHECK (status IN ('Hadir', 'Terlambat', 'Izin', 'Sakit', 'Alpha')),
    keterangan TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    waktu_input TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(siswa_id, tanggal)
);

CREATE TABLE perizinan_siswa (
    id SERIAL PRIMARY KEY,
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    kelas_id INTEGER NOT NULL REFERENCES kelas(id),
    tanggal DATE NOT NULL,
    waktu_keluar TIMESTAMP WITH TIME ZONE NOT NULL,
    waktu_kembali TIMESTAMP WITH TIME ZONE,
    alasan TEXT,
    keterangan_akhir TEXT,
    pemberi_izin VARCHAR(100) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(15) NOT NULL DEFAULT 'Keluar' CHECK (status IN ('Keluar', 'Kembali', 'Tidak Kembali'))
);

CREATE TABLE tagihan (
    id SERIAL PRIMARY KEY,
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    jenis_pembayaran_id INTEGER NOT NULL REFERENCES jenis_pembayaran(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    periode VARCHAR(20) NOT NULL,
    nominal_tagihan INTEGER NOT NULL,
    tanggal_jatuh_tempo DATE,
    status_tagihan VARCHAR(15) NOT NULL DEFAULT 'Belum Lunas' CHECK (status_tagihan IN ('Belum Lunas', 'Lunas', 'Dibatalkan')),
    UNIQUE(siswa_id, jenis_pembayaran_id, periode)
);

CREATE TABLE pembayaran_log (
    id SERIAL PRIMARY KEY,
    tagihan_id INTEGER NOT NULL REFERENCES tagihan(id),
    nominal_dibayar INTEGER NOT NULL,
    tanggal_bayar TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metode_pembayaran VARCHAR(20) NOT NULL,
    bukti_pembayaran VARCHAR(255),
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE pengeluaran_log (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    tanggal_pengeluaran DATE NOT NULL,
    kategori VARCHAR(50) NOT NULL,
    keterangan TEXT,
    nominal INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE ekstrakurikuler_nilai (
    id SERIAL PRIMARY KEY,
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    nama_ekskul VARCHAR(100) NOT NULL,
    predikat VARCHAR(5) CHECK (predikat IN ('A', 'B', 'C', 'D')),
    keterangan TEXT
);

CREATE TABLE pengumuman (
    id SERIAL PRIMARY KEY,
    sekolah_id INTEGER NOT NULL REFERENCES sekolah(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    judul VARCHAR(200) NOT NULL,
    isi TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- 9. OUTPUT & LAPORAN
-- -----------------------------------------------------

CREATE TABLE raport (
    id SERIAL PRIMARY KEY,
    siswa_id INTEGER NOT NULL REFERENCES siswa(id),
    tahun_ajaran_id INTEGER NOT NULL REFERENCES tahun_ajaran(id),
    jenis_raport VARCHAR(20) NOT NULL CHECK (jenis_raport IN ('Tengah Semester', 'Akhir Semester')),
    rata_nilai_pengetahuan INTEGER,
    rata_nilai_keterampilan INTEGER,
    ranking_kelas INTEGER,
    total_hadir INTEGER DEFAULT 0,
    total_sakit INTEGER DEFAULT 0,
    total_izin INTEGER DEFAULT 0,
    total_alpha INTEGER DEFAULT 0,
    catatan_wali_kelas TEXT,
    catatan_ekstrakurikuler TEXT,
    status_raport VARCHAR(20) NOT NULL DEFAULT 'Draft' CHECK (status_raport IN ('Draft', 'Menunggu Persetujuan', 'Disetujui', 'Diterbitkan')),
    tanggal_disetujui TIMESTAMP WITH TIME ZONE,
    pdf_link VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(siswa_id, tahun_ajaran_id, jenis_raport)
);
