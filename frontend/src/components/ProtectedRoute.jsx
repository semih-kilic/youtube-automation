import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

const ProtectedRoute = ({ children }) => {
  const token = useAuthStore((state) => state.token);

  if (!token) {
    // Kullanıcı giriş yapmamışsa, login sayfasına yönlendir
    return <Navigate to="/" />;
  }

  return children; // Giriş yapmışsa, istenen sayfayı göster
};

export default ProtectedRoute;
