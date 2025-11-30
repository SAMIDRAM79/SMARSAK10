import React, { useState, useEffect } from 'react';
import { Plus, Search, Edit, Trash2 } from 'lucide-react';
import { studentsAPI, classesAPI } from '../services/api';

const Students = () => {
  const [students, setStudents] = useState([]);
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterNiveau, setFilterNiveau] = useState('');
  const [filterClasse, setFilterClasse] = useState('');
  const [formData, setFormData] = useState({
    matricule: '',
    nom: '',
    prenoms: '',
    date_naissance: '',
    lieu_naissance: '',
    genre: 'masculin',
    niveau: 'primaire',
    classe: '',
    nom_pere: '',
    nom_mere: '',
    telephone_tuteur: '',
    adresse: ''
  });

  useEffect(() => {
    fetchStudents();
    fetchClasses();
  }, [filterNiveau, filterClasse]);

  const fetchStudents = async () => {
    try {
      const response = await studentsAPI.getAll(filterNiveau, filterClasse);
      setStudents(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchClasses = async () => {
    try {
      const response = await classesAPI.getAll();
      setClasses(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await studentsAPI.create(formData);
      setShowModal(false);
      fetchStudents();
      // Reset form
      setFormData({
        matricule: '',
        nom: '',
        prenoms: '',
        date_naissance: '',
        lieu_naissance: '',
        genre: 'masculin',
        niveau: 'primaire',
        classe: '',
        nom_pere: '',
        nom_mere: '',
        telephone_tuteur: '',
        adresse: ''
      });
    } catch (error) {
      alert('Erreur lors de l\'inscription: ' + (error.response?.data?.detail || 'Erreur'));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet élève ?')) {
      try {
        await studentsAPI.delete(id);
        fetchStudents();
      } catch (error) {
        alert('Erreur lors de la suppression');
      }
    }
  };

  const filteredStudents = students.filter(student =>
    student.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.prenoms.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.matricule.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Gestion des Élèves</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-[#1B89C7] text-white px-6 py-3 rounded-lg hover:bg-[#1565A0] transition-colors flex items-center space-x-2 shadow-lg"
        >
          <Plus className="w-5 h-5" />
          <span>Nouvel élève</span>
        </button>
      </div>

      {/* Filtres */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="grid md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Rechercher..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
            />
          </div>
          <select
            value={filterNiveau}
            onChange={(e) => setFilterNiveau(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
          >
            <option value="">Tous les niveaux</option>
            <option value="pre_primaire">Pré-primaire</option>
            <option value="maternelle">Maternelle</option>
            <option value="primaire">Primaire</option>
          </select>
          <select
            value={filterClasse}
            onChange={(e) => setFilterClasse(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
          >
            <option value="">Toutes les classes</option>
            {classes.map(c => (
              <option key={c.id} value={c.nom}>{c.nom}</option>
            ))}
          </select>
          <div className="text-sm text-gray-600 flex items-center">
            <span className="font-semibold">{filteredStudents.length}</span>&nbsp;élève(s)
          </div>
        </div>
      </div>

      {/* Liste des élèves */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Matricule</th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Nom & Prénoms</th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Genre</th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Classe</th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Téléphone</th>
                <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                    Chargement...
                  </td>
                </tr>
              ) : filteredStudents.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                    Aucun élève trouvé
                  </td>
                </tr>
              ) : (
                filteredStudents.map(student => (
                  <tr key={student.id} className="border-b hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-800">{student.matricule}</td>
                    <td className="px-6 py-4">
                      <div className="font-medium text-gray-800">{student.nom}</div>
                      <div className="text-sm text-gray-600">{student.prenoms}</div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600 capitalize">{student.genre}</td>
                    <td className="px-6 py-4">
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                        {student.classe}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{student.telephone_tuteur}</td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center space-x-2">
                        <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          onClick={() => handleDelete(student.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal d'ajout */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b">
              <h2 className="text-2xl font-bold text-gray-800">Inscription d'un nouvel élève</h2>
            </div>
            <form onSubmit={handleSubmit} className="p-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Matricule *</label>
                  <input
                    type="text"
                    required
                    value={formData.matricule}
                    onChange={(e) => setFormData({...formData, matricule: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nom *</label>
                  <input
                    type="text"
                    required
                    value={formData.nom}
                    onChange={(e) => setFormData({...formData, nom: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Prénoms *</label>
                  <input
                    type="text"
                    required
                    value={formData.prenoms}
                    onChange={(e) => setFormData({...formData, prenoms: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Date de naissance *</label>
                  <input
                    type="date"
                    required
                    value={formData.date_naissance}
                    onChange={(e) => setFormData({...formData, date_naissance: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Lieu de naissance *</label>
                  <input
                    type="text"
                    required
                    value={formData.lieu_naissance}
                    onChange={(e) => setFormData({...formData, lieu_naissance: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Genre *</label>
                  <select
                    required
                    value={formData.genre}
                    onChange={(e) => setFormData({...formData, genre: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  >
                    <option value="masculin">Masculin</option>
                    <option value="feminin">Féminin</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Niveau *</label>
                  <select
                    required
                    value={formData.niveau}
                    onChange={(e) => setFormData({...formData, niveau: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  >
                    <option value="pre_primaire">Pré-primaire</option>
                    <option value="maternelle">Maternelle</option>
                    <option value="primaire">Primaire</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Classe *</label>
                  <select
                    required
                    value={formData.classe}
                    onChange={(e) => setFormData({...formData, classe: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  >
                    <option value="">Sélectionner une classe</option>
                    {classes.filter(c => c.niveau === formData.niveau).map(c => (
                      <option key={c.id} value={c.nom}>{c.nom}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nom du père</label>
                  <input
                    type="text"
                    value={formData.nom_pere}
                    onChange={(e) => setFormData({...formData, nom_pere: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nom de la mère</label>
                  <input
                    type="text"
                    value={formData.nom_mere}
                    onChange={(e) => setFormData({...formData, nom_mere: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Téléphone tuteur *</label>
                  <input
                    type="tel"
                    required
                    value={formData.telephone_tuteur}
                    onChange={(e) => setFormData({...formData, telephone_tuteur: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Adresse *</label>
                  <input
                    type="text"
                    required
                    value={formData.adresse}
                    onChange={(e) => setFormData({...formData, adresse: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-4 mt-6">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-[#1B89C7] text-white rounded-lg hover:bg-[#1565A0] transition-colors"
                >
                  Inscrire l'élève
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Students;
