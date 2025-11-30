import React, { useState, useEffect } from 'react';
import { enseignantsAPI } from '../services/api';

const Enseignants = () => {
  const [enseignants, setEnseignants] = useState([]);

  useEffect(() => {
    fetchEnseignants();
  }, []);

  const fetchEnseignants = async () => {
    try {
      const response = await enseignantsAPI.getAll();
      setEnseignants(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Gestion des Enseignants</h1>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-4 text-left">Matricule</th>
              <th className="px-6 py-4 text-left">Nom & Prénoms</th>
              <th className="px-6 py-4 text-left">Spécialité</th>
              <th className="px-6 py-4 text-left">Téléphone</th>
            </tr>
          </thead>
          <tbody>
            {enseignants.map(ens => (
              <tr key={ens.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4">{ens.matricule}</td>
                <td className="px-6 py-4">{ens.nom} {ens.prenoms}</td>
                <td className="px-6 py-4">{ens.specialite}</td>
                <td className="px-6 py-4">{ens.telephone}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Enseignants;
