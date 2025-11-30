import React, { useState, useEffect } from 'react';
import { classesAPI } from '../services/api';

const Classes = () => {
  const [classes, setClasses] = useState([]);

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    try {
      const response = await classesAPI.getAll();
      setClasses(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Gestion des Classes</h1>
      <div className="grid md:grid-cols-3 gap-6">
        {classes.map(classe => (
          <div key={classe.id} className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-2xl font-bold text-[#1B89C7] mb-2">{classe.nom}</h3>
            <p className="text-gray-600 capitalize mb-4">{classe.niveau.replace('_', ' ')}</p>
            <div className="flex justify-between text-sm">
              <span>Effectif: <strong>{classe.effectif_actuel}/{classe.effectif_max}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Classes;
