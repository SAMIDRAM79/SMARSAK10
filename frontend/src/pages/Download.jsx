import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Download } from 'lucide-react';
import Header from '../components/Header';
import { downloadAPI } from '../services/api';

const DownloadPage = () => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [downloads, setDownloads] = useState([]);
  const [loading, setLoading] = useState(true);

  const screenshots = [
    'https://images.unsplash.com/photo-1759752394755-1241472b589d',
    'https://images.unsplash.com/photo-1575388902449-6bca946ad549',
    'https://images.unsplash.com/photo-1631006732121-a6da2f4864d3',
    'https://images.unsplash.com/photo-1641567535859-c58187ac4954',
    'https://images.unsplash.com/photo-1551288049-bebda4e38f71',
    'https://images.unsplash.com/photo-1631093441315-a06b9bcbe63f',
    'https://images.pexels.com/photos/227731/pexels-photo-227731.jpeg',
  ];

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % screenshots.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + screenshots.length) % screenshots.length);
  };

  const handleDownload = (type) => {
    // Cette fonction sera connectée au backend plus tard
    alert(`Téléchargement de ${type} sera disponible prochainement!`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-12">
        {/* Title */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Télécharger <span className="text-[#1B89C7]">Smart</span><span className="text-[#E91E63]">IEPP</span>
          </h1>
          <div className="flex justify-center space-x-2 mt-4">
            <div className="w-2 h-2 rounded-full bg-[#1B89C7]"></div>
            <div className="w-2 h-2 rounded-full bg-[#4CAF50]"></div>
            <div className="w-2 h-2 rounded-full bg-[#E91E63]"></div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid md:grid-cols-2 gap-8 items-center mb-16">
          {/* Software Image */}
          <div className="flex justify-center">
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop"
                alt="SmartIEPP Software"
                className="rounded-lg shadow-2xl w-full max-w-md transform hover:scale-105 transition-transform duration-300"
              />
            </div>
          </div>

          {/* Download Info Card */}
          <div className="bg-gradient-to-br from-[#1B89C7] to-[#1565A0] rounded-xl shadow-2xl p-8 text-white">
            <h2 className="text-2xl font-bold mb-6">Infos dernière version</h2>
            
            <div className="space-y-4 mb-8">
              <div className="flex items-center space-x-3">
                <span className="text-3xl">⚙️</span>
                <div>
                  <p className="text-sm opacity-90">Version</p>
                  <p className="text-xl font-semibold">v.25.11.25</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <span className="text-3xl">📅</span>
                <div>
                  <p className="text-sm opacity-90">Date de sortie</p>
                  <p className="text-xl font-semibold">25/11/2025</p>
                </div>
              </div>
            </div>

            {/* Download Buttons */}
            <div className="space-y-3">
              <button
                onClick={() => handleDownload('Kit complet')}
                className="w-full bg-white text-[#1B89C7] py-3 px-6 rounded-lg font-semibold hover:bg-gray-100 transition-colors flex items-center justify-center space-x-2 shadow-md"
              >
                <Download className="w-5 h-5" />
                <span>Kit complet (435 Mo)</span>
              </button>

              <button
                onClick={() => handleDownload('Mise à jour')}
                className="w-full bg-white text-[#FF9800] py-3 px-6 rounded-lg font-semibold hover:bg-gray-100 transition-colors flex items-center justify-center space-x-2 shadow-md"
              >
                <Download className="w-5 h-5" />
                <span>Mise à jour (436 Mo)</span>
              </button>

              <button
                onClick={() => handleDownload('Ancienne version')}
                className="w-full bg-white bg-opacity-20 text-white py-3 px-6 rounded-lg font-semibold hover:bg-opacity-30 transition-colors flex items-center justify-center space-x-2 border border-white"
              >
                <Download className="w-5 h-5" />
                <span>Ancienne version</span>
              </button>
            </div>
          </div>
        </div>

        {/* Screenshots Section */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">
            Quelques captures d'écran
          </h2>

          {/* Carousel */}
          <div className="relative">
            <div className="overflow-hidden rounded-lg">
              <img
                src={`${screenshots[currentImageIndex]}?w=1200&h=600&fit=crop`}
                alt={`Screenshot ${currentImageIndex + 1}`}
                className="w-full h-96 object-cover"
              />
            </div>

            {/* Navigation Buttons */}
            <button
              onClick={prevImage}
              className="absolute left-4 top-1/2 -translate-y-1/2 bg-white bg-opacity-90 hover:bg-opacity-100 rounded-full p-3 shadow-lg transition-all"
            >
              <ChevronLeft className="w-6 h-6 text-gray-800" />
            </button>
            
            <button
              onClick={nextImage}
              className="absolute right-4 top-1/2 -translate-y-1/2 bg-white bg-opacity-90 hover:bg-opacity-100 rounded-full p-3 shadow-lg transition-all"
            >
              <ChevronRight className="w-6 h-6 text-gray-800" />
            </button>

            {/* Indicators */}
            <div className="flex justify-center space-x-2 mt-6">
              {screenshots.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentImageIndex(index)}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentImageIndex
                      ? 'bg-[#1B89C7] w-8'
                      : 'bg-gray-300 hover:bg-gray-400'
                  }`}
                />
              ))}
            </div>
          </div>

          {/* Thumbnail Grid */}
          <div className="grid grid-cols-4 md:grid-cols-7 gap-4 mt-8">
            {screenshots.map((screenshot, index) => (
              <button
                key={index}
                onClick={() => setCurrentImageIndex(index)}
                className={`rounded-lg overflow-hidden transition-all ${
                  index === currentImageIndex
                    ? 'ring-4 ring-[#1B89C7] scale-105'
                    : 'opacity-60 hover:opacity-100'
                }`}
              >
                <img
                  src={`${screenshot}?w=200&h=150&fit=crop`}
                  alt={`Thumbnail ${index + 1}`}
                  className="w-full h-20 object-cover"
                />
              </button>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm">
            © 2025 SmartScool. Tous droits réservés.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default DownloadPage;