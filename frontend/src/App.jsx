import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import StrategyPage from './pages/StrategyPage';
import ChannelPage from './pages/ChannelPage';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './components/MainLayout'; // <-- Yeni Layout'u import et

function App() {
  return (
    <Routes>
      {/* Public Route - Layout yok */}
      <Route path="/" element={<LoginPage />} />

      {/* Protected Routes - MainLayout içinde */}
      <Route 
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/strategies" element={<StrategyPage />} />
        <Route path="/channels" element={<ChannelPage />} />
        {/* Buraya gelecekteki Ayarlar vb. sayfaları da ekleyebiliriz */}
        <Route path="/settings" element={<div>Ayarlar Sayfası</div>} />
      </Route>
    </Routes>
  );
}

export default App;