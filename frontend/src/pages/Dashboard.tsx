import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';
import { useLocalization } from '../services/localizationService';

interface DashboardProps {
  language: string;
}

interface DashboardData {
  system_status: string;
  threat_detection: any;
  ai_bot: any;
  notifications: any;
  security_score: number;
  last_updated: string;
}

const Dashboard: React.FC<DashboardProps> = ({ language }) => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { t } = useLocalization(language);

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getDashboardOverview();
      setData(response);
      setError(null);
    } catch (err) {
      setError(t('messages.error_occurred'));
    } finally {
      setLoading(false);
    }
  };

  if (loading && !data) {
    return <div className="loading">{language === 'nl' ? 'Laden...' : 'Loading...'}</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!data) {
    return <div className="error">{t('messages.error_occurred')}</div>;
  }

  return (
    <div className="dashboard">
      <h2>{t('dashboard.title')}</h2>
      
      <div className="overview-cards">
        <div className="card">
          <h3>{t('dashboard.security_score')}</h3>
          <div className="value">{data.security_score}%</div>
          <div className="label">{t('dashboard.system_status')}: {data.system_status}</div>
        </div>

        <div className="card critical">
          <h3>{t('dashboard.threats_detected_today')}</h3>
          <div className="value">{data.threat_detection?.threats_detected_today || 0}</div>
          <div className="label">{t('dashboard.phishing_attempts')}: {data.threat_detection?.phishing_attempts || 0}</div>
        </div>

        <div className="card success">
          <h3>{t('dashboard.blocked_automatically')}</h3>
          <div className="value">{data.threat_detection?.blocked_automatically || 0}</div>
          <div className="label">{t('dashboard.success_rate')}: {data.threat_detection?.success_rate || '0%'}</div>
        </div>

        <div className="card">
          <h3>{t('ai_bot.actions_taken')}</h3>
          <div className="value">{data.ai_bot?.actions_taken_today || 0}</div>
          <div className="label">{t('ai_bot.response_time')}: {data.ai_bot?.response_time_avg || '0s'}</div>
        </div>

        <div className="card warning">
          <h3>{t('ai_bot.blocked_domains')}</h3>
          <div className="value">{data.ai_bot?.blocked_domains || 0}</div>
          <div className="label">{t('ai_bot.quarantined_emails')}: {data.ai_bot?.quarantined_emails || 0}</div>
        </div>

        <div className="card">
          <h3>{t('notifications.title')}</h3>
          <div className="value">{data.notifications?.unread || 0}</div>
          <div className="label">{language === 'nl' ? 'Ongelezen' : 'Unread'}</div>
        </div>
      </div>

      <div className="card">
        <h3>{t('dashboard.ai_bot')} {language === 'nl' ? 'Status' : 'Status'}</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '15px' }}>
          <div>
            <strong>{language === 'nl' ? 'Threat Detector' : 'Threat Detector'}</strong>
            <br />
            <span style={{ color: '#28a745' }}>✅ {language === 'nl' ? 'Actief' : 'Active'}</span>
          </div>
          <div>
            <strong>{language === 'nl' ? 'AI Bot' : 'AI Bot'}</strong>
            <br />
            <span style={{ color: '#28a745' }}>✅ {language === 'nl' ? 'Actief' : 'Active'}</span>
          </div>
          <div>
            <strong>{language === 'nl' ? 'Notificaties' : 'Notifications'}</strong>
            <br />
            <span style={{ color: '#28a745' }}>✅ {language === 'nl' ? 'Actief' : 'Active'}</span>
          </div>
          <div>
            <strong>{language === 'nl' ? 'Database' : 'Database'}</strong>
            <br />
            <span style={{ color: '#28a745' }}>✅ {language === 'nl' ? 'Gezond' : 'Healthy'}</span>
          </div>
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '20px', color: '#6c757d' }}>
        {language === 'nl' ? 'Laatst bijgewerkt' : 'Last updated'}: {new Date(data.last_updated).toLocaleString(language === 'nl' ? 'nl-NL' : 'en-US')}
      </div>
    </div>
  );
};

export default Dashboard;