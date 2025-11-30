import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ChevronDown, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const [openDropdown, setOpenDropdown] = useState(null);
  const navigate = useNavigate();
  const { user, logout, isAuthenticated } = useAuth();

  const toggleDropdown = (menu) => {
    setOpenDropdown(openDropdown === menu ? null : menu);
  };

  return (
    <>
      {/* Top Bar */}
      <div className="bg-[#1B89C7] text-white py-2 px-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center text-sm">
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <span>Bienvenue, {user?.name}</span>
                <button 
                  onClick={() => {
                    logout();
                    navigate('/');
                  }}
                  className="flex items-center space-x-1 hover:opacity-80 transition-opacity"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Déconnexion</span>
                </button>
              </div>
            ) : (
              <button 
                onClick={() => navigate('/connexion')}
                className="flex items-center space-x-1 hover:opacity-80 transition-opacity"
              >
                <span>Connexion</span>
                <span className="text-xs">👤</span>
              </button>
            )}
          </div>
          <div className="flex items-center space-x-6">
            <a href="#" className="hover:opacity-80 transition-opacity">📘</a>
            <a href="#" className="hover:opacity-80 transition-opacity">🔴</a>
            <a href="#" className="hover:opacity-80 transition-opacity">💼</a>
            <a href="#" className="hover:opacity-80 transition-opacity">📷</a>
            <a href="mailto:infos@mysmartschool.com" className="hover:opacity-80 transition-opacity flex items-center space-x-1">
              <span>✉️</span>
              <span>: infos@mysmartschool.com</span>
            </a>
            <a href="tel:+22507097591551" className="hover:opacity-80 transition-opacity flex items-center space-x-1">
              <span>📞</span>
              <span>+225 07-097-591-51</span>
            </a>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            {/* Logo */}
            <Link to="/" className="flex items-center">
              <div className="text-2xl font-bold">
                <span className="text-[#1B89C7]">SMART</span>
                <span className="text-[#4CAF50]">scool</span>
              </div>
            </Link>

            {/* Navigation Menu */}
            <nav className="flex items-center space-x-8">
              <div className="relative">
                <button
                  onClick={() => toggleDropdown('produits')}
                  className="flex items-center space-x-1 text-gray-700 hover:text-[#1B89C7] transition-colors py-2"
                >
                  <span>🎯 Produits</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                {openDropdown === 'produits' && (
                  <div className="absolute top-full left-0 mt-2 w-48 bg-white shadow-lg rounded-md py-2">
                    <Link to="/produits" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                      Tous les produits
                    </Link>
                  </div>
                )}
              </div>

              <div className="relative">
                <button
                  onClick={() => toggleDropdown('commander')}
                  className="flex items-center space-x-1 text-gray-700 hover:text-[#1B89C7] transition-colors py-2"
                >
                  <span>🛒 Commander</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                {openDropdown === 'commander' && (
                  <div className="absolute top-full left-0 mt-2 w-48 bg-white shadow-lg rounded-md py-2">
                    <Link to="/commander" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                      Passer commande
                    </Link>
                  </div>
                )}
              </div>

              <div className="relative">
                <button
                  onClick={() => toggleDropdown('telecharger')}
                  className="flex items-center space-x-1 text-gray-700 hover:text-[#1B89C7] transition-colors py-2"
                >
                  <span>💾 Télécharger</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                {openDropdown === 'telecharger' && (
                  <div className="absolute top-full left-0 mt-2 w-48 bg-white shadow-lg rounded-md py-2">
                    <Link to="/" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                      SmartIEPP
                    </Link>
                  </div>
                )}
              </div>

              <div className="relative">
                <button
                  onClick={() => toggleDropdown('support')}
                  className="flex items-center space-x-1 text-gray-700 hover:text-[#1B89C7] transition-colors py-2"
                >
                  <span>🔧 Support-Tech</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                {openDropdown === 'support' && (
                  <div className="absolute top-full left-0 mt-2 w-48 bg-white shadow-lg rounded-md py-2">
                    <Link to="/support-tech" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                      Support technique
                    </Link>
                  </div>
                )}
              </div>
            </nav>
          </div>
        </div>
      </header>
    </>
  );
};

export default Header;