import React, { useState, useEffect } from 'react';
import { useAuthStore } from '../stores/authStore';
import { getChannels, createChannel } from '../services/api'; // <-- DOĞRUSU BU

// StrategyPage'den kopyalanan stil tanımlamaları
const pageStyle = { padding: '20px', maxWidth: '1200px', margin: '0 auto' };
const formStyle = { marginBottom: '30px', border: '1px solid #444', padding: '20px', borderRadius: '8px', backgroundColor: '#2d2d2d' };
const inputStyle = { width: '100%', padding: '10px', marginBottom: '15px', boxSizing: 'border-box', backgroundColor: '#333', color: '#fff', border: '1px solid #555', borderRadius: '4px' };
const buttonStyle = { width: '100%', padding: '12px', cursor: 'pointer', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', fontSize: '16px' };
const tableStyle = { width: '100%', borderCollapse: 'collapse' };
const thTdStyle = { borderBottom: '1px solid #444', padding: '12px 15px', textAlign: 'left' };
const thStyle = { ...thTdStyle, backgroundColor: '#333' };

const ChannelPage = () => {
  const token = useAuthStore((state) => state.token);
  const [channels, setChannels] = useState([]);
  const [name, setName] = useState('');
  const [youtubeChannelId, setYoutubeChannelId] = useState('');
  const [error, setError] = useState('');
  
  const fetchChannels = async () => {
    if (!token) return;
    try {
      const data = await getChannels(token);
      setChannels(data);
    } catch (err) {
      setError('Kanallar yüklenemedi: ' + err.message);
    }
  };

  useEffect(() => {
    fetchChannels();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await createChannel({ name, youtube_channel_id: youtubeChannelId }, token);
      setName('');
      setYoutubeChannelId('');
      fetchChannels(); // Listeyi anında güncelle
    } catch (err) {
      setError('Kanal oluşturulamadı: ' + err.message);
    }
  };

  return (
    <div style={pageStyle}>
      <h1>Kanal Yönetimi</h1>
      
      <div style={formStyle}>
        <h2>Yeni Kanal Ekle</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Kanal Adı (örn: Teknoloji Kanalım)" value={name} onChange={(e) => setName(e.target.value)} style={inputStyle} required />
          <input type="text" placeholder="YouTube Kanal ID (örn: UC_x5XG1OV2P6hfBC5pa...) " value={youtubeChannelId} onChange={(e) => setYoutubeChannelId(e.target.value)} style={inputStyle} required />
          <button type="submit" style={buttonStyle}>Kanal Ekle</button>
          {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        </form>
      </div>

      <h2>Mevcut Kanallar</h2>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>ID</th>
            <th style={thStyle}>Kanal Adı</th>
            <th style={thStyle}>YouTube Kanal ID</th>
          </tr>
        </thead>
        <tbody>
          {channels.map(channel => (
            <tr key={channel.id}>
              <td style={thTdStyle}>{channel.id}</td>
              <td style={thTdStyle}>{channel.name}</td>
              <td style={thTdStyle}>{channel.youtube_channel_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ChannelPage;
