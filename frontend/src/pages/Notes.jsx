import React, { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import { studentsAPI, matieresAPI, notesAPI, classesAPI } from '../services/api';

const Notes = () => {
  const [students, setStudents] = useState([]);
  const [matieres, setMatieres] = useState([]);
  const [classes, setClasses] = useState([]);
  const [selectedClasse, setSelectedClasse] = useState('');
  const [selectedMatiere, setSelectedMatiere] = useState('');
  const [selectedPeriode, setSelectedPeriode] = useState('trimestre_1');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    student_id: '',
    matiere_id: '',
    type_examen: 'devoir',
    note: '',
    note_sur: 20,
    periode: 'trimestre_1',
    annee_scolaire: '2024-2025',
    observation: ''
  });

  useEffect(() => {
    fetchClasses();
    fetchMatieres();
  }, []);

  useEffect(() => {
    if (selectedClasse) {
      fetchStudents();
    }
  }, [selectedClasse]);

  const fetchClasses = async () => {
    try {
      const response = await classesAPI.getAll();
      setClasses(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const fetchMatieres = async () => {
    try {
      const response = await matieresAPI.getAll();
      setMatieres(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await studentsAPI.getAll(null, selectedClasse);
      setStudents(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await notesAPI.create(formData);
      setShowModal(false);
      alert('Note enregistrée avec succès!');
      setFormData({
        student_id: '',
        matiere_id: '',
        type_examen: 'devoir',
        note: '',
        note_sur: 20,
        periode: 'trimestre_1',
        annee_scolaire: '2024-2025',
        observation: ''
      });
    } catch (error) {
      alert('Erreur: ' + (error.response?.data?.detail || 'Erreur'));
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Gestion des Notes</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-[#1B89C7] text-white px-6 py-3 rounded-lg hover:bg-[#1565A0] flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Nouvelle note</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="grid md:grid-cols-4 gap-4">
          <select
            value={selectedClasse}
            onChange={(e) => setSelectedClasse(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="">Sélectionner une classe</option>
            {classes.map(c => (
              <option key={c.id} value={c.nom}>{c.nom}</option>
            ))}
          </select>
          <select
            value={selectedMatiere}
            onChange={(e) => setSelectedMatiere(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="">Toutes les matières</option>
            {matieres.map(m => (
              <option key={m.id} value={m.id}>{m.nom}</option>
            ))}
          </select>
          <select
            value={selectedPeriode}
            onChange={(e) => setSelectedPeriode(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="trimestre_1">Trimestre 1</option>
            <option value="trimestre_2">Trimestre 2</option>
            <option value="trimestre_3">Trimestre 3</option>
          </select>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="font-bold text-xl mb-4">Élèves de la classe {selectedClasse}</h3>
        {!selectedClasse ? (
          <p className="text-gray-500 text-center py-8">Veuillez sélectionner une classe</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left">Matricule</th>
                  <th className="px-4 py-3 text-left">Nom & Prénoms</th>
                  <th className="px-4 py-3 text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {students.map(student => (
                  <tr key={student.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3">{student.matricule}</td>
                    <td className="px-4 py-3">{student.nom} {student.prenoms}</td>
                    <td className="px-4 py-3 text-center">
                      <button className="text-blue-600 hover:underline">Voir notes</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto m-4">
            <div className="p-6 border-b">
              <h2 className="text-2xl font-bold">Saisir une note</h2>
            </div>
            <form onSubmit={handleSubmit} className="p-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Élève *</label>
                  <select
                    required
                    value={formData.student_id}
                    onChange={(e) => setFormData({...formData, student_id: e.target.value})}
                    className="w-full px-4 py-2 border rounded-lg"
                  >
                    <option value="">Sélectionner</option>
                    {students.map(s => (
                      <option key={s.id} value={s.id}>{s.nom} {s.prenoms}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Matière *</label>
                  <select
                    required
                    value={formData.matiere_id}
                    onChange={(e) => {
                      const matiere = matieres.find(m => m.id === e.target.value);
                      setFormData({...formData, matiere_id: e.target.value, note_sur: matiere?.note_sur || 20});
                    }}
                    className="w-full px-4 py-2 border rounded-lg"
                  >
                    <option value="">Sélectionner</option>
                    {matieres.map(m => (
                      <option key={m.id} value={m.id}>{m.nom} (/{m.note_sur})</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Type examen *</label>
                  <select
                    required
                    value={formData.type_examen}
                    onChange={(e) => setFormData({...formData, type_examen: e.target.value})}
                    className="w-full px-4 py-2 border rounded-lg"
                  >
                    <option value="devoir">Devoir</option>
                    <option value="composition">Composition</option>
                    <option value="examen_blanc">Examen blanc</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Note * (/{formData.note_sur})</label>
                  <input
                    type="number"
                    step="0.5"
                    required
                    max={formData.note_sur}
                    value={formData.note}
                    onChange={(e) => setFormData({...formData, note: e.target.value})}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Période *</label>
                  <select
                    required
                    value={formData.periode}
                    onChange={(e) => setFormData({...formData, periode: e.target.value})}
                    className="w-full px-4 py-2 border rounded-lg"
                  >
                    <option value="trimestre_1">Trimestre 1</option>
                    <option value="trimestre_2">Trimestre 2</option>
                    <option value="trimestre_3">Trimestre 3</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Observation</label>
                  <input
                    type="text"
                    value={formData.observation}
                    onChange={(e) => setFormData({...formData, observation: e.target.value})}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-4 mt-6">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-6 py-2 border rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-[#1B89C7] text-white rounded-lg hover:bg-[#1565A0]"
                >
                  Enregistrer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Notes;
