import React, { useState, useEffect, useCallback } from 'react';
import { useAuthStore } from '../stores/authStore';
import { getStrategies, createStrategy, getChannels } from '../services/api';

// Stil Tanımlamaları
const pageStyle = { padding: '20px', maxWidth: '1200px', margin: '0 auto', color: '#e0e0e0' };
const formStyle = { marginBottom: '30px', border: '1px solid #444', padding: '20px', borderRadius: '8px', backgroundColor: '#2d2d2d' };
const inputStyle = { width: '100%', padding: '10px', marginBottom: '15px', boxSizing: 'border-box', backgroundColor: '#333', color: '#fff', border: '1px solid #555', borderRadius: '4px' };
const buttonStyle = { width: '100%', padding: '12px', cursor: 'pointer', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', fontSize: '16px' };
const tableStyle = { width: '100%', borderCollapse: 'collapse', marginTop: '20px' };
const thTdStyle = { borderBottom: '1px solid #444', padding: '12px 15px', textAlign: 'left' };
const thStyle = { ...thTdStyle, backgroundColor: '#333' };
const labelStyle = { display: 'block', marginBottom: '5px', fontWeight: 'bold' };

// Popüler YouTube Kategorileri
const YOUTUBE_CATEGORIES = [
    "Film & Animasyon", "Otomobil & Araçlar", "Müzik", "Evcil Hayvanlar & Hayvanlar",
    "Spor", "Seyahat & Etkinlikler", "Oyun", "İnsanlar & Bloglar", "Komedi",
    "Eğlence", "Haber & Politika", "Nasıl Yapılır & Stil", "Eğitim",
    "Bilim & Teknoloji", "Kâr Amacı Gütmeyen Kuruluşlar & Aktivizm"
];

const StrategyPage = () => {
    const token = useAuthStore((state) => state.token);
    const [strategies, setStrategies] = useState([]);
    const [channels, setChannels] = useState([]);
    
    // Form State'leri
    const [selectedChannel, setSelectedChannel] = useState('');
    const [selectedCategory, setSelectedCategory] = useState(YOUTUBE_CATEGORIES[0]);
    const [manualTitle, setManualTitle] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(true);

    const fetchData = useCallback(async () => {
        if (!token) return;
        setLoading(true);
        setError('');
        try {
            const [strategiesRes, channelsRes] = await Promise.all([
                getStrategies(token),
                getChannels(token)
            ]);
            setStrategies(strategiesRes);
            setChannels(channelsRes);

            if (channelsRes.length > 0 && !selectedChannel) {
                setSelectedChannel(channelsRes[0].id);
            }
        } catch (err) {
            setError('Veriler yüklenemedi: ' + err.message);
            console.error("Fetch Data Error:", err);
        } finally {
            setLoading(false);
        }
    }, [token, selectedChannel]); // selectedChannel'ı bağımlılıktan çıkardık, ilk yüklemede ayarlanacak

    useEffect(() => {
        fetchData();
    }, [token]); // Sadece token değiştiğinde veya ilk yüklendiğinde çalışsın

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedChannel) {
            setError("Lütfen bir kanal seçin.");
            return;
        }
        setError('');
        
        const strategyData = {
            title: manualTitle || `${selectedCategory} - Otomatik Video`,
            description: "Bu video Chimera tarafından otomatik üretildi.",
            video_path: `/videos/${selectedCategory.toLowerCase().replace(/ & /g, '_').replace(/ /g, '_')}.mp4`,
            category: selectedCategory,
            channel_id: parseInt(selectedChannel)
        };

        try {
            await createStrategy(strategyData, token);
            setManualTitle('');
            await fetchData(); // Listeyi yeniden çek
        } catch (err) {
            setError('Strateji oluşturulamadı: ' + (err.response?.data?.message || err.message));
        }
    };

    if (loading) {
        return <div style={pageStyle}><h1>Veriler Yükleniyor...</h1></div>;
    }

    return (
        <div style={pageStyle}>
            <h1>Video Yükleme Stratejileri</h1>
            
            <div style={formStyle}>
                <h2>Yeni Strateji Oluştur</h2>
                <form onSubmit={handleSubmit}>
                    <label style={labelStyle}>1. Kanal Seçin:</label>
                    <select value={selectedChannel} onChange={(e) => setSelectedChannel(e.target.value)} style={inputStyle} required>
                        <option value="" disabled>-- Kanal Seçiniz --</option>
                        {channels.map(ch => <option key={ch.id} value={ch.id}>{ch.name}</option>)}
                    </select>

                    <label style={labelStyle}>2. Kategori Seçin (Trend Analizi İçin):</label>
                    <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)} style={inputStyle}>
                        {YOUTUBE_CATEGORIES.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                    </select>

                    <label style={labelStyle}>3. Video Başlığı (Opsiyonel):</label>
                    <input type="text" placeholder="Boş bırakırsanız otomatik oluşturulur..." value={manualTitle} onChange={(e) => setManualTitle(e.target.value)} style={inputStyle} />

                    <button type="submit" style={buttonStyle}>Stratejiyi Başlat</button>
                    {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
                </form>
            </div>

            <h2>Mevcut Stratejiler</h2>
            <table style={tableStyle}>
                <thead>
                    <tr>
                        <th style={thStyle}>Başlık</th>
                        <th style={thStyle}>Kategori</th>
                        <th style={thStyle}>Kanal</th>
                        <th style={thStyle}>Durum</th>
                        <th style={thStyle}>Oluşturulma Tarihi</th>
                    </tr>
                </thead>
                <tbody>
                    {strategies.length > 0 ? strategies.map(s => (
                        <tr key={s.id}>
                            <td style={thTdStyle}>{s.title}</td>
                            <td style={thTdStyle}>{s.category}</td>
                            <td style={thTdStyle}>{s.channel ? s.channel.name : 'Bilinmiyor'}</td>
                            <td style={thTdStyle}>{s.status}</td>
                            <td style={thTdStyle}>{new Date(s.created_at).toLocaleString('en-CA', { timeZone: 'America/Toronto' })}</td>
                        </tr>
                    )) : (
                        <tr>
                            <td colSpan="5" style={{...thTdStyle, textAlign: 'center'}}>Henüz strateji oluşturulmadı.</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default StrategyPage;