// Ganti base API supaya terhubung ke server kampus
const API_BASE = 'http://103.151.63.71:8005';

function getAccessToken(){ return localStorage.getItem('access_token'); }

async function requestAPI(path, method='GET', body=null){
    // normalize path and keep querystring
    const raw = String(path || '').trim();
    const [p, qs] = raw.split('?');
    const resource = p.startsWith('/api/') ? p.replace(/^\/+/, '') : p.replace(/^\/+/, '');
    const url = `${API_BASE}/${resource}${urlEndsWithSlash(resource) ? '' : '/'}${qs ? '?'+qs : ''}`;

    const headers = { 'Accept': 'application/json' };
    if (body) headers['Content-Type'] = 'application/json';
    const token = getAccessToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const resp = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
        credentials: 'omit'
    }).catch(e => ({ fetchError: e }));

    if (!resp || resp.fetchError) return { status: 0, error: resp.fetchError };
    const data = await resp.json().catch(()=>null);
    return { status: resp.status, data };
}

function urlEndsWithSlash(s){ return s.endsWith('/'); }