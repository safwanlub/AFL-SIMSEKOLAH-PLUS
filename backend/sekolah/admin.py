# backend/sekolah/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Yayasan, Sekolah, Unit, TahunAjaran, Guru, Pegawai, Kelas, Siswa, Ortu, Alumni,
    Penerbit, Mapel, Buku, Hobi, CitaCita, GuruMapel, SiswaOrtu, SiswaHobi, SiswaCitaCita, KomponenNilai, Nilai, NilaiDetail, Absensi, PerizinanSiswa,
    JamPelajaran, OrganisasiKelas, PiketKelas, KeuanganKelas, ProgramKelas, LogKelas, JadwalPelajaran,
    UnitAnggota, UnitKegiatan, UnitLog, EkstrakurikulerNilai, Raport, JenisPembayaran, Tagihan, PembayaranLog, PengeluaranLog,
    PenerimaanInsidentilLog
)

# -----------------------------------------------------
# 1. TAMPILKAN USER KUSTOM DI ADMIN
# -----------------------------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Tambahkan field yang ada di model User kita ke tampilan admin
    list_display = ('username', 'nama', 'email', 'role', 'sekolah')
    list_filter = ('role', 'sekolah')
    search_fields = ('username', 'nama', 'email')
    
    # Agar field 'nama' muncul di form tambah/edit user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('nama', 'email', 'sekolah', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nama', 'sekolah', 'role', 'password1', 'password2'),
        }),
    )

# -----------------------------------------------------
# 2. TAMPILKAN MODEL LAINNYA
# -----------------------------------------------------

@admin.register(Yayasan)
class YayasanAdmin(admin.ModelAdmin):
    list_display = ('nama_yayasan', 'no_telp', 'created_at')
    search_fields = ('nama_yayasan',)

@admin.register(Sekolah)
class SekolahAdmin(admin.ModelAdmin):
    list_display = ('nama_sekolah', 'npsn', 'yayasan')
    list_filter = ('yayasan',)
    search_fields = ('nama_sekolah', 'npsn')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('nama_unit', 'jenis_unit', 'sekolah', 'pembina', 'is_active')
    list_filter = ('jenis_unit', 'sekolah', 'is_active')
    search_fields = ('nama_unit',)

# -----------------------------------------------------
# 4. TAMPILKAN MODEL ENTITAS UTAMA
# -----------------------------------------------------

@admin.register(TahunAjaran)
class TahunAjaranAdmin(admin.ModelAdmin):
    list_display = ('nama', 'sekolah', 'status', 'tanggal_mulai', 'tanggal_selesai')
    list_filter = ('sekolah', 'status')
    search_fields = ('nama',)

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('user', 'nip', 'nuptk', 'jenis_kelamin', 'status_kepegawaian', 'is_active')
    list_filter = ('jenis_kelamin', 'status_kepegawaian', 'is_active')
    search_fields = ('user__nama', 'nip', 'nuptk')

@admin.register(Pegawai)
class PegawaiAdmin(admin.ModelAdmin):
    list_display = ('user', 'nip', 'jabatan', 'is_active')
    list_filter = ('jabatan', 'is_active')
    search_fields = ('user__nama', 'nip')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sekolah', 'wali_kelas', 'ruangan')
    list_filter = ('sekolah', 'tingkat')
    search_fields = ('nama_kelas', 'wali_kelas__user__nama')

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nis', 'nisn', 'kelas', 'status_siswa')
    list_filter = ('kelas', 'jenis_kelamin', 'status_siswa')
    search_fields = ('nama', 'nis', 'nisn')

@admin.register(Ortu)
class OrtuAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'no_hp')
    search_fields = ('nama_ayah', 'nama_ibu')

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tahun_lulus', 'sekolah', 'no_hp')
    list_filter = ('sekolah', 'tahun_lulus')
    search_fields = ('nama', 'nis_lama')

    # -----------------------------------------------------
# 5. TAMPILKAN MODEL MASTER
# -----------------------------------------------------

@admin.register(Penerbit)
class PenerbitAdmin(admin.ModelAdmin):
    list_display = ('nama_penerbit',)
    search_fields = ('nama_penerbit',)

@admin.register(Mapel)
class MapelAdmin(admin.ModelAdmin):
    list_display = ('kode_mapel', 'nama_mapel', 'kelompok', 'kkm', 'is_active')
    list_filter = ('kelompok', 'is_active')
    search_fields = ('nama_mapel', 'kode_mapel')

@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penulis', 'penerbit', 'mapel')
    list_filter = ('penerbit', 'mapel')
    search_fields = ('judul', 'penulis')

@admin.register(Hobi)
class HobiAdmin(admin.ModelAdmin):
    list_display = ('nama_hobi', 'kategori')
    list_filter = ('kategori',)
    search_fields = ('nama_hobi',)

@admin.register(CitaCita)
class CitaCitaAdmin(admin.ModelAdmin):
    list_display = ('nama_cita_cita',)
    search_fields = ('nama_cita_cita',)

# -----------------------------------------------------
# 6. TAMPILKAN MODEL PENGHUBUNG
# -----------------------------------------------------

@admin.register(GuruMapel)
class GuruMapelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'buku')
    list_filter = ('guru', 'mapel', 'kelas') # <-- TAMBAHKAN 'kelas'
    search_fields = ('guru__user__nama', 'mapel__nama_mapel', 'kelas__nama_kelas')

@admin.register(SiswaOrtu)
class SiswaOrtuAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('hubungan',)

@admin.register(SiswaHobi)
class SiswaHobiAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('hobi__kategori',)

@admin.register(SiswaCitaCita)
class SiswaCitaCitaAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    # -----------------------------------------------------
# 7. TAMPILKAN MODEL TRANSAKSI AKADEMIK
# -----------------------------------------------------

@admin.register(KomponenNilai)
class KomponenNilaiAdmin(admin.ModelAdmin):
    list_display = ('nama_komponen', 'sekolah', 'jenis', 'bobot')
    list_filter = ('sekolah', 'jenis')
    search_fields = ('nama_komponen',)

@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'mapel', 'tahun_ajaran', 'nilai_akhir_pengetahuan')
    list_filter = ('mapel', 'tahun_ajaran', 'siswa__kelas')
    search_fields = ('siswa__nama', 'mapel__nama_mapel')

@admin.register(NilaiDetail)
class NilaiDetailAdmin(admin.ModelAdmin):
    list_display = ('nilai', 'komponen_nilai', 'skor')
    list_filter = ('komponen_nilai',)

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'tanggal', 'status', 'kelas')
    list_filter = ('status', 'kelas', 'tanggal')
    search_fields = ('siswa__nama',)

@admin.register(PerizinanSiswa)
class PerizinanSiswaAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'tanggal', 'status', 'pemberi_izin')
    list_filter = ('status', 'tanggal')
    search_fields = ('siswa__nama',)

    # -----------------------------------------------------
# 8. TAMPILKAN MODEL FITUR DINAMIS KELAS
# -----------------------------------------------------

@admin.register(JamPelajaran)
class JamPelajaranAdmin(admin.ModelAdmin):
    list_display = ('nama_sesi', 'sekolah', 'jam_mulai', 'jam_selesai', 'urutan')
    list_filter = ('sekolah',)
    search_fields = ('nama_sesi',)

@admin.register(OrganisasiKelas)
class OrganisasiKelasAdmin(admin.ModelAdmin):
    list_display = ('jabatan', 'siswa', 'kelas', 'tahun_ajaran')
    list_filter = ('jabatan', 'kelas', 'tahun_ajaran')
    search_fields = ('siswa__nama',)

@admin.register(PiketKelas)
class PiketKelasAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'hari', 'tugas', 'kelas')
    list_filter = ('hari', 'kelas')
    search_fields = ('siswa__nama',)

@admin.register(KeuanganKelas)
class KeuanganKelasAdmin(admin.ModelAdmin):
    list_display = ('kelas', 'tanggal', 'jenis', 'nominal')
    list_filter = ('jenis', 'kelas', 'tanggal')
    search_fields = ('keterangan',)

@admin.register(ProgramKelas)
class ProgramKelasAdmin(admin.ModelAdmin):
    list_display = ('nama_program', 'kelas', 'status', 'tanggal_mulai')
    list_filter = ('status', 'kelas')
    search_fields = ('nama_program',)

@admin.register(LogKelas)
class LogKelasAdmin(admin.ModelAdmin):
    list_display = ('kelas', 'tanggal', 'isi_log')
    list_filter = ('kelas', 'tanggal')
    search_fields = ('isi_log',)

@admin.register(JadwalPelajaran)
class JadwalPelajaranAdmin(admin.ModelAdmin):
    list_display = ('hari', 'kelas', 'jam_pelajaran', 'mapel', 'guru')
    list_filter = ('hari', 'kelas', 'mapel')
    search_fields = ('mapel__nama_mapel', 'guru__user__nama')

    # -----------------------------------------------------
# 9. TAMPILKAN MODEL FITUR UNIT
# -----------------------------------------------------

@admin.register(UnitAnggota)
class UnitAnggotaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tanggal_bergabung', 'jabatan_di_unit')
    list_filter = ('unit', 'jabatan_di_unit')
    search_fields = ('siswa__nama', 'user__nama')

@admin.register(UnitKegiatan)
class UnitKegiatanAdmin(admin.ModelAdmin):
    list_display = ('nama_kegiatan', 'unit', 'tanggal_mulai')
    list_filter = ('unit', 'tanggal_mulai')
    search_fields = ('nama_kegiatan',)

@admin.register(UnitLog)
class UnitLogAdmin(admin.ModelAdmin):
    list_display = ('unit', 'tanggal', 'aktivitas')
    list_filter = ('unit', 'tanggal')
    search_fields = ('aktivitas',)

    # -----------------------------------------------------
# 10. TAMPILKAN MODEL OUTPUT & LAPORAN
# -----------------------------------------------------

@admin.register(EkstrakurikulerNilai)
class EkstrakurikulerNilaiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'nama_ekskul', 'predikat', 'tahun_ajaran')
    list_filter = ('predikat', 'nama_ekskul', 'tahun_ajaran')
    search_fields = ('siswa__nama',)

@admin.register(Raport)
class RaportAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'tahun_ajaran', 'jenis_raport', 'status_raport', 'created_at')
    list_filter = ('jenis_raport', 'status_raport', 'tahun_ajaran')
    search_fields = ('siswa__nama',)
    # Kita akan buat field ini read-only di form agar tidak diubah manual
    readonly_fields = ('rata_nilai_pengetahuan', 'rata_nilai_keterampilan', 'ranking_kelas', 'total_hadir', 'total_sakit', 'total_izin', 'total_alpha')

    # -----------------------------------------------------
# 11. TAMPILKAN MODEL TRANSAKSI KEUANGAN
# -----------------------------------------------------

@admin.register(JenisPembayaran)
class JenisPembayaranAdmin(admin.ModelAdmin):
    list_display = ('nama_jenis', 'sekolah', 'nominal_default', 'is_recurring')
    list_filter = ('sekolah', 'is_recurring')
    search_fields = ('nama_jenis',)

@admin.register(Tagihan)
class TagihanAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'jenis_pembayaran', 'periode', 'nominal_tagihan', 'status_tagihan')
    list_filter = ('status_tagihan', 'jenis_pembayaran', 'periode')
    search_fields = ('siswa__nama',)

@admin.register(PembayaranLog)
class PembayaranLogAdmin(admin.ModelAdmin):
    list_display = ('tagihan', 'nominal_dibayar', 'tanggal_bayar', 'metode_pembayaran')
    list_filter = ('metode_pembayaran', 'tanggal_bayar')
    search_fields = ('tagihan__siswa__nama',)

@admin.register(PengeluaranLog)
class PengeluaranLogAdmin(admin.ModelAdmin):
    list_display = ('tanggal_pengeluaran', 'kategori', 'nominal', 'sekolah')
    list_filter = ('kategori', 'sekolah', 'tanggal_pengeluaran')
    search_fields = ('keterangan',)

    # -----------------------------------------------------
# 12. TAMPILKAN MODEL PENERIMAAN INSIDENTIL
# -----------------------------------------------------

@admin.register(PenerimaanInsidentilLog)
class PenerimaanInsidentilLogAdmin(admin.ModelAdmin):
    list_display = ('tanggal_penerimaan', 'kategori', 'nominal', 'sekolah')
    list_filter = ('kategori', 'sekolah', 'tanggal_penerimaan')
    search_fields = ('keterangan',)