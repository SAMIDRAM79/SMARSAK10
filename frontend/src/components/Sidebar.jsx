import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, Users, BookOpen, FileText, GraduationCap, 
  Calendar, CreditCard, BarChart, IdCard, Clipboard
} from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/', icon: Home, label: 'Tableau de bord' },
    { path: '/students', icon: Users, label: 'Élèves' },
    { path: '/classes', icon: BookOpen, label: 'Classes' },
    { path: '/notes', icon: FileText, label: 'Notes' },
    { path: '/bulletins', icon: GraduationCap, label: 'Bulletins' },
    { path: '/cartes', icon: IdCard, label: 'Cartes scolaires' },
    { path: '/fiches-eps', icon: Clipboard, label: 'Fiches EPS' },
    { path: '/enseignants', icon: Users, label: 'Enseignants' },
    { path: '/emploi-temps', icon: Calendar, label: 'Emploi du temps' },
    { path: '/comptabilite', icon: CreditCard, label: 'Comptabilité' },
    { path: '/rapports', icon: BarChart, label: 'Rapports' },
  ];

  return (
    <div className="w-64 bg-gradient-to-b from-[#1B89C7] to-[#1565A0] text-white min-h-screen fixed left-0 top-0 shadow-2xl">
      <div className="p-6">
        <div className="flex items-center justify-center mb-4">
          <img src="/logo-iepp.jpg" alt="IEPP SAKASSOU" className="w-32 h-32 rounded-full bg-white p-2" />
        </div>
        <h1 className="text-3xl font-bold mb-2 text-center">SMARTSAK10</h1>
        <p className="text-sm opacity-90 text-center">Gestion Scolaire</p>
        <div className="mt-4 p-3 bg-white bg-opacity-20 rounded-lg">
          <p className="text-xs font-semibold">Administrateur</p>
          <p className="text-xs opacity-90 truncate">konatdra@gmail.com</p>
        </div>
      </div>

      <nav className="mt-6">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-6 py-3 transition-all ${
                isActive
                  ? 'bg-white text-[#1B89C7] font-semibold border-r-4 border-white'
                  : 'hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="absolute bottom-4 left-0 right-0 px-6">
        <div className="text-xs opacity-75 text-center">
          <p>Année scolaire 2024-2025</p>
          <p className="mt-1">Version 1.0.0</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
