import React, { useState, useEffect } from 'react';
import { Users, BookOpen, TrendingUp, DollarSign } from 'lucide-react';
import { statsAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await statsAPI.getDashboard();
      setStats(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Chargement...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Tableau de bord</h1>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Élèves</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">
                {stats?.effectifs?.total || 0}
              </p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <Users className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          <div className="mt-4 flex space-x-4 text-sm">
            <span className="text-blue-600">G: {stats?.effectifs?.garcons || 0}</span>
            <span className="text-pink-600">F: {stats?.effectifs?.filles || 0}</span>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Classes</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">
                {stats?.classes?.total || 0}
              </p>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <BookOpen className="w-8 h-8 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Enseignants</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">
                {stats?.personnel?.enseignants || 0}
              </p>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <TrendingUp className="w-8 h-8 text-purple-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-orange-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Taux paiement</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">
                {stats?.finances?.taux_paiement?.toFixed(1) || 0}%
              </p>
            </div>
            <div className="bg-orange-100 p-3 rounded-full">
              <DollarSign className="w-8 h-8 text-orange-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Effectifs par niveau */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="font-bold text-lg text-gray-800 mb-4">Pré-primaire</h3>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Effectif</span>
            <span className="text-2xl font-bold text-blue-600">
              {stats?.effectifs?.pre_primaire || 0}
            </span>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="font-bold text-lg text-gray-800 mb-4">Maternelle</h3>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Effectif</span>
            <span className="text-2xl font-bold text-green-600">
              {stats?.effectifs?.maternelle || 0}
            </span>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="font-bold text-lg text-gray-800 mb-4">Primaire</h3>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Effectif</span>
            <span className="text-2xl font-bold text-purple-600">
              {stats?.effectifs?.primaire || 0}
            </span>
          </div>
        </div>
      </div>

      {/* Détail des classes */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="font-bold text-xl text-gray-800 mb-6">Détail par classe</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Classe</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Niveau</th>
                <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">Effectif</th>
                <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">Garçons</th>
                <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">Filles</th>
              </tr>
            </thead>
            <tbody>
              {stats?.classes?.details?.map((classe, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-800">{classe.classe}</td>
                  <td className="px-4 py-3 text-gray-600 capitalize">{classe.niveau.replace('_', ' ')}</td>
                  <td className="px-4 py-3 text-center font-semibold text-blue-600">{classe.effectif}</td>
                  <td className="px-4 py-3 text-center text-gray-600">{classe.garcons}</td>
                  <td className="px-4 py-3 text-center text-gray-600">{classe.filles}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
