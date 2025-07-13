from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# ==== Constants ====
JENIS_KELAMIN = [('L', 'Laki-laki'), ('P', 'Perempuan')]
JENIS_KRITERIA = [('benefit', 'Benefit'), ('cost', 'Cost')]

# ==== Admin Profile ====
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

# ==== Siswa ====
class Siswa(models.Model):
    nis = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d+$', 'NIS hanya boleh angka')]
    )
    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    tanggal_lahir = models.DateField()
    alamat = models.CharField(max_length=255, blank=True)
    kelas = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nis} - {self.nama}"

    def clean(self):
        if self.tanggal_lahir > timezone.now().date():
            raise ValidationError("Tanggal lahir tidak boleh di masa depan.")

# ==== Kriteria ====
class Kriteria(models.Model):
    kode = models.CharField(max_length=5, unique=True)
    nama = models.CharField(max_length=50)
    bobot = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Bobot total semua kriteria harus <= 1.0"
    )
    jenis = models.CharField(max_length=7, choices=JENIS_KRITERIA)
    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return f"{self.kode} - {self.nama} ({self.jenis})"

# ==== Penilaian Siswa ====
class Penilaian(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='penilaian')
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='penilaian')
    nilai = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Nilai antara 0 - 100"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.siswa.nama} - {self.kriteria.nama}: {self.nilai}"

    class Meta:
        unique_together = ('siswa', 'kriteria')

# ==== Hasil Perhitungan WP ====
class HasilWP(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='hasil_wp')
    vector_s = models.FloatField(validators=[MinValueValidator(0.0)])
    vector_v = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    ranking = models.PositiveIntegerField()
    detail_perhitungan = models.JSONField(blank=True, null=True)
    tanggal_hitung = models.DateTimeField(auto_now_add=True)
    versi = models.CharField(max_length=10, default="1.0")

    def __str__(self):
        return f"{self.siswa.nama} - Rank {self.ranking}"

    class Meta:
        ordering = ['ranking']

# ==== Log Aktivitas (Opsional) ====
class LogAktivitas(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aksi = models.CharField(max_length=20)
    objek = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonim'} - {self.aksi} {self.objek}"

    class Meta:
        ordering = ['-timestamp']
