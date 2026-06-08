// =====================================================================
// GLOBAL STATE
// =====================================================================
let currentTab = 'my_reports'; 
let currentPage = 1;
let totalPages = 1;
let allReports = [];
let editingReportId = null;

// =====================================================================
// 1. FETCH DATA DARI API
// =====================================================================
async function loadDashboardData(tab = currentTab, page = currentPage) {
    currentTab = tab;
    currentPage = page;
    const response = await requestAPI(`/api/report/?tab=${encodeURIComponent(currentTab)}&page=${encodeURIComponent(currentPage)}`, 'GET');

    // optional: tampilkan indikator loading jika ada elemen dengan id 'loadingBar'
    const loadingEl = document.getElementById('loadingBar');
    if (loadingEl) loadingEl.style.display = 'block';

    try {
        if (response && response.status === 200) {
            // Ekstraksi data paginasi (defensive)
            const data = response.data || {};
            const { results = [], count = 0 } = data;

            // Simpan array data laporan ke global allReports
            allReports = Array.isArray(results) ? results : [];

            // Hitung totalPages berdasarkan count dan page_size = 10
            const pageSize = 10;
            totalPages = Math.max(1, Math.ceil((count || 0) / pageSize));

            // Pastikan currentPage berada pada rentang yang valid
            if (currentPage > totalPages) currentPage = totalPages;
            if (currentPage < 1) currentPage = 1;

            // Perbarui UI
            renderList();
            renderPagination();
            await loadSummaryStats();
        } else {
            // API gagal / respons bukan 200
            const listContainer = document.getElementById('listContainer');
            if (listContainer) {
                listContainer.innerHTML = `
                    <div class="col-12 text-center text-muted p-5">
                        <i class="bi bi-exclamation-triangle fs-1"></i>
                        <p>Gagal memuat data laporan.</p>
                    </div>
                `;
            }
            const paginationContainer = document.getElementById('paginationContainer');
            if (paginationContainer) paginationContainer.innerHTML = '';
            console.error('loadDashboardData error:', response);
        }
    } catch (err) {
        console.error('Network/error while loading dashboard data:', err);
        const listContainer = document.getElementById('listContainer');
        if (listContainer) {
            listContainer.innerHTML = `
                <div class="col-12 text-center text-muted p-5">
                    <i class="bi bi-exclamation-triangle fs-1"></i>
                    <p>Terjadi kesalahan saat menghubungi server.</p>
                </div>
            `;
        }
        const paginationContainer = document.getElementById('paginationContainer');
        if (paginationContainer) paginationContainer.innerHTML = '';
    } finally {
        if (loadingEl) loadingEl.style.display = 'none';
    }
}

// =====================================================================
// 2. RENDER LIST (Menampilkan Kartu Laporan)
// =====================================================================
function renderList() {
    console.log('renderList called, allReports length=', Array.isArray(allReports) ? allReports.length : allReports);
    const listContainer = document.getElementById('listContainer');
    if (!listContainer) {
        console.error('renderList: listContainer not found (check element id)');
        return;
    }

    if (!Array.isArray(allReports) || allReports.length === 0) {
        listContainer.innerHTML = `
            <div class="col-12 text-center py-5 text-muted">
                <i class="bi bi-inbox fs-1 mb-3"></i>
                <h5>Tidak ada laporan</h5>
                <p class="mb-0">Klik "Laporan Baru" untuk membuat laporan pertama Anda.</p>
            </div>
        `;
        return;
    }

    let htmlContent = '';
    allReports.forEach(report => {
        let badgeColor = report.status === 'DRAFT' ? 'bg-warning text-dark' : 'bg-primary';
        
        htmlContent += `
            <div class="col-12 mb-3">
                <div class="card border-0 shadow-sm border-start border-4 ${report.status === 'DRAFT' ? 'border-warning' : 'border-primary'}">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge ${badgeColor}">${report.status}</span>
                            <small class="text-muted">${new Date(report.created_at).toLocaleDateString()}</small>
                        </div>
                        <h5 class="card-title fw-bold">${report.title}</h5>
                        <p class="card-text text-secondary">${report.description}</p>
                        <hr>
                        <div class="d-flex justify-content-between">
                            <span class="text-muted small"><i class="bi bi-geo-alt"></i> ${report.location}</span>
                            ${report.is_owner && report.status === 'DRAFT' ? 
                              `<button class="btn btn-sm btn-outline-warning" onclick="editDraft(${report.id})">Edit</button>` : ''}
                        </div>
                    </div>
                </div>
            </div>`;
    });
    listContainer.innerHTML = htmlContent;
}

// =====================================================================
// 3. STATISTIK SIDEBAR
// =====================================================================
async function loadSummaryStats() {
    try {
        const url = `/api/report/?tab=my_reports&page_size=1000`;
        const response = await requestAPI(url, 'GET');

        const results = (response && response.status === 200 && response.data && Array.isArray(response.data.results))
            ? response.data.results
            : [];

        // Hitung rekap berdasarkan status
        const draftCount = results.filter(r => String(r.status).toUpperCase() === 'DRAFT').length;
        const processCount = results.filter(r => {
            const s = String(r.status).toUpperCase();
            return s === 'PROCESS' || s === 'IN_PROGRESS' || s === 'PENDING' || s === 'PROSES';
        }).length;
        const resolvedCount = results.filter(r => {
            const s = String(r.status).toUpperCase();
            return s === 'RESOLVED' || s === 'DONE' || s === 'COMPLETED' || s === 'SELESAI';
        }).length;

        const elDraft = document.getElementById('countDraft');
        if (elDraft) elDraft.textContent = draftCount;
        const elProcess = document.getElementById('countProcess');
        if (elProcess) elProcess.textContent = processCount;
        const elResolved = document.getElementById('countResolved');
        if (elResolved) elResolved.textContent = resolvedCount;
    } catch (err) {
        console.error('loadSummaryStats error:', err);
    }
}

// Fungsi untuk mengisi modal dengan data draft yang akan diedit
async function editDraft(id) {
    if (!id) return;
    const response = await requestAPI(`/api/report/${id}`, 'GET');
    if (response && response.status === 200 && response.data) {
        const data = response.data;
        const t = document.getElementById('reportTitle');
        if (t) t.value = data.title || '';
        const c = document.getElementById('reportCategory');
        if (c) c.value = data.category || '';
        const d = document.getElementById('reportDescription');
        if (d) d.value = data.description || '';
        const l = document.getElementById('reportLocation');
        if (l) l.value = data.location || '';

        editingReportId = id;

        const modalEl = document.getElementById('reportModal');
        if (modalEl) new bootstrap.Modal(modalEl).show();
    } else {
        console.error('Gagal memuat data draft untuk edit', response);
    }
}

// =====================================================================
// 4. SUBMIT HANDLER (Hanya SATU Fungsi Utama & Valid)
// =====================================================================
async function handleReportSubmit(targetStatus = 'REPORTED') {
    console.log('handleReportSubmit triggered, targetStatus =', targetStatus);

    const payload = {
        title: document.getElementById('reportTitle').value,
        category: document.getElementById('reportCategory').value,
        description: document.getElementById('reportDescription').value,
        location: document.getElementById('reportLocation').value,
        status: targetStatus
    };

    let response;

    if (editingReportId === null) {
        response = await requestAPI('report', 'POST', payload);
    } else {
        response = await requestAPI(`report/${editingReportId}`, 'PUT', payload);
    }

    if (response && (response.status === 201 || response.status === 200)) {
        console.log('Submit Success Response:', response);

        // Notifikasi Sukses Dinamis
        if (editingReportId !== null) {
            alert('Laporan berhasil diperbarui!');
        } else {
            alert(
                targetStatus === 'DRAFT'
                    ? 'Draft berhasil disimpan!'
                    : 'Laporan berhasil diajukan!'
            );
        }

        // Sembunyikan Modal Bootstrap secara aman
        const modalEl = document.getElementById('reportModal');
        if (modalEl) {
            const modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modalInstance.hide();
        }

        // Reset Formulir Laporan
        document.getElementById('reportForm')?.reset();

        // Kembalikan status ID edit ke null
        editingReportId = null;

        // Refresh Data Dashboard (Kembali ke halaman 1 agar data baru langsung kelihatan)
        await loadDashboardData(currentTab, 1);

    } else {
        console.error('Submit failed:', response);
        alert(
            'Gagal menyimpan:\n' +
            JSON.stringify(response?.data || response?.error || 'Unknown Error')
        );
    }
}

// =====================================================================
// 5. PAGINASI
// =====================================================================
function renderPagination() {
    const container = document.getElementById('paginationContainer');
    if (!container) return;
    
    let html = `<li class="page-item ${currentPage === 1 ? 'disabled' : ''}"><button class="page-link" onclick="loadDashboardData('${currentTab}', ${currentPage - 1})">Prev</button></li>`;
    for (let i = 1; i <= totalPages; i++) {
        html += `<li class="page-item ${i === currentPage ? 'active' : ''}"><button class="page-link" onclick="loadDashboardData('${currentTab}', ${i})">${i}</button></li>`;
    }
    html += `<li class="page-item ${currentPage === totalPages ? 'disabled' : ''}"><button class="page-link" onclick="loadDashboardData('${currentTab}', ${currentPage + 1})">Next</button></li>`;
    container.innerHTML = html;
}

// Tambahkan fungsi inisialisasi tombol laporan (dipanggil setelah dashboard dirender)
function initializeReportButtons() {
    const btnDraft = document.getElementById('btnDraft');
    if (btnDraft) {
        btnDraft.onclick = () => {
            handleReportSubmit('DRAFT');
        };
    }

    const btnSubmit = document.getElementById('btnSubmit');
    if (btnSubmit) {
        btnSubmit.onclick = () => {
            handleReportSubmit('REPORTED');
        };
    }
}

// =====================================================================
// API REQUESTS
// =====================================================================
const API_BASE = 'http://127.0.0.1:8000';
function getAccessToken(){ return localStorage.getItem('access_token'); }
async function requestAPI(path, method='GET', body=null){
  const raw = String(path||'').trim();
  const [p, qs] = raw.split('?');
  const resource = p.startsWith('/api/') ? p.replace(/^\/+/, '') : `api/${p.replace(/^\/+/, '')}`;
  const finalPath = resource.endsWith('/') ? resource : resource + '/';
  const url = `${API_BASE}/${finalPath}${qs ? '?' + qs : ''}`;
  const headers = {'Accept':'application/json'};
  if (body) headers['Content-Type']='application/json';
  const token = getAccessToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return fetch(url, { method, headers, body: body?JSON.stringify(body):null, credentials:'omit' })
    .then(r => r.json().catch(()=>null).then(data => ({ status: r.status, data })))
    .catch(err => ({ status:0, error: err }));
}

// Handler login
async function handleLogin() {
    const username = (document.getElementById('username')||{}).value || '';
    const password = (document.getElementById('password')||{}).value || '';
    if (!username || !password) { alert('Isi username & password'); return; }

    const resp = await requestAPI(LOGIN_URL, 'POST', { username, password });

    if (resp && (resp.status === 200 || resp.status === 204 || resp.status === 201)) {
        await loadDashboardData('my_reports', 1);
        if (location.hash !== '#/dashboard') location.hash = '#/dashboard';
    } else {
        console.error('Login gagal', resp);
        alert('Login gagal: periksa username/password atau lihat console network');
    }
}

// Bind tombol login
const btnLogin = document.getElementById('btnLogin');
if (btnLogin) btnLogin.addEventListener('click', handleLogin);

// Routing logic
function handleRouteChange() {
    const hash = window.location.hash || '#/dashboard';
    if (hash.startsWith('#/dashboard')) {
        // pastikan tombol inisialisasi dipanggil setelah loadDashboardData selesai
        loadDashboardData('my_reports', 1).finally(() => {
            initializeReportButtons();
        });
    }
}

window.addEventListener('hashchange', handleRouteChange);
window.addEventListener('DOMContentLoaded', handleRouteChange);

// =====================================================================
// DOM EVENT LISTENERS (Inisialisasi Event setelah DOM Siap)
// =====================================================================
window.addEventListener('DOMContentLoaded', () => {
    // Tombol ajukan / submit default
    const btn = document.getElementById('btnSubmit');
    if (btn) btn.addEventListener('click', () => handleReportSubmit('REPORTED'));

    // Pencegahan default submit jika menggunakan form element HTML
    const form = document.getElementById('reportForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            // Default behavior diarahkan ke REPORTED jika ditekan via Enter form
            handleReportSubmit('REPORTED');
        });
    }
});