from django.contrib import admin
from .models import *

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nis', 'nama', 'jenis_kelamin', 'tanggal_lahir', 'kelas', 'alamat', 'created_at')

@admin.register(Kriteria)
class KriteriaAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama', 'bobot', 'jenis', 'deskripsi')

@admin.register(Penilaian)
class PenilaianAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'kriteria', 'nilai', 'created_at')

@admin.register(HasilWP)
class HasilWPAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'vector_s', 'vector_v', 'ranking', 'tanggal_hitung', 'versi')


# Register your models here.
