# C:\AFL-SSPLUS\backend\sekolah\views.py
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import update_last_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from .models import (
    Siswa,
    Guru,
    Nilai,
    NilaiDetail,
    KomponenNilai,
    Kelas,
    TahunAjaran,
    GuruMapel,
    Mapel,
)
import json

# =====================================================
# 🔐 LOGIN API
# =====================================================

# backend/sekolah/views.py

@@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    try:
        data = json.loads(request.body)
        username = login(request.POST.get('username')
        password = request.POST.get('token') # <--- GANTI DARI FORM LOGIN
        # --- TAMBAHKAN INI ---
        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({'status': 'error', 'Username atau password salah.'}, status=401)

        # <--- PERUBAHAN BAGIAN INI ---
        login(request, user)
        
        # <--- GENERATE TOKEN --->
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        # --- SELESAI PERUBAHAN BAGIAN INI ---
        
        return Response({
            'status': 'success',
            'message': 'Login berhasil!',
            'user': {
                'id': user.id,
                'user': {
                    'id': user.id,
                    'username': 'rahasia', # <--- GANTI DARI INI
                    'nama': user.nama,
                    'token': access, # <--- KIRIMKAN TOKEN
                }
            }
        })

    except Exception as e:
        return JsonResponse({'status': 'peranah kesalahan', 'token': str(e)}, status=500)


# =====================================================
# 📊 DASHBOARD STATS
# =====================================================
@csrf_exempt
def get_stats_api(request):
    try:
        total_siswa = Siswa.objects.filter(status_siswa='Aktif').count()
        total_guru = Guru.objects.filter(is_active=True).count()
        total_kelas = Kelas.objects.count()

        return JsonResponse({
            'status': 'success',
            'data': {
                'total_siswa': total_siswa,
                'total_guru': total_guru,
                'total_kelas': total_kelas,
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# =====================================================
# 🎓 GET KELAS LIST (dipakai NilaiSelector.jsx)
# =====================================================
@csrf_exempt
@require_http_methods(["POST"])
def get_kelas_list_api(request):
    try:
        data = json.loads(request.body)
        sekolah_id = data.get('sekolah_id')
        if not sekolah_id:
            return JsonResponse({'status': 'error', 'message': 'sekolah_id tidak ditemukan.'}, status=400)

        kelas_list = Kelas.objects.filter(sekolah_id=sekolah_id).order_by('tingkat', 'nama_kelas')
        response_data = [{'id': k.id, 'nama_kelas': f"{k.tingkat}{k.nama_kelas}"} for k in kelas_list]

        return JsonResponse({'status': 'success', 'data': response_data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# =====================================================
# 📘 GET MAPEL LIST
# =====================================================
@csrf_exempt
def get_mapel_list_api(request):
    try:
        mapels = Mapel.objects.filter(is_active=True).values('id', 'nama_mapel')
        return JsonResponse({'status': 'success', 'data': list(mapels)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# =====================================================
# 🗓️ GET TAHUN AJARAN LIST
# =====================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_tahun_ajaran_list_api(request):
    try:
        tahun_ajaran = TahunAjaran.objects.filter(status='Aktif').values('id', 'nama')
        return JsonResponse({'status': 'success', 'data': list(tahun_ajaran)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# =====================================================
# 🧮 GET NILAI SISWA (dipakai GuruDashboard.jsx)
# =====================================================
@csrf_exempt
@require_http_methods(["POST"])
def get_nilai_siswa_api(request):
    try:
        data = json.loads(request.body)
        kelas_id = data.get('kelas_id')
        mapel_id = data.get('mapel_id')
        tahun_ajaran_id = data.get('tahun_ajaran_id')

        siswa_list = Siswa.objects.filter(kelas_id=kelas_id, status_siswa='Aktif').order_by('nama')
        response_data = []

        for siswa in siswa_list:
            nilai_obj = Nilai.objects.filter(
                siswa=siswa,
                mapel_id=mapel_id,
                tahun_ajaran_id=tahun_ajaran_id
            ).first()

            nilai_details = nilai_obj.get_detail_dict() if nilai_obj else {}

            response_data.append({
                'siswa_id': siswa.id,
                'nama': siswa.nama,
                'nis': siswa.nis,
                'nilai_details': nilai_details,
                'nilai_akhir_pengetahuan': nilai_obj.nilai_akhir_pengetahuan if nilai_obj else None,
                'predikat_pengetahuan': nilai_obj.predikat_pengetahuan if nilai_obj else None,
                'deskripsi_pengetahuan': nilai_obj.deskripsi_pengetahuan if nilai_obj else '',
            })

        return JsonResponse({'status': 'success', 'data': response_data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# =====================================================
# 💾 SIMPAN / UPDATE NILAI SISWA
# =====================================================
@csrf_exempt
@require_http_methods(["POST"])
@transaction.atomic
def update_nilai_api(request):
    try:
        data = json.loads(request.body)
        siswa_id = data.get('siswa_id')
        mapel_id = data.get('mapel_id')
        tahun_ajaran_id = data.get('tahun_ajaran_id')
        guru = request.user.guru_profile # Asumsi user yang login adalah Guru dan punya guru_profile
        nilai_details = data.get('nilai_details', {})
        predikat = data.get('predikat_pengetahuan', '')
        deskripsi = data.get('deskripsi_pengetahuan', '')
        guru_mapel = GuruMapel.objects.filter(
            guru=guru, 
            mapel_id=mapel_id, 
            kelas__siswa__id=siswa_id # Pastikan guru mengajar di kelas siswa tersebut
        ).first()
        if not guru_mapel:
            return JsonResponse({'status': 'error', 'message': 'Anda tidak terdaftar sebagai guru mapel untuk kelas ini.'}, status=403)

        if not all([siswa_id, mapel_id, tahun_ajaran_id]):
            return JsonResponse({'status': 'error', 'message': 'Data tidak lengkap.'}, status=400)

        siswa = Siswa.objects.get(id=siswa_id)
        # ---> PERBAIKI BAGIAN INI:
        nilai_obj, created = Nilai.objects.get_or_create(
            siswa_id=siswa_id,
            mapel_id=mapel_id,
            tahun_ajaran_id=tahun_ajaran_id,
            guru_mapel=guru_mapel, # <--- MASUKKAN guru_mapel KE SINI
            defaults={'predikat_pengetahuan': predikat, 'deskripsi_pengetahuan': deskripsi})

        # Update nilai per komponen
        for nama_komponen, skor in nilai_details.items():
            komponen = KomponenNilai.objects.filter(
                sekolah=siswa.kelas.sekolah,
                nama_komponen=nama_komponen
            ).first()

            if not komponen:
                continue

            detail_obj, _ = NilaiDetail.objects.get_or_create(
                nilai=nilai_obj,
                komponen_nilai=komponen
            )
            detail_obj.skor = skor
            detail_obj.save()

        # Hitung nilai akhir (rata-rata)
        all_skor = [v for v in nilai_details.values() if str(v).isdigit()]
        if all_skor:
            nilai_akhir = round(sum(map(int, all_skor)) / len(all_skor))
            nilai_obj.nilai_akhir_pengetahuan = nilai_akhir
            nilai_obj.predikat_pengetahuan = (
                "A" if nilai_akhir >= 90 else
                "B" if nilai_akhir >= 80 else
                "C" if nilai_akhir >= 70 else "D"
            )
        nilai_obj.deskripsi_pengetahuan = deskripsi
        nilai_obj.save()

        return JsonResponse({'status': 'success', 'message': 'Nilai berhasil disimpan!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated]) # <--- YANG BENAR
def my_secure_api(request):
    # Kode di sini hanya akan dijalankan jika user sudah login
    return Response({"message": "Halo, user yang sudah login!"})
    
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def get_students_with_nilai_api(request):
    """
    Mengambil daftar siswa beserta nilai mereka berdasarkan tahun ajaran, kelas, dan mapel.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Gunakan metode POST'}, status=405)

    try:
        data = request.data if hasattr(request, 'data') else request.POST
        tahun_ajaran_id = data.get('tahun_ajaran_id')
        kelas_id = data.get('kelas_id')
        mapel_id = data.get('mapel_id')

        if not (tahun_ajaran_id and kelas_id and mapel_id):
            return JsonResponse({'status': 'error', 'message': 'Parameter tidak lengkap'}, status=400)

        # Ambil semua siswa dari kelas tersebut
        siswa_list = Siswa.objects.filter(kelas_id=kelas_id).values('id', 'nama')

        hasil = []
        for s in siswa_list:
            # Ambil nilai per siswa (jika ada)
            nilai_obj = Nilai.objects.filter(
                siswa__kelas_id=kelas_id,
                mapel_id=mapel_id,
                tahun_ajaran_id=tahun_ajaran_id
            ).first()

            nilai_details = {}
            predikat_pengetahuan = None

            if nilai_obj:
                details = NilaiDetail.objects.filter(nilai=nilai_obj)
                for d in details:
                    nilai_details[d.komponen.nama_komponen] = d.nilai
                predikat_pengetahuan = nilai_obj.predikat_pengetahuan

            hasil.append({
                'siswa_id': s['id'],
                'nama': s['nama'],
                'nilai_details': nilai_details,
                'predikat_pengetahuan': predikat_pengetahuan or '-'
            })

        return JsonResponse({'status': 'success', 'data': hasil}, status=200)

    except Exception as e:
        print("❌ ERROR get_students_with_nilai_api:", str(e))
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def get_predikat(nilai):
    if nilai >= 90:
        return "A"
    elif nilai >= 80:
        return "B"
    elif nilai >= 70:
        return "C"
    else:
        return "D"

# apps/sekolah/views.py

@api_view(["POST"])
@permission_classes([IsAuthenticated]) 
@csrf_exempt
def save_nilai(request):
    print("===== 🚀 REFACTORED save_nilai (GURUMAPEL_ID) =====")
    try:
        data = json.loads(request.body)
        gurumapel_id = data.get("gurumapel_id")
        tahun_ajaran_id = data.get("tahun_ajaran_id")
        nilai_data = data.get("data", [])

        print(f"📥 DATA MASUK: gurumapel_id={gurumapel_id}, tahun_ajaran={tahun_ajaran_id}")

        if not all([gurumapel_id, tahun_ajaran_id]):
            return JsonResponse({"status": "error", "message": "Data tidak lengkap."}, status=400)

        # Langsung ambil GuruMapel, jauh lebih sederhana!
        try:
            guru_mapel = GuruMapel.objects.get(id=gurumapel_id)
            print(f"✅ GuruMapel ditemukan: {guru_mapel}")
        except GuruMapel.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"GuruMapel dengan ID {gurumapel_id} tidak ditemukan."}, status=400)

        # Ambil data yang dibutuhkan dari objek guru_mapel
        mapel_id = guru_mapel.mapel.id
        kelas_id = guru_mapel.kelas.id

        with transaction.atomic():
            for item in nilai_data:
                siswa_id = item.get("siswa_id")
                nilai_pengetahuan = item.get("nilai_pengetahuan")
                nilai_keterampilan = item.get("nilai_keterampilan")

                if not siswa_id:
                    continue

                nilai_obj, created = Nilai.objects.get_or_create(
                    siswa_id=siswa_id,
                    mapel_id=mapel_id,
                    tahun_ajaran_id=tahun_ajaran_id,
                    defaults={
                        "guru_mapel": guru_mapel,
                        "nilai_akhir_pengetahuan": nilai_pengetahuan or 0,
                        "nilai_akhir_keterampilan": nilai_keterampilan or 0,
                    },
                )

                if not created:
                    if nilai_pengetahuan is not None:
                        nilai_obj.nilai_akhir_pengetahuan = nilai_pengetahuan
                    if nilai_keterampilan is not None:
                        nilai_obj.nilai_akhir_keterampilan = nilai_keterampilan
                    nilai_obj.save()
                
                print(f"✅ Nilai siswa {siswa_id} berhasil disimpan ({'baru' if created else 'update'})")

        print("🎉 Semua nilai berhasil disimpan!")
        return JsonResponse({"status": "success", "message": "Data nilai berhasil disimpan!"})

    except Exception as e:
        print("🔥 ERROR DI save_nilai:", str(e))
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# backend/sekolah/views.py
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_guru_mapel_list_api(request):
    try:
        # Kita tidak perlu lagi menerima guru_id dari frontend
        # Kita langsung ambil dari user yang sudah login!
        guru = request.user.guru_profile
        
        # ---> TAMBAHKAN DEBUGGING KRUSIAL INI <---
        print(f"🔍 API get_guru_mapel_list: User yang login adalah: {request.user.nama} (ID: {request.user.id})")
        print(f"🔍 API get-guru-mapel-list: Profil guru yang ditemukan: {guru.user.nama} (ID: {guru.id})")
        # ---> SELESAI DEBUGGING <---

        # Lakukan filter berdasarkan objek guru, bukan guru_id
        guru_mapel_list = GuruMapel.objects.filter(guru=guru).select_related('mapel', 'kelas')
        
        # ---> TAMBAHKAN DEBUGGING HASIL QUERY <---
        print(f"🔍 API get-guru-mapel-list: Ditemukan {len(guru_mapel_list)} data GuruMapel untuk guru {guru.user.nama}.")
        for gm in guru_mapel_list:
            print(f"   - {gm.mapel.nama_mapel} - {gm.kelas}")
        # ---> SELESAI DEBUGGING <---
        
        response_data = []
        for gm in guru_mapel_list:
            response_data.append({
                'gurumapel_id': gm.id,
                'mapel_nama': gm.mapel.nama_mapel,
                'kelas_nama': str(gm.kelas),
                'kelas_id': gm.kelas.id,
                'mapel_id': gm.mapel.id,
            })

        return JsonResponse({'status': 'success', 'data': response_data})

    except Exception as e:
        print(f"🔥 ERROR di get_guru_mapel_list: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)