import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import api from '../services/api';
import { MapPin, School, Building2, Download, AlertCircle, CheckCircle, Users, Calculator, FileSpreadsheet } from 'lucide-react';

const RepartitionCEPE = () => {
  const [anneeScolaire, setAnneeScolaire] = useState('');
  const [centres, setCentres] = useState([]);
  const [ecoles, setEcoles] = useState([]);
  const [repartition, setRepartition] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [showCentreForm, setShowCentreForm] = useState(false);
  const [nouveauCentre, setNouveauCentre] = useState({ nom: '', capacite: 480, salles: 16 });
  const [affectations, setAffectations] = useState({});

  useEffect(() => {
    fetchParametres();
  }, []);

  useEffect(() => {
    if (anneeScolaire) {
      fetchCentres();
      fetchEcoles();
      fetchRepartition();
    }
  }, [anneeScolaire]);

  const fetchParametres = async () => {
    try {
      const response = await api.get('/parametres/');
      setAnneeScolaire(response.data.annee_scolaire_actuelle);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const fetchCentres = async () => {
    try {
      const response = await api.get('/centres/', {
        params: { annee_scolaire: anneeScolaire }
      });
      setCentres(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const fetchEcoles = async () => {
    try {
      const response = await api.get('/import/candidats/stats', {
        params: { annee_scolaire: anneeScolaire }
      });
      if (response.data.par_ecole) {
        const ecolesData = response.data.par_ecole.map(e => ({
          nom: e._id,
          total: e.total,
          centreAffecte: null
        }));
        setEcoles(ecolesData);
      }
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

  const creerCentre = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post('/centres/', null, {
        params: {
          nom: nouveauCentre.nom,
          capacite_max: nouveauCentre.capacite,
          nb_salles_fonctionnelles: nouveauCentre.salles,
          annee_scolaire: anneeScolaire
        }
      });
      setMessage({ type: 'success', text: 'Centre créé avec succès !' });
      setNouveauCentre({ nom: '', capacite: 480, salles: 16 });
      setShowCentreForm(false);
      fetchCentres();
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: 'Erreur lors de la création du centre' });
    } finally {
      setLoading(false);
    }
  };

  const affecterEcoleCentre = async (ecole, centreId) => {
    try {
      await api.post(`/centres/${centreId}/affecter-ecole`, null, {
        params: { codeecole: ecole }
      });
      setAffectations(prev => ({ ...prev, [ecole]: centreId }));
      setMessage({ type: 'success', text: `École affectée au centre` });
      setTimeout(() => setMessage({ type: '', text: '' }), 2000);
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: 'Erreur lors de l\'affectation' });
    }
  };

  const calculerRepartitionAuto = async () => {
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const response = await api.post('/repartition/calculer');
      setRepartition(response.data.repartition);
      setMessage({ 
        type: 'success', 
        text: `Répartition calculée ! ${response.data.total_ecoles} écoles, ${response.data.total_candidats} candidats dans ${response.data.centres_utilises} centres` 
      });
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Erreur lors de la répartition' });
    } finally {
      setLoading(false);
    }
  };

  const exporterRepartition = async (format) => {
    try {
      const response = await api.get('/repartition/export');
      
      if (format === 'csv') {
        const blob = new Blob([response.data.csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', response.data.filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
      
      setMessage({ type: 'success', text: 'Export réussi !' });
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: 'Erreur lors de l\'export' });
    }
  };

  const totalCandidats = ecoles.reduce((sum, e) => sum + e.total, 0);
  const capaciteTotale = centres.reduce((sum, c) => sum + c.capacite_max, 0);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
          <MapPin className="w-8 h-8" />
          Répartition des Candidats CEPE
        </h1>
        <p className="text-gray-600 mt-2">Gérez les centres d'examen et répartissez les candidats CM2</p>
      </div>

      {message.text && (
        <div className={`mb-4 p-4 rounded-lg flex items-center gap-2 ${
          message.type === 'success' 
            ? 'bg-green-100 text-green-800 border border-green-300' 
            : 'bg-red-100 text-red-800 border border-red-300'
        }`}>
          {message.type === 'success' ? 
            <CheckCircle className="w-5 h-5" /> : 
            <AlertCircle className="w-5 h-5" />
          }
          <span>{message.text}</span>
        </div>
      )}

      {/* Statistiques globales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Candidats CM2</p>
                <p className="text-2xl font-bold text-blue-600">{totalCandidats}</p>
              </div>
              <Users className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Centres Disponibles</p>
                <p className="text-2xl font-bold text-green-600">{centres.length}</p>
              </div>
              <Building2 className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Capacité Totale</p>
                <p className="text-2xl font-bold text-purple-600">{capaciteTotale}</p>
              </div>
              <School className="w-8 h-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Écoles</p>
                <p className="text-2xl font-bold text-orange-600">{ecoles.length}</p>
              </div>
              <School className="w-8 h-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Gestion des centres */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Centres d'Examen</span>
              <Button 
                size="sm" 
                onClick={() => setShowCentreForm(!showCentreForm)}
              >
                {showCentreForm ? 'Annuler' : '+ Nouveau'}
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {showCentreForm && (
              <form onSubmit={creerCentre} className="mb-4 p-3 bg-gray-50 rounded space-y-3">
                <div>
                  <Label>Nom du Centre</Label>
                  <input
                    type="text"
                    value={nouveauCentre.nom}
                    onChange={(e) => setNouveauCentre({...nouveauCentre, nom: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md text-sm"
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label>Capacité</Label>
                    <input
                      type="number"
                      value={nouveauCentre.capacite}
                      onChange={(e) => setNouveauCentre({...nouveauCentre, capacite: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border rounded-md text-sm"
                      max="480"
                    />
                  </div>
                  <div>
                    <Label>Salles</Label>
                    <input
                      type="number"
                      value={nouveauCentre.salles}
                      onChange={(e) => setNouveauCentre({...nouveauCentre, salles: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border rounded-md text-sm"
                      max="16"
                    />
                  </div>
                </div>
                <Button type="submit" size="sm" className="w-full" disabled={loading}>
                  Créer
                </Button>
              </form>
            )}

            <div className="space-y-2 max-h-96 overflow-y-auto">
              {centres.map((centre) => (
                <div key={centre.id} className="p-3 bg-blue-50 border border-blue-200 rounded">
                  <p className="font-semibold text-sm">{centre.nom}</p>
                  <div className="text-xs text-gray-600 mt-1 space-y-1">
                    <p>Capacité: {centre.capacite_max} candidats</p>
                    <p>Salles: {centre.nb_salles_fonctionnelles}</p>
                    <p>Écoles affectées: {centre.ecoles_affectees?.length || 0}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Affectation des écoles */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Affecter les Écoles aux Centres</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {ecoles.map((ecole) => (
                <div key={ecole.nom} className="flex items-center justify-between p-3 bg-gray-50 border rounded">
                  <div className="flex-1">
                    <p className="font-medium text-sm">{ecole.nom}</p>
                    <p className="text-xs text-gray-600">{ecole.total} candidats CM2</p>
                  </div>
                  <select
                    value={affectations[ecole.nom] || ''}
                    onChange={(e) => affecterEcoleCentre(ecole.nom, e.target.value)}
                    className="px-3 py-1 border rounded text-sm"
                  >
                    <option value="">Sélectionner un centre</option>
                    {centres.map((centre) => (
                      <option key={centre.id} value={centre.id}>{centre.nom}</option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Actions de répartition */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calculator className="w-5 h-5" />
            Calcul de la Répartition
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <Button 
              onClick={calculerRepartitionAuto}
              disabled={loading || centres.length === 0}
              className="flex items-center gap-2"
            >
              <Calculator className="w-4 h-4" />
              {loading ? 'Calcul en cours...' : 'Répartition Automatique'}
            </Button>
            
            <Button 
              onClick={() => exporterRepartition('csv')}
              disabled={repartition.length === 0}
              variant="outline"
              className="flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Exporter CSV
            </Button>

            <Button 
              onClick={() => exporterRepartition('excel')}
              disabled={repartition.length === 0}
              variant="outline"
              className="flex items-center gap-2"
            >
              <FileSpreadsheet className="w-4 h-4" />
              Exporter Excel
            </Button>
          </div>

          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded">
            <p className="font-semibold text-sm mb-2">Règles de répartition :</p>
            <ul className="text-xs text-gray-700 space-y-1">
              <li>✓ 28 candidats par salle (sauf dernière salle)</li>
              <li>✓ 29-30 candidats autorisés si effectif école &gt; 28</li>
              <li>✓ Maximum 16 salles par centre</li>
              <li>✓ Maximum 480 candidats par centre</li>
              <li>✓ Tri alphabétique des candidats CM2</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* Résultat de la répartition */}
      {repartition.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Résultat de la Répartition</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-100 border-b">
                    <th className="p-2 text-left">École</th>
                    <th className="p-2 text-left">Centre</th>
                    <th className="p-2 text-center">Candidats</th>
                    <th className="p-2 text-center">Salles</th>
                    <th className="p-2 text-left">Détails Salles</th>
                  </tr>
                </thead>
                <tbody>
                  {repartition.map((rep, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      <td className="p-2">{rep.ecole}</td>
                      <td className="p-2">{rep.centre}</td>
                      <td className="p-2 text-center font-semibold">{rep.nb_candidats}</td>
                      <td className="p-2 text-center">{rep.nb_salles}</td>
                      <td className="p-2">
                        <div className="flex gap-1 flex-wrap">
                          {rep.salles?.map((salle, i) => (
                            <span key={i} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                              S{salle.numero_salle}: {salle.nb_candidats}
                            </span>
                          ))}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default RepartitionCEPE;
