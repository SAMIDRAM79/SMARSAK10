import React, { useState } from 'react';
import { MessageCircle, Phone, Mail, FileText } from 'lucide-react';
import Header from '../components/Header';
import { ticketAPI } from '../services/api';

const SupportPage = () => {
  const [ticketData, setTicketData] = useState({
    name: '',
    email: '',
    subject: '',
    priority: 'normal',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const response = await ticketAPI.createTicket(ticketData);
      setSuccess(`Ticket créé avec succès! Numéro de ticket: ${response.data.ticket_number}`);
      
      // Reset form
      setTicketData({
        name: '',
        email: '',
        subject: '',
        priority: 'normal',
        description: '',
      });
    } catch (err) {
      setError('Erreur lors de la création du ticket. Veuillez réessayer.');
      console.error('Ticket error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setTicketData({
      ...ticketData,
      [e.target.name]: e.target.value,
    });
  };

  const faqItems = [
    {
      question: 'Comment installer SmartIEPP ?',
      answer: 'Téléchargez le kit complet, exécutez le fichier .exe et suivez les instructions d\'installation.',
    },
    {
      question: 'Quelle est la configuration minimale requise ?',
      answer: 'Windows 7 ou supérieur, 4GB RAM, 500MB d\'espace disque disponible.',
    },
    {
      question: 'Comment mettre à jour le logiciel ?',
      answer: 'Téléchargez la mise à jour depuis notre page de téléchargement et exécutez-la.',
    },
    {
      question: 'Le support technique est-il inclus ?',
      answer: 'Oui, le support technique est inclus pour tous nos clients avec une licence active.',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Support Technique</h1>
          <p className="text-xl text-gray-600">
            Nous sommes là pour vous aider
          </p>
        </div>

        {/* Contact Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-xl shadow-lg p-6 text-center hover:shadow-xl transition-shadow">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Phone className="w-8 h-8 text-[#1B89C7]" />
            </div>
            <h3 className="font-bold text-gray-800 mb-2">Téléphone</h3>
            <p className="text-gray-600 text-sm mb-3">Lun - Ven, 8h - 18h</p>
            <a href="tel:+22507097591551" className="text-[#1B89C7] font-semibold hover:underline">
              +225 07-097-591-51
            </a>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 text-center hover:shadow-xl transition-shadow">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Mail className="w-8 h-8 text-[#4CAF50]" />
            </div>
            <h3 className="font-bold text-gray-800 mb-2">E-mail</h3>
            <p className="text-gray-600 text-sm mb-3">Réponse sous 24h</p>
            <a href="mailto:infos@mysmartschool.com" className="text-[#4CAF50] font-semibold hover:underline">
              infos@mysmartschool.com
            </a>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 text-center hover:shadow-xl transition-shadow">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageCircle className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="font-bold text-gray-800 mb-2">Chat en direct</h3>
            <p className="text-gray-600 text-sm mb-3">Disponible maintenant</p>
            <button className="text-purple-600 font-semibold hover:underline">
              Démarrer le chat
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Support Ticket Form */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center space-x-2">
              <FileText className="w-6 h-6 text-[#1B89C7]" />
              <span>Créer un ticket</span>
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                  Nom complet *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={ticketData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent outline-none transition-all"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  E-mail *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={ticketData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent outline-none transition-all"
                />
              </div>

              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">
                  Sujet *
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={ticketData.subject}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent outline-none transition-all"
                />
              </div>

              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                  Priorité *
                </label>
                <select
                  id="priority"
                  name="priority"
                  value={ticketData.priority}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent outline-none transition-all"
                >
                  <option value="low">Basse</option>
                  <option value="normal">Normale</option>
                  <option value="high">Haute</option>
                  <option value="urgent">Urgente</option>
                </select>
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                  Description du problème *
                </label>
                <textarea
                  id="description"
                  name="description"
                  rows="4"
                  value={ticketData.description}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B89C7] focus:border-transparent outline-none transition-all"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-[#1B89C7] text-white py-3 px-6 rounded-lg font-semibold hover:bg-[#1565A0] transition-colors shadow-md"
              >
                Soumettre le ticket
              </button>
            </form>
          </div>

          {/* FAQ Section */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Questions Fréquentes</h2>
            <div className="space-y-4">
              {faqItems.map((item, index) => (
                <div key={index} className="border-b border-gray-200 pb-4 last:border-b-0">
                  <h3 className="font-semibold text-gray-800 mb-2">{item.question}</h3>
                  <p className="text-gray-600 text-sm">{item.answer}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-2">Documentation</h4>
              <p className="text-blue-800 text-sm mb-3">
                Consultez notre documentation complète pour plus d'informations.
              </p>
              <button className="text-[#1B89C7] font-semibold hover:underline">
                Voir la documentation →
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm">© 2025 SmartScool. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
};

export default SupportPage;