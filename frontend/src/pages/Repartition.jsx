import React, { useState, useEffect } from 'react';
import { Download, RefreshCw, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API_URL = BACKEND_URL ? `${BACKEND_URL}/api` : '/api';
const USER_EMAIL = 'konatdra@gmail.com';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-User-Email': USER_EMAIL,
  },
});

const Repartition = () => {
  const [centres, setCentres] = useState([]);
  const [repartition, setRepartition] = useState([]);
  const [loading, setLoading] = useState(false);
  const [nouveauCentre, setNouveauCentre] = useState('');
  const [showAddCentre, setShowAddCentre] = useState(false);

  useEffect(() => {
    fetchCentres();
    fetchRepartition();
  }, []);

  const fetchCentres = async () => {
    try {
      const response = await api.get('/repartition/centres');
      setCentres(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const fetchRepartition = async () => {
    try {
      const response = await api.get('/repartition/repartition');
      setRepartition(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const ajouterCentre = async () => {
    if (!nouveauCentre.trim()) {
      alert('Veuillez entrer un nom de centre');
      return;
    }
    
    try {
      await api.post(`/repartition/centres?nom=${encodeURIComponent(nouveauCentre)}&capacite_max=480`);
      setNouveauCentre('');
      setShowAddCentre(false);
      fetchCentres();
      alert('Centre ajouté avec succès!');
    } catch (error) {
      alert('Erreur lors de l\'ajout du centre');
    }
  };

  const calculerRepartition = async () => {
    setLoading(true);
    try {
      const response = await api.post('/repartition/calculer');
      alert(response.data.message + '\n' + 
        `Total écoles: ${response.data.total_ecoles}\n` +
        `Total candidats: ${response.data.total_candidats}\n` +
        `Centres utilisés: ${response.data.centres_utilises}`);
      fetchRepartition();
    } catch (error) {
      alert('Erreur: ' + (error.response?.data?.detail || 'Erreur lors du calcul'));
    } finally {
      setLoading(false);
    }
  };

  const verifierDoublons = async () => {
    setLoading(true);
    try {
      const response = await api.post('/repartition/verifier-doublons');
      alert(`Vérification terminée:\n` +
        `Doublons trouvés: ${response.data.doublons_trouves}\n` +
        `Doublons supprimés: ${response.data.doublons_supprimes}`);
    } catch (error) {
      alert('Erreur lors de la vérification');
    } finally {
      setLoading(false);
    }
  };

  const exporterCSV = async () => {
    try {
      const response = await api.get('/repartition/export');
      const blob = new Blob([response.data.csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = response.data.filename;
      a.click();
    } catch (error) {
      alert('Erreur: ' + (error.response?.data?.detail || 'Erreur lors de l\'export'));
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Répartition des Centres de Composition</h1>

      {/* Règles */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-8">
        <h2 className="text-xl font-bold text-blue-900 mb-4">📋 Règles de répartition</h2>
        <ul className="space-y-2 text-blue-800">
          <li>✓ <strong>28 candidats par salle</strong> (ratio unique)</li>
          <li>✓ Dernière salle : peut contenir moins de 28 candidats</li>
          <li>✓ Salles de 29 ou 30 : autorisées pour IEPP avec effectifs > 28</li>
          <li>✓ Maximum <strong>16 salles</strong> par centre</li>
          <li>✓ Maximum <strong>480 candidats</strong> par centre</li>
        </ul>
      </div>

      {/* Actions */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <button
          onClick={() => setShowAddCentre(!showAddCentre)}
          className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-semibold"
        >
          + Ajouter un centre
        </button>
        <button
          onClick={calculerRepartition}
          disabled={loading || centres.length === 0}
          className="bg-[#1B89C7] text-white px-6 py-3 rounded-lg hover:bg-[#1565A0] transition-colors font-semibold disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          <span>Calculer répartition</span>
        </button>
        <button
          onClick={verifierDoublons}
          disabled={loading}
          className="bg-orange-600 text-white px-6 py-3 rounded-lg hover:bg-orange-700 transition-colors font-semibold disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          <AlertCircle className="w-5 h-5" />
          <span>Vérifier doublons</span>
        </button>
        <button
          onClick={exporterCSV}
          disabled={repartition.length === 0}
          className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors font-semibold disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          <Download className="w-5 h-5" />
          <span>Exporter CSV</span>
        </button>
      </div>

      {/* Formulaire ajout centre */}
      {showAddCentre && (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h3 className="font-bold text-lg mb-4">Ajouter un centre de composition</h3>
          <div className="flex space-x-4">
            <input
              type="text"
              value={nouveauCentre}
              onChange={(e) => setNouveauCentre(e.target.value)}
              placeholder="Nom du centre (ex: EPP SAKASSOU 1)"
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <button
              onClick={ajouterCentre}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
            >
              Ajouter
            </button>
            <button
              onClick={() => setShowAddCentre(false)}
              className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
            >
              Annuler
            </button>
          </div>
        </div>
      )}

      {/* Liste des centres */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-xl font-bold mb-4">Centres de composition ({centres.length})</h2>
        {centres.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Aucun centre. Ajoutez-en un pour commencer.</p>
        ) : (
          <div className="grid md:grid-cols-3 gap-4">
            {centres.map(centre => (
              <div key={centre.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 className="font-bold text-lg text-[#1B89C7]">{centre.nom}</h3>
                <p className="text-sm text-gray-600">Capacité: {centre.capacite_max} candidats</p>
                <p className="text-sm text-gray-600">Max: 16 salles</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Résultats de la répartition */}
      {repartition.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="p-6 bg-green-50 border-b">
            <h2 className="text-xl font-bold text-green-900 flex items-center space-x-2">
              <CheckCircle className="w-6 h-6" />
              <span>Répartition calculée - {repartition.length} écoles</span>
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left font-semibold">École</th>
                  <th className="px-6 py-4 text-left font-semibold">Centre de composition</th>
                  <th className="px-6 py-4 text-center font-semibold">Candidats</th>
                  <th className="px-6 py-4 text-center font-semibold">Salles</th>
                  <th className="px-6 py-4 text-left font-semibold">Détail des salles</th>
                </tr>
              </thead>
              <tbody>
                {repartition.map((r, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="px-6 py-4 font-medium">{r.ecole}</td>
                    <td className="px-6 py-4 text-blue-600">{r.centre}</td>
                    <td className="px-6 py-4 text-center font-bold">{r.nb_candidats}</td>
                    <td className="px-6 py-4 text-center">{r.nb_salles}</td>
                    <td className="px-6 py-4">
                      <div className="text-sm space-y-1">
                        {r.salles.map(salle => (
                          <div key={salle.numero_salle}>
                            Salle {salle.numero_salle}: <strong>{salle.nb_candidats}</strong> candidats
                          </div>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Repartition;
