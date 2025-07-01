import React, { useState, useEffect } from 'react';
import { useAuthStore } from '../stores/authStore';
import { getSystemHealth, createStrategy } from '../services/api';

const ServiceStatusPanel = ({ services, loading, error }) => {
  if (loading) return <p>Sistem durumu yükleniyor...</p>;
  if (error) return <p style={{ color: 'red' }}>Durum bilgisi alınamadı: {error}</p>;
  if (!services) return null;

  return (
    <div className="service-status-panel">
      <h3>Sistem Durumu</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {Object.values(services).map(service => (
          <li key={service.name} style={{ marginBottom: '10px' }}>
            {service.name}: 
            <strong style={{ color: service.status === 'Online' ? 'green' : 'red', marginLeft: '10px' }}>
              {service.status}
            </strong>
          </li>
        ))}
      </ul>
    </div>
  );
};

const QuickActionPanel = ({ token }) => {
  const [creating, setCreating] = useState(false);

  const createQuickStrategy = async () => {
    setCreating(true);
    try {
      const quickStrategy = {
        title: `Hızlı Video ${new Date().toLocaleTimeString()}`,
        description: 'Otomatik oluşturulan demo video',
        video_path: '/demo/quick_video.mp4',
        category: 'Bilim & Teknoloji',
        channel_id: 1
      };
      
      await createStrategy(quickStrategy, token);
      alert('Hızlı video başlatıldı! Strateji sayfasından takip edebilirsiniz.');
    } catch (error) {
      alert('Hata: ' + error.message);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="quick-action-panel" style={{ marginTop: '20px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Hızlı İşlemler</h3>
      <button 
        onClick={createQuickStrategy}
        disabled={creating}
        style={{
          padding: '10px 20px',
          backgroundColor: creating ? '#ccc' : '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: creating ? 'not-allowed' : 'pointer',
          fontSize: '16px'
        }}
      >
        {creating ? 'Oluşturuluyor...' : '⚡ Hızlı Video Başlat'}
      </button>
      <p style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
        Bu buton demo bir video oluşturup yükleme işlemini başlatır. Para kazanmaya hemen başlayın!
      </p>
    </div>
  );
};

const DashboardPage = () => {
    const token = useAuthStore((state) => state.token);
    const [services, setServices] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchHealth = async () => {
            try {
                const response = await getSystemHealth(token);
                setServices(response.data);
            } catch (err) {
                setError(err.message || 'API hatası.');
            } finally {
                setLoading(false);
            }
        };
        if (token) fetchHealth();
    }, [token]);

    return (
        <div>
            <h1>💰 Para Kazanma Komuta Merkezi</h1>
            <p>Hoşgeldin, Komutan. YouTube otomasyonunuz aktif ve para kazanmaya hazır!</p>
            <ServiceStatusPanel services={services} loading={loading} error={error} />
            <QuickActionPanel token={token} />
        </div>
    );
};

export default DashboardPage;