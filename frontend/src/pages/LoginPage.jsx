// /home/semih/youtube-automation/frontend/src/pages/LoginPage.jsx - TAM VE DOĞRU KOD
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { loginUser } from '../services/api'; // api.js'den import ediyoruz
import './LoginPage.css';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const setToken = useAuthStore((state) => state.setToken);
    const navigate = useNavigate();

    // Fonksiyonun adını 'handleSubmit' olarak standartlaştırıyoruz
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await loginUser({ username, password });
            setToken(response.access_token);
            navigate('/dashboard');
        } catch (err) {
            // Yeni 'fetch' tabanlı hata yönetimi
            setError(err.message || 'Giriş sırasında bilinmeyen bir hata oluştu.');
            console.error(err);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2>Chimera Control</h2>
                <p>Welcome Back, Commander</p>
                {/* Formun onSubmit'i de 'handleSubmit'i çağırıyor */}
                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="login-button">Login</button>
                    {error && <p className="error-message">{error}</p>}
                </form>
            </div>
        </div>
    );
};

export default LoginPage;