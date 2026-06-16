const routes = {
    '#login': `
        <section class="auth-shell">
            <div class="auth-card">
                <div class="text-center mb-4">
                    <i class="bi bi-buildings-fill fs-1"></i>
                    <h4 class="fw-bold mt-3 mb-1">Masuk Portal Warga</h4>
                    <p class="text-muted mb-0">Kelola laporan kota dari satu dashboard.</p>
                </div>
                <form id="loginForm">
                    <div class="mb-3">
                        <label for="loginUsername" class="form-label">Username</label>
                        <input type="text" id="loginUsername" class="form-control" placeholder="Masukkan username" required>
                    </div>

                    <div class="mb-4">
                        <label for="loginPassword" class="form-label">Password</label>
                        <input type="password" id="loginPassword" class="form-control" placeholder="Masukkan password" required>
                    </div>

                    <button type="submit" class="btn btn-premium w-100 fw-bold">
                        Masuk
                    </button>
                </form>
                <div class="text-center mt-4">
                    <span class="text-muted small">Belum punya akun?</span>
                    <a href="#register" class="fw-bold text-decoration-none ms-1" style="color: var(--accent-teal);">Daftar Sekarang</a>
                </div>
            </div>
        </section>
    `,

    '#register': `
        <section class="auth-shell">
            <div class="auth-card">
                <div class="text-center mb-4">
                    <i class="bi bi-person-plus-fill fs-1"></i>
                    <h4 class="fw-bold mt-3 mb-1">Daftar Pengguna Baru</h4>
                    <p class="text-muted mb-0">Buat akun untuk mulai mengirim laporan.</p>
                </div>
                <form id="registerForm">
                    <div class="mb-3">
                        <label for="registerUsername" class="form-label">Username</label>
                        <input type="text" id="registerUsername" class="form-control" placeholder="Pilih username" required>
                    </div>

                    <div class="mb-3">
                        <label for="registerEmail" class="form-label">Email</label>
                        <input type="email" id="registerEmail" class="form-control" placeholder="nama@email.com">
                    </div>

                    <div class="mb-4">
                        <label for="registerPassword" class="form-label">Password</label>
                        <input type="password" id="registerPassword" class="form-control" placeholder="Buat password" required>
                    </div>

                    <button type="submit" class="btn btn-premium w-100 fw-bold">
                        Daftar
                    </button>
                </form>
                <div class="text-center mt-4">
                    <span class="text-muted small">Sudah punya akun?</span>
                    <a href="#login" class="fw-bold text-decoration-none ms-1">Masuk Portal</a>
                </div>
            </div>
        </section>
    `,

    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="floating-panel p-3">
                    <h6 class="fw-bold mb-3"><i class="bi bi-bar-chart-line-fill me-2"></i>Statistik</h6>
                    <div class="d-grid gap-2">
                        <div class="stat-row d-flex align-items-center justify-content-between p-2">
                            <small class="text-muted">Draft</small>
                            <span id="statDraft" class="stat-badge stat-draft">0</span>
                        </div>
                        <div class="stat-row d-flex align-items-center justify-content-between p-2">
                            <small class="text-muted">Reported</small>
                            <span id="statReported" class="stat-badge stat-reported">0</span>
                        </div>
                        <div class="stat-row d-flex align-items-center justify-content-between p-2">
                            <small class="text-muted">Verified</small>
                            <span id="statVerified" class="stat-badge stat-verified">0</span>
                        </div>
                        <div class="stat-row d-flex align-items-center justify-content-between p-2">
                            <small class="text-muted">In Progress</small>
                            <span id="statInProgress" class="stat-badge stat-progress">0</span>
                        </div>
                        <div class="stat-row d-flex align-items-center justify-content-between p-2">
                            <small class="text-muted">Resolved</small>
                            <span id="statResolved" class="stat-badge stat-resolved">0</span>
                        </div>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="floating-panel p-4 text-center mb-4">
                    <i class="bi bi-shield-check fs-1" style="color: #00f2fe;"></i>
                    <h5 class="fw-bold mt-2">Autentikasi Berhasil Terhubung</h5>
                    <p class="text-muted small mb-0">Seluruh fitur pelaporan siap digunakan.</p>
                </div>

                <div id="listContainer" class="row"></div>
                <nav><ul id="paginationContainer" class="pagination justify-content-center mt-4"></ul></nav>
            </section>

            <aside class="col-12 col-lg-3">
                <div class="floating-panel p-3">
                    <button id="btnAddReport" type="button" class="btn btn-premium btn-lg w-100 fw-bold mb-3">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>

                    <div class="list-group sub-nav-group">
                        <button type="button" class="list-group-item list-group-item-action text-white active" id="menuMyReports">
                            <i class="bi bi-list-task me-2"></i>Laporan Saya
                        </button>
                        <button type="button" class="list-group-item list-group-item-action text-white" id="menuFeed">
                            <i class="bi bi-globe me-2"></i>Feed Kota
                        </button>
                    </div>
                </div>
            </aside>
        </div>
    `
};

function handleRouting() {
    const hash = window.location.hash || '#login';
    const appContent = document.getElementById('app-content');
    const navMenus = document.getElementById('nav-menus');
    
    const token = localStorage.getItem('access_token');
    let route = routes[hash] ? hash : '#login';
    
    // Route Guard (Proteksi Halaman)
    if (!token && route !== '#register') {
        route = '#login';
        if (window.location.hash !== '#login') {
            window.location.hash = '#login';
            return;
        }
    } else if (token && (route === '#login' || route === '#register')) {
        window.location.hash = '#dashboard';
        return;
    }

    // Suntik HTML ke dalam DOM
    if (appContent) appContent.innerHTML = routes[route];

    // Logika Header Navbar Atas
    if (route === '#dashboard') {
        const username = localStorage.getItem('username') || 'Warga';
        if (navMenus) {
            navMenus.innerHTML = `
                <span class="navbar-text me-3 text-white">
                    <i class="bi bi-person-circle me-1"></i>${username}
                </span>
                <button onclick="logout()" class="btn btn-outline-light btn-sm fw-bold">
                    Keluar
                </button>
            `;
        }

        // Panggil fungsi pembuat data dashboard dari app.js
        if (typeof loadDashboardData === 'function') {
            loadDashboardData('my_reports', 1).then(() => {
                console.log('Dashboard data loaded successfully');
            });
        }

        // BINDING MANUAL: Tombol "+ Laporan Baru" ke Modal Bootstrap
        const btnAddReport = document.getElementById('btnAddReport');
        if (btnAddReport) {
            console.log('Binding btnAddReport event listener');
            btnAddReport.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('btnAddReport clicked!');
                
                // Cari form laporan di dalam modal, lalu bersihkan isinya
                const reportForm = document.getElementById('reportForm');
                if (reportForm) reportForm.reset();
                
                // Set global state ke null (menandakan ini data BARU, bukan EDIT)
                // FIX: Typo 'define' → 'undefined'
                if (typeof editingReportId !== 'undefined') editingReportId = null; 
                
                // Ubah judul modal menjadi Buat Laporan Baru
                const modalTitle = document.getElementById('reportModalLabel');
                if (modalTitle) {
                    modalTitle.innerHTML = `<i class="bi bi-pencil-square me-2" style="color: var(--accent-teal)"></i>Buat Laporan Baru`;
                }

                // Munculkan Modal secara terprogram
                const modalEl = document.getElementById('reportModal');
                if (modalEl) {
                    const existingInstance = bootstrap.Modal.getInstance(modalEl);
                    if (existingInstance) existingInstance.dispose();
                    
                    const modalInstance = new bootstrap.Modal(modalEl);
                    modalInstance.show();
                    console.log('Modal shown successfully');
                } else {
                    console.error('reportModal element not found!');
                }
            });
        } else {
            console.error('btnAddReport not found in DOM');
        }

        // BINDING MANUAL: Navigasi Sub-menu (Laporan Saya vs Feed Kota)
        const menuMyReports = document.getElementById('menuMyReports');
        const menuFeed = document.getElementById('menuFeed');

        if (menuMyReports && menuFeed) {
            menuMyReports.addEventListener('click', function() {
                menuMyReports.classList.add('active');
                menuFeed.classList.remove('active');
                if (typeof loadDashboardData === 'function') loadDashboardData('my_reports', 1);
            });

            menuFeed.addEventListener('click', function() {
                menuFeed.classList.add('active');
                menuMyReports.classList.remove('active');
                if (typeof loadDashboardData === 'function') loadDashboardData('feed', 1);
            });
        }

    } else {
        if (navMenus) {
            navMenus.innerHTML = `
                <a class="btn btn-outline-light btn-sm fw-bold" href="#login">
                    Masuk Portal
                </a>
            `;
        }
    }

    if (route === '#login') setupLoginForm();
    if (route === '#register') setupRegisterForm();
}

// =====================================================================
// AUTHENTICATION PROCESS DIRECT HANDLERS
// =====================================================================
function setupLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    // replace handler safely (avoid duplicate listeners)
    form.onsubmit = async (e) => {
        e.preventDefault();
        const usernameEl = document.getElementById('loginUsername');
        const passwordEl = document.getElementById('loginPassword');

        if (!usernameEl || !passwordEl) return;

        const username = usernameEl.value.trim();
        const password = passwordEl.value;

        if (typeof requestAPI !== 'function') {
            alert('Fungsi requestAPI tidak ditemukan di app.js!');
            return;
        }

        // SimpleJWT standard token obtain pair endpoint: api/token/
        const resp = await requestAPI('token', 'POST', { username, password });

        if (resp && (resp.status === 200 || resp.status === 201)) {
            // SimpleJWT returns { access, refresh }
            const access = resp.data?.access || resp.data?.access_token || resp.data?.token;
            const refresh = resp.data?.refresh || resp.data?.refresh_token || null;
            if (access) localStorage.setItem('access_token', access);
            if (refresh) localStorage.setItem('refresh_token', refresh);
            localStorage.setItem('username', username);
            window.location.hash = '#dashboard';
        } else {
            alert('Login Gagal! Periksa kembali username dan password.');
        }
    };
}

function setupRegisterForm() {
    const form = document.getElementById('registerForm');
    if (!form) return;
    // use onsubmit to prevent duplicate handlers
    form.onsubmit = async (e) => {
        e.preventDefault();
        const username = document.getElementById('registerUsername').value.trim();
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;

        if (typeof requestAPI !== 'function') return;

        // backend register endpoint: api/register/
        const resp = await requestAPI('register', 'POST', { username, email, password });

        if (resp && (resp.status === 200 || resp.status === 201)) {
            alert('Registrasi Berhasil! Silakan login.');
            window.location.hash = '#login';
        } else {
            alert('Registrasi Gagal! Username mungkin sudah digunakan.');
        }
    };
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    window.location.hash = '#login';
}

// Global Lifecycle Listeners
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);