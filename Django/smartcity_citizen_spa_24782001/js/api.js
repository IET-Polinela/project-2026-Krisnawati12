// Ganti base API supaya frontend memanggil server kampus
const API_BASE = 'http://103.151.63.71:8005';

function getAccessToken(){ return localStorage.getItem('access_token'); }

async function requestAPI(path, method='GET', body=null){
    if (typeof API_BASE === 'undefined') {
        console.error('API_BASE is not defined! Ensure api.js is loaded before other scripts.');
        return { status: 0, error: 'Configuration Error' };
    }

    const raw = String(path || '').trim();
    const [p = '', qs] = raw.split('?');

    // Normalisasi resource agar selalu berbentuk 'api/...'
    let resource;
    if (p.startsWith('/api/')) {
        resource = p.substring(1); // remove leading slash -> 'api/...'
    } else if (p.startsWith('api/')) {
        resource = p;
    } else {
        resource = `api/${p.replace(/^\/+/, '')}`;
    }

    // Pastikan tidak ada double-slash dan selalu ada trailing '/'
    resource = resource.replace(/\/+$/,'') + '/';
    const base = String(API_BASE).replace(/\/+$/,'');
    const url = `${base}/${resource}${qs ? '?' + qs : ''}`;

    const headers = { 'Accept': 'application/json' };
    if (body) headers['Content-Type'] = 'application/json';
    const token = (typeof getAccessToken === 'function') ? getAccessToken() : null;
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const resp = await fetch(url, {
            method,
            headers,
            body: body ? JSON.stringify(body) : null,
            credentials: 'omit'
        });
        const data = await resp.json().catch(()=>null);
        return { status: resp.status, data };
    } catch (err) {
        return { status: 0, error: err };
    }
}

function urlEndsWithSlash(s){ return s.endsWith('/'); }