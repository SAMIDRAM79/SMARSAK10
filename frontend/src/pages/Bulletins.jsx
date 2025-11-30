import React, { useState } from 'react';
import { studentsAPI, bulletinsAPI } from '../services/api';

const Bulletins = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [periode, setPeriode] = useState('trimestre_1');

  const handleGenerate = async () => {
    if (!selectedStudent) {
      alert('Sélectionnez un élève');
      return;
    }
    setLoading(true);
    try {
      const response = await bulletinsAPI.generate(selectedStudent, periode, '2024-2025');
      alert(`Bulletin généré! Moyenne: ${response.data.moyenne}/20, Rang: ${response.data.rang}, Appréciation: ${response.data.appreciation}`);
    } catch (error) {
      alert('Erreur: ' + (error.response?.data?.detail || 'Erreur'));
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    studentsAPI.getAll().then(r => setStudents(r.data));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Gestion des Bulletins</h1>
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="font-bold text-xl mb-4">Générer un bulletin</h3>
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <select value={selectedStudent} onChange={(e) => setSelectedStudent(e.target.value)} className="px-4 py-2 border rounded-lg">
            <option value="">Sélectionner un élève</option>
            {students.map(s => <option key={s.id} value={s.id}>{s.nom} {s.prenoms} - {s.classe}</option>)}
          </select>
          <select value={periode} onChange={(e) => setPeriode(e.target.value)} className="px-4 py-2 border rounded-lg">
            <option value="trimestre_1">Trimestre 1</option>
            <option value="trimestre_2">Trimestre 2</option>
            <option value="trimestre_3">Trimestre 3</option>
          </select>
          <button onClick={handleGenerate} disabled={loading} className="bg-[#1B89C7] text-white px-6 py-2 rounded-lg hover:bg-[#1565A0] disabled:opacity-50">
            {loading ? 'Génération...' : 'Générer le bulletin'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Bulletins;
