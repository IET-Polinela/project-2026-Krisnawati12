function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Mencegah reload halaman

        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        try {
            // Kirim payload ke endpoint JWT Django
            const response = await requestAPI('/api/token/', 'POST', {
                username: usernameInput,
                password: passwordInput
            });

            console.log('Login Response:', response);

            // PERBAIKAN: gunakan status, bukan response.ok
            if (response.status === 200 && response.data?.access) {

                // Simpan token
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                localStorage.setItem('username', usernameInput);

                alert(`Sukses! Selamat datang, ${usernameInput}!`);

                // Pindah ke dashboard
                window.location.hash = '#dashboard';

            } else {

                const errorMsg =
                    response?.data?.detail ||
                    'Username atau password salah.';

                alert(`Gagal: ${errorMsg}`);
            }

        } catch (error) {
            console.error('Login Error:', error);
            alert('Terjadi kesalahan saat menghubungi server.');
        }
    });
}

function setupRegisterForm() {
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) return;

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('registerUsername').value.trim();
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;

        if (!username || !password) {
            alert('Username dan password wajib diisi.');
            return;
        }

        try {
            const payload = { username, password };
            if (email) payload.email = email;

            const response = await requestAPI('/api/register/', 'POST', payload);

            if (response.status === 201 || response.status === 200) {
                alert('Registrasi berhasil. Silakan login.');
                window.location.hash = '#login';
            } else {
                const errorMsg = response?.data?.detail || JSON.stringify(response?.data || 'Registrasi gagal.');
                alert(`Gagal: ${errorMsg}`);
            }
        } catch (error) {
            console.error('Register Error:', error);
            alert('Terjadi kesalahan saat menghubungi server.');
        }
    });
}
