// /home/semih/youtube-automation/frontend/src/services/api.js - NİHAİ VE ONARILMIŞ KOD
const BASE_URL = 'https://api.benimotomasyonum.com';

// --- Ortak Yanıt İşleyici ---
const handleResponse = async (response) => {
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: `Sunucu hatası: ${response.status}` }));
        throw new Error(errorData.message || `Bilinmeyen HTTP hatası: ${response.status}`);
    }
    // Başarılı cevaplarda, eğer cevap boş değilse JSON'a çevir
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
        return response.json();
    }
    return {}; // Cevap boşsa, boş bir obje döndür
};

// --- Merkezi API İstek Fonksiyonu (ONARILDI) ---
const apiRequest = async (endpoint, token, options = {}) => {
    // Başlıkları varsayılan olarak ayarlıyoruz
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    // Eğer bir token varsa, onu Authorization başlığına ekliyoruz
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // Nihai konfigürasyonu oluşturuyoruz
    const config = {
        ...options,
        headers,
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    return handleResponse(response);
};

// --- Auth (Değişiklik yok) ---
export const loginUser = (credentials) => apiRequest('/auth/login', null, { method: 'POST', body: JSON.stringify(credentials) });
export const registerUser = (userData) => apiRequest('/auth/register', null, { method: 'POST', body: JSON.stringify(userData) });

// --- Health (Artık apiRequest kullanıyor) ---
export const getSystemHealth = (token) => apiRequest('/health/status', token, { method: 'GET' });

// --- Strategies (Artık apiRequest kullanıyor) ---
export const getStrategies = (token) => apiRequest('/strategies/', token, { method: 'GET' });
export const createStrategy = (data, token) => apiRequest('/strategies/', token, { method: 'POST', body: JSON.stringify(data) });

// --- Channels (Artık apiRequest kullanıyor) ---
export const getChannels = (token) => apiRequest('/channels/', token, { method: 'GET' });
export const createChannel = (data, token) => apiRequest('/channels/', token, { method: 'POST', body: JSON.stringify(data) });