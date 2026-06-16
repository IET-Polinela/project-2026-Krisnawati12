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
    
    const loadingEl = document.getElementById('loadingBar');
    if (loadingEl) loadingEl.style.display = 'block';

    // Menggunakan requestAPI dari api.js
    const response = await requestAPI(`/api/report/?tab=${encodeURIComponent(currentTab)}&page=${encodeURIComponent(currentPage)}`, 'GET');

    try {
        if (response && response.status === 200) {
            const data = response.data || {};
            const { results = [], count = 0 } = data;

            allReports = Array.isArray(results) ? results : [];

            const pageSize = 10;
            totalPages = Math.max(1, Math.ceil((count || 0) / pageSize));

            if (currentPage > totalPages) currentPage = totalPages;
            if (currentPage < 1) currentPage = 1;

            renderList();
            renderPagination();
            await loadSummaryStats();
        } else {
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
// 2. LOAD SUMMARY STATS
// =====================================================================
async function loadSummaryStats() {
    try {
        const url = `/api/report/?tab=my_reports&page_size=1000`;
        const response = await requestAPI(url, 'GET');

        const results = (response && response.status === 200 && response.data && Array.isArray(response.data.results))
            ? response.data.results
            : [];

        const draftCount = results.filter(r => String(r.status).toUpperCase() === 'DRAFT').length;
        const processCount = results.filter(r => {
            const s = String(r.status).toUpperCase();
            return s === 'PROCESS' || s === 'IN_PROGRESS' || s === 'PENDING' || s === 'PROSES';
        }).length;
        const resolvedCount = results.filter(r => {
            const s = String(r.status).toUpperCase();
            return s === 'RESOLVED' || s === 'DONE' || s === 'COMPLETED' || s === 'SELESAI';
        }).length;
        const reportedCount = results.filter(r => String(r.status).toUpperCase() === 'REPORTED').length;
        const verifiedCount = results.filter(r => String(r.status).toUpperCase() === 'VERIFIED').length;

        // Update semua ID statistik
        const statIds = {
            'statDraft': draftCount,
            'statReported': reportedCount,
            'statVerified': verifiedCount,
            'statInProgress': processCount,
            'statResolved': resolvedCount
        };

        Object.entries(statIds).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        });

    } catch (err) {
        console.error('loadSummaryStats error:', err);
    }
}

// =====================================================================
// 3. RENDER LIST
// =====================================================================
function renderList() {
    console.log('renderList called, allReports length=', Array.isArray(allReports) ? allReports.length : allReports);
    const listContainer = document.getElementById('listContainer');
    if (!listContainer) {
        console.error('renderList: listContainer not found');
        return;
    }

    if (!Array.isArray(allReports) || allReports.length === 0) {
        listContainer.innerHTML = `
            <div class="col-12 text-center py-5 text-muted">
                <i class="bi bi-inbox fs-1 mb-3" style="color: var(--accent-teal)"></i>
                <h5>Tidak ada laporan</h5>
                <p class="mb-0">Klik "+ Laporan Baru" untuk membuat laporan pertama Anda.</p>
            </div>
        `;
        return;
    }

    let htmlContent = '';
    allReports.forEach(report => {
        let badgeClass = 'bg-primary';
        const currentStatus = String(report.status).toUpperCase();

        if (currentStatus === 'DRAFT') badgeClass = 'bg-warning text-dark';
        else if (currentStatus === 'REPORTED') badgeClass = 'bg-info text-dark';
        else if (currentStatus === 'RESOLVED' || currentStatus === 'SELESAI') badgeClass = 'bg-success';

        htmlContent += `
            <div class="col-12 mb-3">
                <div class="card border-0 shadow-sm border-start border-4 ${currentStatus === 'DRAFT' ? 'border-warning' : 'border-primary'}" style="background-color: var(--card-bg) !important;">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge ${badgeClass}">${report.status}</span>
                            <small class="text-muted">${new Date(report.created_at).toLocaleDateString()}</small>
                        </div>
                        <h5 class="card-title fw-bold" style="color: var(--text-main) !important;">${report.title}</h5>
                        <p class="card-text text-secondary" style="color: var(--text-muted) !important;">${report.description}</p>
                        <hr style="border-color: var(--glass-border)">
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="text-muted small"><i class="bi bi-geo-alt me-1" style="color: var(--accent-teal)"></i>${report.location}</span>
                            ${report.is_owner && currentStatus === 'DRAFT' ? 
                              `<button class="btn btn-sm btn-outline-warning" onclick="editDraft(${report.id})"><i class="bi bi-pencil-square me-1"></i>Edit</button>` : ''}
                        </div>
                    </div>
                </div>
            </div>`;
    });
    listContainer.innerHTML = htmlContent;
}

// =====================================================================
// 4. EDIT DRAFT
// =====================================================================
async function editDraft(id) {
    if (!id) return;
    const response = await requestAPI(`/api/report/${id}`, 'GET');
    if (response && response.status === 200 && response.data) {
        const data = response.data;
        
        document.getElementById('reportTitle').value = data.title || '';
        document.getElementById('reportCategory').value = data.category || '';
        document.getElementById('reportDescription').value = data.description || '';
        document.getElementById('reportLocation').value = data.location || '';

        editingReportId = id;

        const modalTitle = document.getElementById('reportModalLabel');
        if (modalTitle) modalTitle.innerHTML = `<i class="bi bi-pencil-square me-2" style="color: var(--accent-teal)"></i>Edit Draft Laporan`;

        const modalEl = document.getElementById('reportModal');
        if (modalEl) {
            const modalInstance = new bootstrap.Modal(modalEl);
            modalInstance.show();
        }
    } else {
        console.error('Gagal memuat data draft untuk edit', response);
    }
}

// =====================================================================
// 5. SUBMIT HANDLER
// =====================================================================
async function handleReportSubmit(targetStatus = 'REPORTED') {
    console.log('handleReportSubmit triggered, targetStatus =', targetStatus);

    const payload = {
        title: document.getElementById('reportTitle').value.trim(),
        category: document.getElementById('reportCategory').value,
        description: document.getElementById('reportDescription').value.trim(),
        location: document.getElementById('reportLocation').value.trim(),
        status: targetStatus 
    };

    if (!payload.title || !payload.description || !payload.location) {
        alert('Harap lengkapi seluruh formulir laporan!');
        return;
    }

    let response;
    try {
        // 1. Kirim data ke server
        if (editingReportId === null) {
            response = await requestAPI('report', 'POST', payload);
        } else {
            response = await requestAPI(`report/${editingReportId}`, 'PUT', payload);
        }

        console.log('Server Response:', response);

        if (response && (response.status === 201 || response.status === 200)) {
            const returnedData = response.data;
            const returnedStatus = returnedData?.status?.toUpperCase();

            // 2. DETEKSI MASALAH STATUS DRAFT
            if (targetStatus === 'DRAFT' && returnedStatus === 'REPORTED') {
                console.warn('⚠️ Server memaksa status jadi REPORTED. Melakukan fix otomatis...');
                
                const newReportId = returnedData.id || editingReportId;
                
                if (newReportId) {
                    // 3. KIRIM UPDATE KHUSUS UNTUK MENGEMBALIKAN KE DRAFT
                    await requestAPI(`report/${newReportId}`, 'PATCH', { status: 'DRAFT' });
                    console.log('✅ Status berhasil diperbaiki menjadi DRAFT di server.');
                }
            }

            alert(editingReportId !== null ? 'Laporan berhasil diperbarui!' : (targetStatus === 'DRAFT' ? 'Draft berhasil disimpan!' : 'Laporan berhasil diajukan!'));

            // Tutup Modal & Reset Form
            const modalEl = document.getElementById('reportModal');
            if (modalEl) {
                const modalInstance = bootstrap.Modal.getInstance(modalEl);
                if (modalInstance) modalInstance.hide();
            }

            document.getElementById('reportForm')?.reset();
            editingReportId = null;

            const modalTitle = document.getElementById('reportModalLabel');
            if (modalTitle) modalTitle.innerHTML = `<i class="bi bi-pencil-square me-2" style="color: var(--accent-teal)"></i>Buat Laporan Baru`;

            // Refresh Dashboard
            await loadDashboardData(currentTab, 1);

        } else {
            console.error('Submit failed:', response);
            alert('Gagal menyimpan laporan. Sila periksa kembali isian Anda.');
        }
    } catch (err) {
        console.error('Error during submit:', err);
        alert('Terjadi kesalahan jaringan saat menyimpan laporan.');
    }
}

// =====================================================================
// 6. PAGINASI
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

// =====================================================================
// 8. INITIALIZATION
// =====================================================================
window.addEventListener('DOMContentLoaded', () => {
    // Setup event listener untuk tombol di dalam modal
    const btnDraft = document.getElementById('btnDraft');
    if (btnDraft) {
        btnDraft.onclick = (e) => { e.preventDefault(); handleReportSubmit('DRAFT'); };
    }

    const btnSubmit = document.getElementById('btnSubmit');
    if (btnSubmit) {
        btnSubmit.onclick = (e) => { e.preventDefault(); handleReportSubmit('REPORTED'); };
    }

    // Cegah default action submit bawaan browser form
    const form = document.getElementById('reportForm');
    if (form) {
        form.addEventListener('submit', (e) => e.preventDefault());
    }
});