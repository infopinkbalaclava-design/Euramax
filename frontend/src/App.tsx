import React, { useState, useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import ThreatsPage from './pages/ThreatsPage';
import NotificationsPage from './pages/NotificationsPage';
import { useLocalization } from './services/localizationService';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [language, setLanguage] = useState('nl');
  const { t } = useLocalization(language);

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>{t('app_name')}</h1>
          <p>{t('app_description')}</p>
          
          <div className="language-selector">
            <button 
              className={language === 'nl' ? 'active' : ''}
              onClick={() => setLanguage('nl')}
            >
              NL
            </button>
            <button 
              className={language === 'en' ? 'active' : ''}
              onClick={() => setLanguage('en')}
            >
              EN
            </button>
          </div>
        </div>
      </header>

      <nav className="main-nav">
        <button 
          className={currentPage === 'dashboard' ? 'active' : ''}
          onClick={() => setCurrentPage('dashboard')}
        >
          {t('navigation.dashboard')}
        </button>
        <button 
          className={currentPage === 'threats' ? 'active' : ''}
          onClick={() => setCurrentPage('threats')}
        >
          {t('navigation.threats')}
        </button>
        <button 
          className={currentPage === 'notifications' ? 'active' : ''}
          onClick={() => setCurrentPage('notifications')}
        >
          {t('navigation.notifications')}
        </button>
      </nav>

      <main className="main-content">
        {currentPage === 'dashboard' && <Dashboard language={language} />}
        {currentPage === 'threats' && <ThreatsPage language={language} />}
        {currentPage === 'notifications' && <NotificationsPage language={language} />}
      </main>

      <footer className="app-footer">
        <p>© 2024 Euramax AI Cybersecurity Defense System - Bescherming tegen cyberbedreigingen</p>
      </footer>
    </div>
  );
}

export default App;