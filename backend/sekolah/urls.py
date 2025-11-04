# C:\AFL-SSPLUS\backend\sekolah\urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 🔐 Auth & Dashboard
    path('login/', views.login, name='login'),
    path('stats/', views.get_stats_api, name='get_stats_api'),

    # 🎓 Data Akademik
    path('get-kelas-list/', views.get_kelas_list_api, name='get_kelas_list_api'),
    path('get-mapel-list/', views.get_mapel_list_api, name='get_mapel_list_api'),
    path('get-tahun-ajaran-list/', views.get_tahun_ajaran_list, name='get-tahun-ajaran-list'),

    # 🧮 Nilai Siswa
    path('get-students-with-nilai/', views.get_students_with_nilai_api, name='get_students_with_nilai_api'),
    path('save-nilai/', views.save_nilai, name='save_nilai'), # <--- HANYA SATU INI!
    path('get-guru-mapel-list/', views.get_guru_mapel_list, name='get-guru-mapel-list'),

    

]
