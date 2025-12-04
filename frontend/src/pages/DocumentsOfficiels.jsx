import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import api from '../services/api';
import { FileText, Download, AlertCircle, CheckCircle, FileSpreadsheet, Clipboard, Users } from 'lucide-react';

const DocumentsOfficiels = () => {
  const [anneeScolaire, setAnneeScolaire] = useState('');
  const [centre, setCentre] = useState('');
  const [centres, setCentres] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchParametres();
    fetchCentres();
  }, []);

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
      const response = await api.get('/centres/');
      setCentres(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const genererDocument = async (typeDocument) => {
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const endpoint = `/documents/${typeDocument}`;
      const params = {
        annee_scolaire: anneeScolaire,
        ...(centre && { centre })
      };

      const response = await api.get(endpoint, {
        params,
        responseType: 'blob'
      });

      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${typeDocument}_${anneeScolaire}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage({ type: 'success', text: 'Document généré avec succès !' });
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || "Erreur lors de la génération du document. Cette fonctionnalité sera bientôt disponible." 
      });
    } finally {
      setLoading(false);
    }
  };

  const documents = [
    {
      id: 'convocations',
      nom: 'Convocations des Élèves',
      description: 'Convocations individuelles avec photos',
      icon: FileText,
      needsCentre: true
    },
    {
      id: 'fiches-eps',
      nom: 'Fiches EPS',
      description: 'Fiches d\'éducation physique et sportive',
      icon: Clipboard,
      needsCentre: true
    },
    {
      id: 'listing-centre',
      nom: 'Listing des Centres',
      description: 'Liste des centres d\'examen et effectifs',
      icon: FileSpreadsheet,
      needsCentre: false
    },
    {
      id: 'liste-emargement',
      nom: 'Listes d\'Émargement',
      description: 'Feuilles d\'émargement par centre',
      icon: Users,
      needsCentre: true
    },
    {
      id: 'annexe-2',
      nom: 'Annexe II',
      description: 'Annexe II - Format officiel DECO',
      icon: FileText,
      needsCentre: true
    },
    {
      id: 'annexe-3',
      nom: 'Annexe III',
      description: 'Annexe III - Format officiel DECO',
      icon: FileText,
      needsCentre: true
    }
  ];

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
          <FileSpreadsheet className="w-8 h-8" />
          Documents Officiels
        </h1>
        <p className="text-gray-600 mt-2">Générez les documents officiels conformes aux modèles DECO</p>
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

      {/* Filtres */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Paramètres</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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

            <div>
              <Label>Centre (optionnel)</Label>
              <select
                value={centre}
                onChange={(e) => setCentre(e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
              >
                <option value="">Tous les centres</option>
                {centres.map((c, index) => (
                  <option key={index} value={c.nom}>{c.nom}</option>
                ))}
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Liste des documents */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {documents.map((doc) => {
          const Icon = doc.icon;
          return (
            <Card key={doc.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Icon className="w-5 h-5 text-blue-600" />
                  {doc.nom}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 mb-4">{doc.description}</p>
                <Button
                  onClick={() => genererDocument(doc.id)}
                  className="w-full"
                  disabled={loading || (doc.needsCentre && !centre)}
                >
                  <Download className="w-4 h-4 mr-2" />
                  {loading ? 'Génération...' : 'Générer PDF'}
                </Button>
                {doc.needsCentre && !centre && (
                  <p className="text-xs text-amber-600 mt-2">
                    ⚠️ Sélectionnez un centre
                  </p>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Avertissement */}
      <Card className="mt-6 bg-amber-50 border-amber-200">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-6 h-6 text-amber-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-amber-900 mb-2">
                🚧 Fonctionnalité en développement
              </h3>
              <p className="text-sm text-amber-800">
                La génération des documents officiels (Convocations, Fiches EPS, Annexes, etc.) 
                est actuellement en cours de développement. Cette fonctionnalité sera disponible 
                dans la prochaine version de SMARTSAK10.
              </p>
              <p className="text-sm text-amber-800 mt-2">
                Les documents générés seront conformes aux modèles officiels de la DECO 
                (Direction des Examens et Concours de Côte d'Ivoire).
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DocumentsOfficiels;
