import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import { productAPI } from '../services/api';

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await productAPI.getProducts();
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Nos Produits</h1>
          <p className="text-xl text-gray-600">
            Des solutions logicielles innovantes pour votre gestion
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600">Chargement des produits...</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-3 gap-8">
            {products.map((product) => (
              <div
                key={product.id}
                className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-shadow duration-300"
              >
                <img
                  src={product.image}
                  alt={product.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-6">
                  <h3 className="text-2xl font-bold text-gray-800 mb-3">{product.name}</h3>
                  <p className="text-gray-600 mb-4">{product.description}</p>
                  <div className="space-y-2 mb-6">
                    <p className="font-semibold text-gray-700">Fonctionnalités :</p>
                    <ul className="space-y-1">
                      {product.features.map((feature, idx) => (
                        <li key={idx} className="text-gray-600 flex items-center space-x-2">
                          <span className="text-[#4CAF50]">✓</span>
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  {product.price && (
                    <p className="text-xl font-bold text-[#1B89C7] mb-4">
                      {product.price.toLocaleString()} FCFA
                    </p>
                  )}
                  <button className="w-full bg-[#1B89C7] text-white py-2 px-4 rounded-lg hover:bg-[#1565A0] transition-colors">
                    En savoir plus
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm">© 2025 SmartScool. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
};

export default ProductsPage;