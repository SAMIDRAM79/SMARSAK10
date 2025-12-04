import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import api from '../services/api';
import { CreditCard, Download, Printer, AlertCircle, CheckCircle } from 'lucide-react';

const CartesGeneration = () => {
  const [anneeScolaire, setAnneeScolaire] = useState('');
  const [ecoleSelectionnee, setEcoleSelectionnee] = useState('');
  const [ecoles, setEcoles] = useState([]);
  const [modeleSelectionne, setModeleSelectionne] = useState('standard');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchParametres();
  }, []);

  useEffect(() => {
    if (anneeScolaire) {
      fetchEcoles();
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

  const fetchEcoles = async () => {
    try {
      const response = await api.get('/import/candidats/stats', {
        params: { annee_scolaire: anneeScolaire }
      });
      if (response.data.par_ecole) {
        const ecolesUniques = response.data.par_ecole.map(e => e._id);
        setEcoles(ecolesUniques);
      }
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const modeles = [
    {
      id: 'standard',
      nom: 'Standard Bleu-Vert Vif',
      description: '8 cartes avec logo, couleurs vives',
      couleurs: ['#0066CC', '#00CC66', '#FFFFFF']
    },
    {
      id: 'logo_blanc',
      nom: 'Violet Vif avec Logo',
      description: '8 cartes logo IEPP, bordure violette vive',
      couleurs: ['#9C27B0', '#AB47BC', '#FFFFFF']
    },
    {
      id: 'logo_couleur',
      nom: 'Orange-Jaune Vif avec Logo',
      description: '8 cartes logo, fond jaune et orange vif',
      couleurs: ['#FFF9C4', '#FF6F00', '#FFB300']
    },
    {
      id: 'drapeau_ivoirien',
      nom: 'Drapeau Ivoirien 🇨🇮 avec Logo',
      description: '8 cartes logo, couleurs nationales vives',
      couleurs: ['#00A86B', '#FFFFFF', '#FF8C00']
    }
  ];

  const genererCartes = async () => {
    if (!ecoleSelectionnee) {
      setMessage({ type: 'error', text: "Veuillez sélectionner une école" });
      return;
    }

    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      // Appel API pour générer le PDF des cartes
      const response = await api.post('/cartes/generer', null, {
        params: {
          ecole: ecoleSelectionnee,
          modele: modeleSelectionne,
          annee_scolaire: anneeScolaire
        },
        responseType: 'blob'
      });

      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cartes_${ecoleSelectionnee}_${modeleSelectionne}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage({ type: 'success', text: 'Cartes générées avec succès !' });
    } catch (error) {
      console.error('Erreur:', error);
      let errorMessage = "Erreur lors de la génération des cartes";
      
      // Si c'est une réponse blob, ne pas essayer d'accéder à response.data.detail
      if (error.response && error.response.data instanceof Blob) {
        try {
          const text = await error.response.data.text();
          const jsonError = JSON.parse(text);
          errorMessage = jsonError.detail || errorMessage;
        } catch {
          errorMessage = "Erreur lors de la génération des cartes";
        }
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
          <CreditCard className="w-8 h-8" />
          Génération des Cartes Scolaires
        </h1>
        <p className="text-gray-600 mt-2">Créez des cartes scolaires (8 par page A4) avec différents modèles</p>
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

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Configuration</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>École</Label>
              <select
                value={ecoleSelectionnee}
                onChange={(e) => setEcoleSelectionnee(e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
              >
                <option value="">Sélectionner une école</option>
                {ecoles.map((ecole, index) => (
                  <option key={index} value={ecole}>{ecole}</option>
                ))}
              </select>
            </div>

            <div>
              <Label>Année Scolaire</Label>
              <input
                type="text"
                value={anneeScolaire}
                onChange={(e) => setAnneeScolaire(e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
                readOnly
              />
            </div>

            <Button 
              onClick={genererCartes} 
              className="w-full" 
              disabled={loading || !ecoleSelectionnee}
            >
              <Download className="w-4 h-4 mr-2" />
              {loading ? 'Génération...' : 'Générer PDF (A4)'}
            </Button>
          </CardContent>
        </Card>

        {/* Modèles */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Choisir un Modèle</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {modeles.map((modele) => (
                  <div
                    key={modele.id}
                    onClick={() => setModeleSelectionne(modele.id)}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      modeleSelectionne === modele.id
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold">{modele.nom}</h3>
                      {modeleSelectionne === modele.id && (
                        <CheckCircle className="w-5 h-5 text-blue-600" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{modele.description}</p>
                    <div className="flex gap-2">
                      {modele.couleurs.map((couleur, index) => (
                        <div
                          key={index}
                          className="w-12 h-12 rounded border"
                          style={{ backgroundColor: couleur }}
                          title={couleur}
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg border border-blue-200">
                <h4 className="font-semibold mb-2 text-blue-800">✨ Informations sur les cartes :</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li>✓ 8 cartes par page A4</li>
                  <li>✓ Photo du candidat</li>
                  <li>✓ Matricule, Nom, Prénoms</li>
                  <li>✓ Date de naissance</li>
                  <li>✓ Nom de l&apos;école</li>
                  <li>✓ Classe et Niveau</li>
                  <li>✓ Emplacement émargement directeur</li>
                  <li>✓ <strong>Logo IEPP SAKASSOU sur TOUTES les cartes</strong></li>
                  <li>✓ <strong>Couleurs vives et attrayantes</strong></li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default CartesGeneration;
