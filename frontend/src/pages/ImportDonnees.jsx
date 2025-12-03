import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import api from '../services/api';
import { Upload, FileText, Image, AlertCircle, CheckCircle, Users, Camera, Trash2 } from 'lucide-react';

const ImportDonnees = () => {
  const [anneeScolaire, setAnneeScolaire] = useState('');
  const [ecole, setEcole] = useState('');
  const [excelFile, setExcelFile] = useState(null);
  const [zipFile, setZipFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [stats, setStats] = useState(null);
  const [doublons, setDoublons] = useState([]);
  const [showDoublons, setShowDoublons] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  useEffect(() => {
    fetchAnneeScolaire();
  }, []);

  const fetchAnneeScolaire = async () => {
    try {
      const response = await api.get('/parametres/');
      setAnneeScolaire(response.data.annee_scolaire_actuelle);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const fetchStats = async () => {
    if (!anneeScolaire) return;
    try {
      const response = await api.get('/import/candidats/stats', {
        params: { annee_scolaire: anneeScolaire }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [anneeScolaire]);

  const handleExcelUpload = async (e) => {
    e.preventDefault();
    if (!excelFile || !anneeScolaire) {
      setMessage({ type: 'error', text: "Veuillez sélectionner un fichier Excel et vérifier l'année scolaire" });
      return;
    }

    setLoading(true);
    setMessage({ type: '', text: '' });
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', excelFile);
    formData.append('annee_scolaire', anneeScolaire);

    try {
      const response = await api.post('/import/excel/candidats', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        }
      });
      setMessage({ 
        type: 'success', 
        text: `Import réussi ! ${response.data.candidats_importes} candidats importés. ${response.data.erreurs > 0 ? `${response.data.erreurs} erreurs détectées.` : ''}` 
      });
      setExcelFile(null);
      fetchStats();
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: error.response?.data?.detail || "Erreur lors de l'importation" });
    } finally {
      setLoading(false);
      setUploadProgress(0);
    }
  };

  const handleZipUpload = async (e) => {
    e.preventDefault();
    if (!zipFile || !ecole) {
      setMessage({ type: 'error', text: "Veuillez sélectionner un fichier ZIP et spécifier l'école" });
      return;
    }

    setLoading(true);
    setMessage({ type: '', text: '' });

    const formData = new FormData();
    formData.append('file', zipFile);
    formData.append('ecole', ecole);

    try {
      const response = await api.post('/import/photos/zip', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setMessage({ 
        type: 'success', 
        text: `Import photos réussi ! ${response.data.photos_importees} photos importées.` 
      });
      setZipFile(null);
      setEcole('');
      fetchStats();
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: error.response?.data?.detail || "Erreur lors de l'importation des photos" });
    } finally {
      setLoading(false);
    }
  };

  const handleEpurationDoublons = async (mode) => {
    setLoading(true);
    setMessage({ type: '', text: '' });

    const formData = new FormData();
    formData.append('annee_scolaire', anneeScolaire);

    try {
      const response = await api.post('/import/epuration/doublons', formData, {
        params: { mode }
      });
      
      if (mode === 'manuel' && response.data.doublons) {
        setDoublons(response.data.doublons);
        setShowDoublons(true);
        setMessage({ type: 'success', text: `${response.data.doublons.length} doublon(s) détecté(s)` });
      } else {
        setMessage({ 
          type: 'success', 
          text: `Épuration terminée ! ${response.data.doublons_supprimes} doublon(s) supprimé(s).` 
        });
        fetchStats();
      }
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: "Erreur lors de l'épuration" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
          <Upload className="w-8 h-8" />
          Import des Données
        </h1>
        <p className="text-gray-600 mt-2">Importez les candidats et leurs photos depuis les fichiers AGCEPE/DECO</p>
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

      {/* Statistiques */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Candidats</p>
                  <p className="text-2xl font-bold text-blue-600">{stats.total_candidats}</p>
                </div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Avec Photos</p>
                  <p className="text-2xl font-bold text-green-600">{stats.candidats_avec_photo}</p>
                </div>
                <Camera className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Taux Photos</p>
                  <p className="text-2xl font-bold text-purple-600">{stats.taux_photos}%</p>
                </div>
                <CheckCircle className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Import Excel */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Importer les Candidats (Excel)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleExcelUpload} className="space-y-4">
              <div>
                <Label>Année Scolaire</Label>
                <input
                  type="text"
                  value={anneeScolaire}
                  onChange={(e) => setAnneeScolaire(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>

              <div>
                <Label>Fichier Excel (Canevas AGCEPE)</Label>
                <input
                  type="file"
                  accept=".xls,.xlsx"
                  onChange={(e) => setExcelFile(e.target.files[0])}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
                <p className="text-sm text-gray-500 mt-1">Format: .xls ou .xlsx</p>
              </div>

              {loading && uploadProgress > 0 && (
                <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
                  <div 
                    className="bg-blue-600 h-2.5 rounded-full transition-all duration-300" 
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                  <p className="text-sm text-center text-gray-600 mt-1">{uploadProgress}% téléchargé...</p>
                </div>
              )}

              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={loading}>
                <FileText className="w-4 h-4 mr-2" />
                {loading ? 'Importation en cours...' : 'Importer les Candidats'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Import Photos ZIP */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Image className="w-5 h-5" />
              Importer les Photos (ZIP)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleZipUpload} className="space-y-4">
              <div>
                <Label>École</Label>
                <input
                  type="text"
                  value={ecole}
                  onChange={(e) => setEcole(e.target.value)}
                  placeholder="Nom de l'école"
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>

              <div>
                <Label>Fichier ZIP (Photos nommées par matricule)</Label>
                <input
                  type="file"
                  accept=".zip"
                  onChange={(e) => setZipFile(e.target.files[0])}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
                <p className="text-sm text-gray-500 mt-1">Format: matricule.jpg (ex: 12345.jpg)</p>
              </div>

              <Button type="submit" className="w-full" disabled={loading}>
                <Image className="w-4 h-4 mr-2" />
                {loading ? 'Importation...' : 'Importer les Photos'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Épuration des doublons */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trash2 className="w-5 h-5" />
            Épuration des Doublons
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <Button 
              onClick={() => handleEpurationDoublons('automatique')} 
              disabled={loading}
              variant="destructive"
            >
              Épuration Automatique
            </Button>
            <Button 
              onClick={() => handleEpurationDoublons('manuel')} 
              disabled={loading}
              variant="outline"
            >
              Détecter les Doublons
            </Button>
          </div>

          {showDoublons && doublons.length > 0 && (
            <div className="mt-4">
              <h3 className="font-semibold mb-2">Doublons détectés:</h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {doublons.map((doublon, index) => (
                  <div key={index} className="p-3 bg-yellow-50 border border-yellow-200 rounded">
                    <p className="font-medium">{doublon.noms} {doublon.prenoms}</p>
                    <p className="text-sm text-gray-600">Matricule: {doublon.matricule}</p>
                    <p className="text-sm text-gray-600">Occurrences: {doublon.occurrences}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ImportDonnees;
