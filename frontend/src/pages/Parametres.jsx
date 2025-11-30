import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import api from '../services/api';
import { Settings, Save, AlertCircle, CheckCircle } from 'lucide-react';

const Parametres = () => {
  const [parametres, setParametres] = useState({
    annee_scolaire_actuelle: '',
    session_examen: '',
    drena: '',
    iepp: '',
    region: '',
    date_examen: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchParametres();
  }, []);

  const fetchParametres = async () => {
    try {
      const response = await api.get('/parametres/');
      setParametres(response.data);
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: 'Erreur lors du chargement des paramètres' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setParametres(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      await api.put('/parametres/', null, { params: parametres });
      setMessage({ type: 'success', text: 'Paramètres mis à jour avec succès !' });
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (error) {
      console.error('Erreur:', error);
      setMessage({ type: 'error', text: 'Erreur lors de la mise à jour' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
          <Settings className="w-8 h-8" />
          Paramètres de l'Application
        </h1>
        <p className="text-gray-600 mt-2">Configurez les paramètres globaux de SMARTSAK10</p>
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

      <Card>
        <CardHeader>
          <CardTitle>Paramètres Généraux</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="annee_scolaire_actuelle">Année Scolaire Actuelle *</Label>
                <Input
                  id="annee_scolaire_actuelle"
                  name="annee_scolaire_actuelle"
                  value={parametres.annee_scolaire_actuelle}
                  onChange={handleChange}
                  placeholder="2024-2025"
                  required
                />
              </div>

              <div>
                <Label htmlFor="session_examen">Session d'Examen *</Label>
                <Input
                  id="session_examen"
                  name="session_examen"
                  value={parametres.session_examen}
                  onChange={handleChange}
                  placeholder="2025"
                  required
                />
              </div>

              <div>
                <Label htmlFor="region">Région *</Label>
                <Input
                  id="region"
                  name="region"
                  value={parametres.region}
                  onChange={handleChange}
                  placeholder="GBEKE"
                  required
                />
              </div>

              <div>
                <Label htmlFor="drena">DRENA *</Label>
                <Input
                  id="drena"
                  name="drena"
                  value={parametres.drena}
                  onChange={handleChange}
                  placeholder="BOUAKE 2"
                  required
                />
              </div>

              <div>
                <Label htmlFor="iepp">IEPP *</Label>
                <Input
                  id="iepp"
                  name="iepp"
                  value={parametres.iepp}
                  onChange={handleChange}
                  placeholder="SAKASSOU"
                  required
                />
              </div>

              <div>
                <Label htmlFor="date_examen">Date d'Examen (Optionnel)</Label>
                <Input
                  id="date_examen"
                  name="date_examen"
                  type="date"
                  value={parametres.date_examen || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={fetchParametres}
                disabled={saving}
              >
                Annuler
              </Button>
              <Button type="submit" disabled={saving}>
                <Save className="w-4 h-4 mr-2" />
                {saving ? 'Enregistrement...' : 'Enregistrer'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Parametres;
