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

                    <button type="submit" class="btn btn-primary w-100 fw-bold">
                        Masuk
                    </button>
                </form>
            </div>
        </div>
    `,

    '#dashboard': `
        <div class="row g-4">

            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm">

                    <button
                        class="btn btn-primary btn-lg w-100 fw-bold mb-3"
                        data-bs-toggle="modal"
                        data-bs-target="#reportModal">

                        <i class="bi bi-plus-circle-fill me-2"></i>
                        Laporan Baru
                    </button>

                    <div class="list-group list-group-flush">

                        <button
                            class="list-group-item list-group-item-action"
                            onclick="loadDashboardData('my_reports', 1)">

                            <i class="bi bi-list-task me-2"></i>
                            Laporan Saya
                        </button>

                        <button
                            class="list-group-item list-group-item-action"
                            onclick="loadDashboardData('feed', 1)">

                            <i class="bi bi-globe me-2"></i>
                            Feed Kota
                        </button>

                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">

                <div
                    class="card border-0 p-4 shadow-sm text-center mb-4"
                    style="border:2px dashed #0d6efd; background-color:#f8f9ff;">

                    <i class="bi bi-shield-check text-primary fs-1"></i>

                    <h5 class="fw-bold mt-2">
                        Autentikasi Berhasil Terhubung!
                    </h5>

                    <p class="text-muted small">
                        Seluruh fitur pelaporan kini siap digunakan.
                    </p>

                </div>

                <div id="listContainer" class="row"></div>

                <nav>
                    <ul
                        id="paginationContainer"
                        class="pagination justify-content-center mt-4">
                    </ul>
                </nav>

            </section>

            <aside class="col-lg-3 d-none d-lg-block">

                <div class="card border-0 p-3 shadow-sm">

                    <h6 class="fw-bold">
                        <i class="bi bi-pie-chart-fill text-primary me-2"></i>
                        Statistik
                    </h6>

                    <hr>

                    <div class="d-flex justify-content-between mb-2">
                        <span>Draft:</span>
                        <span id="countDraft" class="fw-bold text-warning">0</span>
                    </div>

                    <div class="d-flex justify-content-between mb-2">
                        <span>Diproses:</span>
                        <span id="countProcess" class="fw-bold text-primary">0</span>
                    </div>

                    <div class="d-flex justify-content-between">
                        <span>Selesai:</span>
                        <span id="countResolved" class="fw-bold text-success">0</span>
                    </div>

                </div>

            </aside>

        </div>
    `
};

function handleRouting() {

    const hash = window.location.hash || '#login';

    const appContent = document.getElementById('app-content');

    appContent.innerHTML = routes[hash] || routes['#login'];

    const navMenus = document.getElementById('nav-menus');

    if (hash === '#dashboard') {

        const username =
            localStorage.getItem('username') || 'Warga';

        navMenus.innerHTML = `
            <span class="navbar-text me-3 text-white-50">
                <i class="bi bi-person-circle me-1"></i>
                ${username}
            </span>

            <button
                onclick="logout()"
                class="btn btn-outline-light btn-sm fw-bold">

                Keluar
            </button>
        `;

        if (typeof loadDashboardData === 'function') {
            loadDashboardData('my_reports', 1);
        }

    } else {

        navMenus.innerHTML = `
            <a
                class="btn btn-outline-light btn-sm fw-bold"
                href="#login">

                Masuk Portal
            </a>
        `;
    }

    if (
        hash === '#login' &&
        typeof setupLoginForm === 'function'
    ) {
        setupLoginForm();
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);

function logout() {

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');

    window.location.hash = '#login';

    location.reload();
}