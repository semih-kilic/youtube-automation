import React from 'react';
import { Link, useNavigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import './MainLayout.css'; // Birazdan bu stil dosyasını oluşturacağız

const MainLayout = () => {
    const navigate = useNavigate();
    const logout = useAuthStore((state) => state.logout);

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    const linkStyle = {
        textDecoration: 'none',
        color: 'inherit',
        display: 'block',
        padding: '10px 15px',
    };

    return (
        <div className="layout-container">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h2>Chimera</h2>
                </div>
                <ul className="sidebar-menu">
                    <li><Link to="/dashboard" style={linkStyle}>Dashboard</Link></li>
                    <li><Link to="/strategies" style={linkStyle}>Stratejiler</Link></li>
                    <li><Link to="/channels" style={linkStyle}>Kanallar</Link></li>
                    <li><Link to="/settings" style={linkStyle}>Ayarlar</Link></li>
                </ul>
                <div className="sidebar-footer">
                    <button onClick={handleLogout} className="logout-button">Çıkış Yap</button>
                </div>
            </aside>
            <main className="main-content">
                {/* Diğer sayfalarımız (Dashboard, Stratejiler vb.) burada render edilecek */}
                <Outlet /> 
            </main>
        </div>
    );
};

export default MainLayout;
