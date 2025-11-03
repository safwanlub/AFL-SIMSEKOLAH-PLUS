# backend/sekolah/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------------------------------
# 1. MODEL USER (PENGUBAHAN DARI DEFAULT DJANGO)
# -----------------------------------------------------
class User(AbstractUser):
    nama = models.CharField(max_length=100)
    # Tambahkan field yang ada di tabel users kita
    sekolah = models.ForeignKey('Sekolah', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin_kepala', 'Admin Kepala Sekolah'),
            ('tu', 'Tata Usaha'),
            ('guru', 'Guru'),
            ('siswa', 'Siswa'),
            ('ortu', 'Orang Tua'),
            ('pegawai', 'Pegawai'),
            ('alumni', 'Alumni'),
        ],
        default='siswa'
    )
    # Field default dari AbstractUser (username, password, email, etc.) sudah ada

    def __str__(self):
        return f"{self.nama} ({self.get_role_display()})"

# -----------------------------------------------------
# 2. MODEL FONDASI UTAMA
# -----------------------------------------------------

class Yayasan(models.Model):
    nama_yayasan = models.CharField(max_length=150, unique=True)
    alamat = models.TextField(blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_yayasan

class Sekolah(models.Model):
    yayasan = models.ForeignKey(Yayasan, on_delete=models.SET_NULL, null=True, blank=True)
    nama_sekolah = models.CharField(max_length=150)
    npsn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    logo_sekolah = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_sekolah

# -----------------------------------------------------
# 3. MODEL UNIT (KERANGKA KERJA HOLISTIK)
# -----------------------------------------------------

class Unit(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama_unit = models.CharField(max_length=100)
    jenis_unit = models.CharField(max_length=20) # Akademik, Non-Akademik, dll
    deskripsi = models.TextField(blank=True, null=True)
    pembina = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='unit_dibina')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('sekolah', 'nama_unit')

    def __str__(self):
        return f"{self.nama_unit} - {self.sekolah.nama_sekolah}"
    
    # -----------------------------------------------------
# 4. DATA ENTITAS UTAMA (GURU, PEGAWAI, KELAS, SISWA)
# -----------------------------------------------------

class TahunAjaran(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama = models.CharField(max_length=20)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Aktif', 'Aktif'), ('Ditutup', 'Ditutup'), ('Arsip', 'Arsip')],
        default='Arsip'
    )

    class Meta:
        unique_together = ('sekolah', 'nama')

    def __str__(self):
        return f"{self.nama} - {self.sekolah.nama_sekolah}"

class Guru(models.Model):
    # Relasi One-to-One ke model User. Setiap Guru adalah seorang User.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guru_profile')
    nip = models.CharField(max_length=20, unique=True)
    nuptk = models.CharField(max_length=20, unique=True, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=10, choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')])
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    agama = models.CharField(max_length=20, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    no_hp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tanggal_mulai_kerja = models.DateField(blank=True, null=True)
    status_kepegawaian = models.CharField(max_length=20, choices=[('PNS', 'PNS'), ('GTK Honorer', 'GTK Honorer'), ('Guru Yayasan', 'Guru Yayasan')])
    foto = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.nama} ({self.nip})"

class Pegawai(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pegawai_profile')
    nip = models.CharField(max_length=20, unique=True)
    jenis_kelamin = models.CharField(max_length=10, choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')])
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    no_hp = models.CharField(max_length=20, blank=True, null=True)
    jabatan = models.CharField(max_length=100)
    tanggal_mulai_kerja = models.DateField(blank=True, null=True)
    status_kepegawaian = models.CharField(max_length=20, choices=[('PNS', 'PNS'), ('GTK Honorer', 'GTK Honorer'), ('Karyawan Yayasan', 'Karyawan Yayasan')])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.nama} ({self.jabatan})"

class Kelas(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    tingkat = models.IntegerField()
    nama_kelas = models.CharField(max_length=10)
    ruangan = models.CharField(max_length=50, blank=True, null=True)
    wali_kelas = models.OneToOneField(Guru, on_delete=models.SET_NULL, null=True, blank=True, related_name='wali_kelas_profile')

    class Meta:
        unique_together = ('sekolah', 'tingkat', 'nama_kelas')

    def __str__(self):
        return f"{self.tingkat}{self.nama_kelas}"

class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='siswa_profile')
    nis = models.CharField(max_length=20)
    nisn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=10, choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')])
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    agama = models.CharField(max_length=20, blank=True, null=True)
    alamat_jalan = models.TextField(blank=True, null=True)
    rt_rw = models.CharField(max_length=10, blank=True, null=True)
    kelurahan = models.CharField(max_length=50, blank=True, null=True)
    kecamatan = models.CharField(max_length=50, blank=True, null=True)
    kota_kabupaten = models.CharField(max_length=50, blank=True, null=True)
    provinsi = models.CharField(max_length=50, blank=True, null=True)
    kode_pos = models.CharField(max_length=10, blank=True, null=True)
    no_hp_siswa = models.CharField(max_length=20, blank=True, null=True)
    nama_kontak_darurat = models.CharField(max_length=100, blank=True, null=True)
    nomor_kontak_darurat = models.CharField(max_length=20, blank=True, null=True)
    foto = models.CharField(max_length=255, blank=True, null=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.SET_NULL, null=True, blank=True, related_name='siswa')
    status_siswa = models.CharField(max_length=15, choices=[('Aktif', 'Aktif'), ('Pindah', 'Pindah'), ('Lulus', 'Lulus'), ('Cuti', 'Cuti'), ('Dikeluarkan', 'Dikeluarkan')], default='Aktif')
    tanggal_masuk = models.DateField()
    tanggal_keluar = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama} ({self.nis})"

class Ortu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ortu_profile', blank=True, null=True)
    nama_ayah = models.CharField(max_length=100, blank=True, null=True)
    nama_ibu = models.CharField(max_length=100, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    no_hp = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Ayah: {self.nama_ayah}, Ibu: {self.nama_ibu}"

class Alumni(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile', blank=True, null=True)
    nis_lama = models.CharField(max_length=20, blank=True, null=True)
    nama = models.CharField(max_length=100)
    tahun_lulus = models.IntegerField()
    no_hp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    info_terkini = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama} ({self.tahun_lulus})"
    
    # -----------------------------------------------------
# 5. DATA MASTER AKADEMIK & NON-AKADEMIK
# -----------------------------------------------------

class Penerbit(models.Model):
    nama_penerbit = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nama_penerbit

class Mapel(models.Model):
    kode_mapel = models.CharField(max_length=10, unique=True)
    nama_mapel = models.CharField(max_length=100, unique=True)
    kelompok = models.CharField(max_length=50, blank=True, null=True)
    kkm = models.IntegerField(default=75)
    deskripsi = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.kode_mapel} - {self.nama_mapel}"

class Buku(models.Model):
    judul = models.CharField(max_length=255)
    penulis = models.CharField(max_length=100, blank=True, null=True)
    penerbit = models.ForeignKey(Penerbit, on_delete=models.SET_NULL, null=True, blank=True)
    mapel = models.ForeignKey(Mapel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.judul

class Hobi(models.Model):
    nama_hobi = models.CharField(max_length=100, unique=True)
    kategori = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_hobi

class CitaCita(models.Model):
    nama_cita_cita = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nama_cita_cita

# -----------------------------------------------------
# 6. TABEL PENGHUBUNG (MANY-TO-MANY)
# -----------------------------------------------------

class GuruMapel(models.Model):
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, null=True, blank=True) # <-- TAMBAHKAN INI
    buku = models.ForeignKey(Buku, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        # Pastikan satu guru tidak mengajar mapel yang sama di kelas yang sama
        unique_together = ('guru', 'mapel', 'kelas')

    def __str__(self):
        return f"{self.guru.user.nama} - {self.mapel.nama_mapel} ({self.kelas})"

class SiswaOrtu(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    ortu = models.ForeignKey(Ortu, on_delete=models.CASCADE)
    hubungan = models.CharField(max_length=10, choices=[('Ayah', 'Ayah'), ('Ibu', 'Ibu'), ('Wali', 'Wali')])

    def __str__(self):
        return f"{self.siswa.nama} - {self.ortu.nama_ayah} ({self.hubungan})"

class SiswaHobi(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    hobi = models.ForeignKey(Hobi, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.siswa.nama} - {self.hobi.nama_hobi}"

class SiswaCitaCita(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    cita_cita = models.ForeignKey(CitaCita, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.siswa.nama} - {self.cita_cita.nama_cita_cita}"

# -----------------------------------------------------
# 7. TRANSAKSI AKADEMIK & KEUANGAN
# -----------------------------------------------------

# --- Transaksi Akademik ---
# Tempatkan di bagian DATA MASTER
class JamPelajaran(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama_sesi = models.CharField(max_length=50) # 'Jam 1', 'Istirahat', dll.
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    urutan = models.IntegerField()

    class Meta:
        unique_together = ('sekolah', 'urutan')

    def __str__(self):
        return f"{self.nama_sesi} ({self.sekolah.nama_sekolah})"
# Tempatkan di bagian DATA MASTER
class KomponenNilai(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama_komponen = models.CharField(max_length=100)
    jenis = models.CharField(
        max_length=15,
        choices=[('Pengetahuan', 'Pengetahuan'), ('Keterampilan', 'Keterampilan')]
    )
    bobot = models.IntegerField()

    class Meta:
        unique_together = ('sekolah', 'nama_komponen')

    def __str__(self):
        return f"{self.nama_komponen} ({self.sekolah.nama_sekolah})"

class Nilai(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE)
    guru_mapel = models.ForeignKey('GuruMapel', on_delete=models.CASCADE) # Relasi ke tabel penghubung
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    
    # Nilai Akhir (sudah dihitung)
    nilai_akhir_pengetahuan = models.IntegerField(null=True, blank=True)
    nilai_akhir_keterampilan = models.IntegerField(null=True, blank=True)
    predikat_pengetahuan = models.CharField(max_length=10, blank=True, null=True)
    predikat_keterampilan = models.CharField(max_length=10, blank=True, null=True)
    
    # Deskripsi
    deskripsi_pengetahuan = models.TextField(blank=True, null=True)
    deskripsi_keterampilan = models.TextField(blank=True, null=True)
    catatan_sikap = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('siswa', 'mapel', 'tahun_ajaran')

    def __str__(self):
        return f"Nilai {self.siswa.nama} - {self.mapel.nama_mapel} ({self.tahun_ajaran.nama})"
    
    def get_detail_dict(self):
        return {
            detail.komponen_nilai.nama_komponen: detail.skor
            for detail in self.details.all()
        }


class NilaiDetail(models.Model):
    nilai = models.ForeignKey(Nilai, on_delete=models.CASCADE, related_name='details')
    komponen_nilai = models.ForeignKey('KomponenNilai', on_delete=models.CASCADE) # Akan kita buat setelah ini
    skor = models.IntegerField()

    class Meta:
        unique_together = ('nilai', 'komponen_nilai')

    def __str__(self):
        return f"Detail {self.nilai} - {self.komponen_nilai.nama_komponen}"

class Absensi(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    tanggal = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=[('Hadir', 'Hadir'), ('Terlambat', 'Terlambat'), ('Izin', 'Izin'), ('Sakit', 'Sakit'), ('Alpha', 'Alpha')]
    )
    keterangan = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu_input = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('siswa', 'tanggal')

    def __str__(self):
        return f"Absensi {self.siswa.nama} - {self.tanggal} ({self.status})"

class PerizinanSiswa(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tanggal = models.DateField()
    waktu_keluar = models.DateTimeField()
    waktu_kembali = models.DateTimeField(null=True, blank=True)
    alasan = models.TextField(blank=True, null=True)
    keterangan_akhir = models.TextField(blank=True, null=True)
    pemberi_izin = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15,
        choices=[('Keluar', 'Keluar'), ('Kembali', 'Kembali'), ('Tidak Kembali', 'Tidak Kembali')],
        default='Keluar'
    )

    def __str__(self):
        return f"Izin {self.siswa.nama} ({self.status})"
    
    # --- Fitur Dinamis Kelas ---

class OrganisasiKelas(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    jabatan = models.CharField(max_length=50) # 'Ketua Kelas', 'Wakil Ketua', dll.

    class Meta:
        unique_together = ('kelas', 'tahun_ajaran', 'jabatan')

    def __str__(self):
        return f"{self.jabatan} - {self.kelas} ({self.siswa.nama})"

class PiketKelas(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    hari = models.CharField(max_length=10) # 'Senin', 'Selasa', dll.
    tugas = models.CharField(max_length=100, blank=True, null=True) # 'Membersihkan papan tulis'

    class Meta:
        unique_together = ('kelas', 'tahun_ajaran', 'siswa', 'hari')

    def __str__(self):
        return f"Piket {self.hari} - {self.siswa.nama} ({self.kelas})"

class KeuanganKelas(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    tanggal = models.DateField()
    jenis = models.CharField(max_length=20, choices=[('Pemasukan', 'Pemasukan'), ('Pengeluaran', 'Pengeluaran')])
    keterangan = models.TextField()
    nominal = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Guru yang mencatat

    def __str__(self):
        return f"{self.jenis} {self.kelas} - {self.tanggal}"

class ProgramKelas(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    nama_program = models.CharField(max_length=150)
    deskripsi = models.TextField(blank=True, null=True)
    tanggal_mulai = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Rencana', 'Rencana'), ('Berjalan', 'Berjalan'), ('Selesai', 'Selesai'), ('Batal', 'Batal')],
        default='Rencana'
    )

    def __str__(self):
        return f"{self.nama_program} - {self.kelas}"

class LogKelas(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    tanggal = models.DateField()
    isi_log = models.TextField() # "Siswa Ahmad terlambat 15 menit"
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Guru yang mencatat

    def __str__(self):
        return f"Log {self.kelas} - {self.tanggal}"

class JadwalPelajaran(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    hari = models.CharField(max_length=10) # 'Senin', 'Selasa', dll.
    jam_pelajaran = models.ForeignKey('JamPelajaran', on_delete=models.CASCADE) # Akan kita buat
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE)
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('kelas', 'tahun_ajaran', 'hari', 'jam_pelajaran')

    def __str__(self):
        return f"{self.hari} - {self.jam_pelajaran} - {self.mapel.nama_mapel} ({self.kelas})"
    
    # --- Fitur Unit ---

class UnitAnggota(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Untuk guru/pegawai
    tanggal_bergabung = models.DateField()
    jabatan_di_unit = models.CharField(max_length=50, blank=True, null=True) # 'Ketua', 'Anggota', 'Pelatih'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['unit', 'siswa'], name='unique_unit_siswa'),
            models.UniqueConstraint(fields=['unit', 'user'], name='unique_unit_user'),
        ]

    def __str__(self):
        if self.siswa:
            return f"{self.siswa.nama} - {self.unit.nama_unit}"
        return f"{self.user.nama} - {self.unit.nama_unit}"

class UnitKegiatan(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    nama_kegiatan = models.CharField(max_length=200)
    tanggal_mulai = models.DateTimeField(null=True, blank=True)
    tanggal_selesai = models.DateTimeField(null=True, blank=True)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama_kegiatan} - {self.unit.nama_unit}"

class UnitLog(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Yang mencatat log
    tanggal = models.DateTimeField(auto_now_add=True)
    aktivitas = models.TextField() # "Siswa Rina meminjam buku 'Laskar Pelangi'"

    def __str__(self):
        return f"Log {self.unit.nama_unit} - {self.tanggal.strftime('%Y-%m-%d')}"
    
    # --- Output & Laporan ---

class EkstrakurikulerNilai(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    nama_ekskul = models.CharField(max_length=100)
    predikat = models.CharField(max_length=5, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('siswa', 'tahun_ajaran', 'nama_ekskul')

    def __str__(self):
        return f"{self.nama_ekskul} - {self.siswa.nama}"

class Raport(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    jenis_raport = models.CharField(
        max_length=20,
        choices=[('Tengah Semester', 'Tengah Semester'), ('Akhir Semester', 'Akhir Semester')]
    )
    
    # Ringkasan Nilai (Akan diisi oleh logika backend nanti)
    rata_nilai_pengetahuan = models.IntegerField(null=True, blank=True)
    rata_nilai_keterampilan = models.IntegerField(null=True, blank=True)
    ranking_kelas = models.IntegerField(null=True, blank=True)

    # Ringkasan Kehadiran (Akan diisi oleh logika backend nanti)
    total_hadir = models.IntegerField(default=0)
    total_sakit = models.IntegerField(default=0)
    total_izin = models.IntegerField(default=0)
    total_alpha = models.IntegerField(default=0)

    # Catatan & Status
    catatan_wali_kelas = models.TextField(blank=True, null=True)
    catatan_ekstrakurikuler = models.TextField(blank=True, null=True)
    status_raport = models.CharField(
        max_length=20,
        choices=[('Draft', 'Draft'), ('Menunggu Persetujuan', 'Menunggu Persetujuan'), ('Disetujui', 'Disetujui'), ('Diterbitkan', 'Diterbitkan')],
        default='Draft'
    )
    tanggal_disetujui = models.DateTimeField(null=True, blank=True)
    
    # File Output
    pdf_link = models.CharField(max_length=255, blank=True, null=True) # Link ke file PDF
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('siswa', 'tahun_ajaran', 'jenis_raport')

    def __str__(self):
        return f"Raport {self.jenis_raport} - {self.siswa.nama} ({self.tahun_ajaran.nama})"
    
    # --- Transaksi Keuangan ---

class JenisPembayaran(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama_jenis = models.CharField(max_length=100) # 'SPP Bulanan', 'DSP', 'Donasi'
    nominal_default = models.IntegerField()
    is_recurring = models.BooleanField(default=False) # TRUE untuk SPP

    class Meta:
        unique_together = ('sekolah', 'nama_jenis')

    def __str__(self):
        return f"{self.nama_jenis} ({self.sekolah.nama_sekolah})"

class Tagihan(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    jenis_pembayaran = models.ForeignKey(JenisPembayaran, on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    periode = models.CharField(max_length=20) # '2025-01', '2025-02', 'Pendaftaran'
    nominal_tagihan = models.IntegerField()
    tanggal_jatuh_tempo = models.DateField(blank=True, null=True)
    status_tagihan = models.CharField(
        max_length=15,
        choices=[('Belum Lunas', 'Belum Lunas'), ('Lunas', 'Lunas'), ('Dibatalkan', 'Dibatalkan')],
        default='Belum Lunas'
    )

    class Meta:
        unique_together = ('siswa', 'jenis_pembayaran', 'periode')

    def __str__(self):
        return f"Tagihan {self.jenis_pembayaran.nama_jenis} - {self.siswa.nama}"

class PembayaranLog(models.Model):
    tagihan = models.ForeignKey(Tagihan, on_delete=models.CASCADE)
    nominal_dibayar = models.IntegerField()
    tanggal_bayar = models.DateTimeField(auto_now_add=True)
    metode_pembayaran = models.CharField(max_length=20) # 'Tunai', 'Transfer', 'GoPay'
    bukti_pembayaran = models.CharField(max_length=255, blank=True, null=True) # Link ke file
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Bendahara yang mencatat

    def __str__(self):
        return f"Pembayaran {self.tagihan} - {self.nominal_dibayar}"

class PengeluaranLog(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    tanggal_pengeluaran = models.DateField()
    kategori = models.CharField(max_length=50) # 'Operasional', 'Gaji', 'ATK'
    keterangan = models.TextField()
    nominal = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pengeluaran {self.kategori} - {self.nominal}"
    
    # --- Penerimaan Insidentil (Non-Tagihan) ---

class PenerimaanInsidentilLog(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    tanggal_penerimaan = models.DateField()
    kategori = models.CharField(max_length=50) # 'Donasi', 'Penjualan Seragam', 'Lainnya'
    keterangan = models.TextField() # 'Donasi dari Bapak Ahmad untuk rehab perpustakaan'
    nominal = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Yang mencatat (bendahara/kepsek)

    def __str__(self):
        return f"Penerimaan {self.kategori} - {self.nominal}"