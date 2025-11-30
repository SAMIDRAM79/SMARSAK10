import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import DownloadPage from './pages/Download';
import LoginPage from './pages/Login';
import ProductsPage from './pages/Products';
import OrderPage from './pages/Order';
import SupportPage from './pages/Support';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<DownloadPage />} />
            <Route path="/connexion" element={<LoginPage />} />
            <Route path="/produits" element={<ProductsPage />} />
            <Route path="/commander" element={<OrderPage />} />
            <Route path="/support-tech" element={<SupportPage />} />
          </Routes>
        </BrowserRouter>
      </div>
    </AuthProvider>
  );
}

export default App;