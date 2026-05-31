const BASE_URL = 'http://127.0.0.1:8000';

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const accessToken = localStorage.getItem('access_token');
    const headers = { 'Content-Type': 'application/json' };

    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const options = { method: method, headers: headers };

    if (bodyData && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);
        const data = await response.json();
        return { status: response.status, ok: response.ok, data: data };
    } catch (error) {
        console.error('Koneksi API Gagal:', error);
        return { status: 500, ok: false, data: { detail: 'Koneksi ke server gagal.' } };
    }
}