from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Siswa, Kriteria, Penilaian, HasilWP, AdminProfile
from django.core.exceptions import ValidationError
from django.utils import timezone

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class SiswaForm(forms.ModelForm):
    # tanggal_lahir = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     initial=timezone.now().date()
    # )

    class Meta:
        model = Siswa
        fields = "__all__"
        widgets = {
            'nis': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Masukkan NIS',
                'autocomplete': 'off'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Masukkan Nama',
                'autocomplete': 'off'
            }),
            'jenis_kelamin': forms.Select(attrs={
                'class': 'form-select rounded-pill'
            }),
            'tanggal_lahir': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control rounded-pill'
            }),
            'kelas': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Masukkan Kelas',
                'autocomplete': 'off'
            }),
            'alamat': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control rounded-4',
                'placeholder': 'Masukkan Alamat',
                'style': 'resize:none;',
                'autocomplete': 'off'
            }),
        }

    def clean_nis(self):
        nis = self.cleaned_data['nis']
        if len(nis) != 10:
            raise ValidationError("NIS harus terdiri dari 10 digit angka")
        return nis

class KriteriaForm(forms.ModelForm):
    class Meta:
        model = Kriteria
        fields = '__all__'
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Kode'}),
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Nama Kriteria'}),
            'jenis': forms.Select(attrs={'class': 'form-control'}),
            'bobot': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Masukkan Bobot'}),
            'deskripsi': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Masukkan Deskripsi'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bobot'].widget.attrs.update({'step': '0.01'})

class PenilaianForm(forms.ModelForm):
    class Meta:
        model = Penilaian
        fields = ['siswa', 'kriteria', 'nilai']
        widgets = {
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'kriteria': forms.Select(attrs={'class': 'form-control'}),
            'nilai': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control', 'placeholder': 'Masukkan Nilai'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['siswa'].queryset = Siswa.objects.all().order_by('nama')
        self.fields['kriteria'].queryset = Kriteria.objects.all().order_by('kode')


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['phone']

class WPCalculationForm(forms.Form):
    judul_perhitungan = forms.CharField(max_length=100, required=True)
    deskripsi = forms.CharField(widget=forms.Textarea, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['judul_perhitungan'].widget.attrs.update({
            'placeholder': 'Misal: Perhitungan Semester Ganjil 2023'
        })
        self.fields['deskripsi'].widget.attrs.update({
            'rows': 3,
            'placeholder': 'Deskripsi tambahan tentang perhitungan ini'
        })