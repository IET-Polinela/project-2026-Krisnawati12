function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Mencegah password bocor ke URL / reload halaman

        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        // Kirim payload ke endpoint Django sesuai instruksi
        const response = await requestAPI('/api/token/', 'POST', {
            username: usernameInput,
            password: passwordInput
        });

        if (response.ok && response.data.access) {
            // Simpan access dan refresh token ke localStorage
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('username', usernameInput);

            alert(`Sukses! Selamat datang, ${usernameInput}!`);
            
            // Ubah rute secara instan ke dashboard
            window.location.hash = '#dashboard';
        } else {
            const errorMsg = response.data.detail || 'Username atau password salah.';
            alert(`Gagal: ${errorMsg}`);
        }
    });
}