import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';
import { useLocalization } from '../services/localizationService';

interface ThreatsPageProps {
  language: string;
}

interface Threat {
  threat_id: string;
  threat_type: string;
  severity: string;
  source: string;
  content: string;
  indicators: string[];
  confidence: number;
  detected_at: string;
  status: string;
}

const ThreatsPage: React.FC<ThreatsPageProps> = ({ language }) => {
  const [threats, setThreats] = useState<Threat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [scanContent, setScanContent] = useState('');
  const [scanResult, setScanResult] = useState<Threat | null>(null);
  const { t } = useLocalization(language);

  useEffect(() => {
    loadThreats();
  }, []);

  const loadThreats = async () => {
    try {
      setLoading(true);
      const response = await apiService.getThreats();
      setThreats(response);
      setError(null);
    } catch (err) {
      setError(t('messages.error_occurred'));
    } finally {
      setLoading(false);
    }
  };

  const handleScanContent = async () => {
    if (!scanContent.trim()) return;

    try {
      const result = await apiService.scanContent(scanContent, 'manual_scan');
      setScanResult(result);
      if (result) {
        await loadThreats(); // Refresh the threats list
      }
    } catch (err) {
      setError(t('messages.error_occurred'));
    }
  };

  const getSeverityClass = (severity: string) => {
    return `severity-badge severity-${severity}`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString(language === 'nl' ? 'nl-NL' : 'en-US');
  };

  if (loading) {
    return <div className="loading">{language === 'nl' ? 'Laden...' : 'Loading...'}</div>;
  }

  return (
    <div>
      <h2>{t('threats.title')}</h2>

      {/* Content Scanner */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3>{t('threats.scan_content')}</h3>
        <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
          <textarea
            value={scanContent}
            onChange={(e) => setScanContent(e.target.value)}
            placeholder={language === 'nl' ? 'Voer verdachte inhoud in om te scannen...' : 'Enter suspicious content to scan...'}
            style={{
              flex: 1,
              padding: '10px',
              border: '1px solid #dee2e6',
              borderRadius: '5px',
              minHeight: '80px',
              resize: 'vertical'
            }}
          />
          <button
            onClick={handleScanContent}
            style={{
              padding: '10px 20px',
              background: '#1e3c72',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              height: 'fit-content'
            }}
          >
            {t('buttons.scan')}
          </button>
        </div>

        {scanResult && (
          <div style={{ marginTop: '15px', padding: '15px', background: '#f8d7da', borderRadius: '5px' }}>
            <h4>🚨 {language === 'nl' ? 'Bedreiging Gedetecteerd!' : 'Threat Detected!'}</h4>
            <p><strong>{language === 'nl' ? 'Type' : 'Type'}:</strong> {scanResult.threat_type}</p>
            <p><strong>{language === 'nl' ? 'Ernst' : 'Severity'}:</strong> 
              <span className={getSeverityClass(scanResult.severity)} style={{ marginLeft: '10px' }}>
                {t(`threats.severity.${scanResult.severity}`)}
              </span>
            </p>
            <p><strong>{language === 'nl' ? 'Vertrouwen' : 'Confidence'}:</strong> {Math.round(scanResult.confidence * 100)}%</p>
          </div>
        )}

        {scanContent && !scanResult && (
          <div style={{ marginTop: '15px', padding: '15px', background: '#d1edff', borderRadius: '5px' }}>
            <p>✅ {t('messages.no_threats_found')}</p>
          </div>
        )}
      </div>

      {error && <div className="error">{error}</div>}

      <div className="threats-container">
        <div className="threats-header">
          <h3>{language === 'nl' ? 'Recente Bedreigingen' : 'Recent Threats'}</h3>
          <button onClick={loadThreats} style={{
            background: '#1e3c72',
            color: 'white',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '5px',
            cursor: 'pointer'
          }}>
            {t('buttons.refresh')}
          </button>
        </div>

        <div className="threats-list">
          {threats.length === 0 ? (
            <div style={{ padding: '40px', textAlign: 'center', color: '#6c757d' }}>
              {t('messages.no_threats_found')}
            </div>
          ) : (
            threats.map((threat) => (
              <div key={threat.threat_id} className="threat-item">
                <div className="threat-info">
                  <h4>
                    {threat.threat_type === 'phishing' && '🎣'}
                    {threat.threat_type === 'malware' && '🦠'}
                    {threat.threat_type === 'social_engineering' && '🎭'}
                    {' '}{t(`threats.${threat.threat_type}`)}
                  </h4>
                  <p><strong>{language === 'nl' ? 'Bron' : 'Source'}:</strong> {threat.source}</p>
                  <p><strong>{language === 'nl' ? 'Gedetecteerd' : 'Detected'}:</strong> {formatDate(threat.detected_at)}</p>
                  <p><strong>{language === 'nl' ? 'Vertrouwen' : 'Confidence'}:</strong> {Math.round(threat.confidence * 100)}%</p>
                  {threat.indicators.length > 0 && (
                    <p><strong>{language === 'nl' ? 'Indicatoren' : 'Indicators'}:</strong> {threat.indicators.join(', ')}</p>
                  )}
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '10px' }}>
                  <span className={getSeverityClass(threat.severity)}>
                    {t(`threats.severity.${threat.severity}`)}
                  </span>
                  <span style={{ 
                    color: threat.status === 'blocked' ? '#28a745' : '#6c757d',
                    fontSize: '0.9rem',
                    fontWeight: '600'
                  }}>
                    {t(`threats.status.${threat.status}`)}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ThreatsPage;