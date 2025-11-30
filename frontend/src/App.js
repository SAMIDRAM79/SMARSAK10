import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Parametres from './pages/Parametres';
import ImportDonnees from './pages/ImportDonnees';
import RepartitionCEPE from './pages/RepartitionCEPE';
import CartesGeneration from './pages/CartesGeneration';
import Students from './pages/Students';
import Classes from './pages/Classes';
import Notes from './pages/Notes';
import Bulletins from './pages/Bulletins';
import Cartes from './pages/Cartes';
import FichesEPS from './pages/FichesEPS';
import Enseignants from './pages/Enseignants';
import EmploiTemps from './pages/EmploiTemps';
import Comptabilite from './pages/Comptabilite';
import Rapports from './pages/Rapports';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/parametres" element={<Parametres />} />
            <Route path="/import" element={<ImportDonnees />} />
            <Route path="/repartition" element={<Repartition />} />
            <Route path="/cartes-generation" element={<CartesGeneration />} />
            <Route path="/students" element={<Students />} />
            <Route path="/classes" element={<Classes />} />
            <Route path="/notes" element={<Notes />} />
            <Route path="/bulletins" element={<Bulletins />} />
            <Route path="/cartes" element={<Cartes />} />
            <Route path="/fiches-eps" element={<FichesEPS />} />
            <Route path="/enseignants" element={<Enseignants />} />
            <Route path="/emploi-temps" element={<EmploiTemps />} />
            <Route path="/comptabilite" element={<Comptabilite />} />
            <Route path="/rapports" element={<Rapports />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </div>
  );
}

export default App;