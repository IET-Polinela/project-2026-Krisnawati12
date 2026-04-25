from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Memanggil Custom User Model yang telah dikonfigurasi [cite: 21]
User = get_user_model()

# --- 1. FORM REGISTRASI KUSTOM ---
# Dibuat untuk menghindari AttributeError pada Custom User Model [cite: 39]
class CitizenRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

# --- 2. FUNGSI REGISTRASI (CITIZEN) ---
def register(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Secara otomatis menetapkan role sebagai Citizen [cite: 13, 40]
            user.is_admin = False 
            user.is_member = True
            user.is_staff = False
            user.save()
            
            messages.success(request, f'Akun {user.username} berhasil dibuat! Silakan melakukan login.')
            return redirect('usermanagement_24782001:login')
        else:
            messages.error(request, "Pendaftaran gagal. Mohon periksa kembali data yang dimasukkan.")
    else:
        form = CitizenRegistrationForm()
    return render(request, 'usermanagement_24782001/register.html', {'form': form})

# --- 3. FUNGSI LOGIN ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Feedback system berdasarkan peran pengguna [cite: 8, 46]
                role = "Admin" if user.is_admin else "Citizen"
                messages.success(request, f"Selamat datang kembali, {username} ({role})!")
                return redirect('main_app:home')
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm()
    return render(request, 'usermanagement_24782001/login.html', {'form': form})

# --- 4. FUNGSI LOGOUT ---
def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah berhasil keluar dari sistem.")
    return redirect('usermanagement_24782001:login')