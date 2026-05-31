// 1. Definisi Konten Halaman SPA menggunakan Simbol Backtick (`)
const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-md-4 card shadow-sm border-0 p-4">
                <h4 class="text-center fw-bold mb-4">Login Warga</h4>
                <form id="loginForm">
                    <div class="mb-3">
                        <input type="text" id="loginUsername" class="form-control" placeholder="Username" required>
                    </div>
                    <div class="mb-3">
                        <input type="password" id="loginPassword" class="form-control" placeholder="Password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 fw-bold">Masuk</button>
                </form>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button class="btn btn-primary btn-lg w-100 fw-bold mb-3">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card border-0 p-5 shadow-sm text-center text-muted border-dashed" style="border-style: dashed !important; border-width: 2px !important;">
                    <i class="bi bi-inbox fs-1 text-primary mb-3"></i>
                    <h5 class="fw-bold text-dark">Selamat Datang!</h5>
                    <p class="small text-secondary">Koneksi API untuk data laporan akan diimplementasikan pada Lab 12.</p>
                </div>
            </section>

            <aside class="col-lg-3 d-none d-lg-block">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <h6 class="fw-bold text-dark">
                        <i class="bi bi-info-circle-fill text-primary me-2"></i>Pengumuman
                    </h6>
                    <hr>
                    <p class="small text-muted">Aplikasi Client Portal Smart City berbasis Single Page Application (SPA) sedang dalam tahap pengembangan awal.</p>
                </div>
            </aside>
        </div>
    `
};

// 2. Fungsi Utama Pengatur Rute Halaman
function handleRouting() {
    // Ambil hash URL saat ini (misal: #login), jika kosong default ke #login
    const hash = window.location.hash || '#login';
    
    // Ambil elemen container utama dari index.html
    const appContent = document.getElementById('app-content');
    
    // Jika hash ada di dalam daftar rute, suntikkan kodenya. Jika tidak, pakai rute #login
    if (routes[hash]) {
        appContent.innerHTML = routes[hash];
    } else {
        appContent.innerHTML = routes['#login'];
    }

    // Perbarui Menu Navigasi Pojok Kanan Secara Dinamis
    const navMenus = document.getElementById('nav-menus');
    if (hash === '#dashboard') {
        navMenus.innerHTML = `
            <span class="navbar-text me-3 text-white-50">Warga Terautentikasi</span>
            <button onclick="logout()" class="btn btn-outline-light btn-sm fw-bold">
                <i class="bi bi-box-arrow-right me-1"></i>Keluar
            </button>
        `;
    } else {
        navMenus.innerHTML = `
            <a class="btn btn-outline-light btn-sm fw-bold" href="#login">
                <i class="bi bi-box-arrow-in-right me-1"></i>Masuk Portal
            </a>
        `;
    }

    // Jalankan fungsi inisialisasi login dari auth.js jika user berada di halaman login
    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }
}

// 3. Daftarkan Event Listener agar router berjalan otomatis saat URL/hash berubah
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);

// Fungsi pembantu untuk tombol Keluar (Logout) sementara
function logout() {
    localStorage.clear();
    window.location.hash = '#login';
    alert('Log out berhasil!');
}