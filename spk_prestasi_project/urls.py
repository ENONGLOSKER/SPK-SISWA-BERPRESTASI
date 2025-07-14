"""
URL configuration for spk_prestasi_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spk_prestasi_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # import file excel
    path('import_siswa/', views.import_siswa, name='import_siswa'),
    # path('import_kriteria/', views.import_kriteria, name='import_kriteria'),
    # path('import_penilaian/', views.import_penilaian, name='import_penilaian'),

    # siswa
    path('siswa/', views.siswa_list, name='siswa_list'),
    path('siswa/add/', views.siswa_add, name='siswa_add'),
    path('siswa/update/<int:id>/', views.siswa_update, name='siswa_update'),
    path('siswa/delete/<int:id>/', views.siswa_delete, name='siswa_delete'),
    # kriteria
    path('kriteria/', views.kriteria_list, name='kriteria_list'),
    path('kriteria/add/', views.kriteria_add, name='kriteria_add'),
    path('kriteria/update/<int:id>/', views.kriteria_update, name='kriteria_update'),
    path('kriteria/delete/<int:id>/', views.kriteria_delete, name='kriteria_delete'),
    # penilaian
    path('penilaian/', views.penilaian_list, name='penilaian_list'),
    path('penilaian/add/', views.penilaian_add, name='penilaian_add'),
    path('penilaian/update/<int:id>/', views.penilaian_update, name='penilaian_update'),
    path('penilaian/delete/<int:id>/', views.penilaian_delete, name='penilaian_delete'),
    # hasil_wp
    path('hasil/wp/', views.hasil_wp_list, name='hasil_wp'),
    path('hasil/wp/detail/<int:id>/', views.hasil_wp_detail, name='detail_hasil_wp'),
    path('hitung/wp/', views.perhitungan_wp, name='hitung_wp'),
    path('reset/hasil/', views.reset_perhitungan, name='reset_perhitungan'),

]
