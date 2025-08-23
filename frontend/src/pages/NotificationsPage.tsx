import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';
import { useLocalization } from '../services/localizationService';

interface NotificationsPageProps {
  language: string;
}

interface Notification {
  notification_id: string;
  type: string;
  title: string;
  message: string;
  severity: string;
  recipient: string;
  channel: string;
  language: string;
  data: any;
  created_at: string;
  sent_at: string | null;
  read_at: string | null;
}

const NotificationsPage: React.FC<NotificationsPageProps> = ({ language }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');
  const { t } = useLocalization(language);

  useEffect(() => {
    loadNotifications();
  }, [filter]);

  const loadNotifications = async () => {
    try {
      setLoading(true);
      const response = await apiService.getNotifications(filter === 'unread');
      setNotifications(response);
      setError(null);
    } catch (err) {
      setError(t('messages.error_occurred'));
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (notificationId: string) => {
    try {
      await apiService.markNotificationRead(notificationId);
      // Update the notification in the local state
      setNotifications(prev => 
        prev.map(n => 
          n.notification_id === notificationId 
            ? { ...n, read_at: new Date().toISOString() }
            : n
        )
      );
    } catch (err) {
      setError(t('messages.error_occurred'));
    }
  };

  const testNotifications = async () => {
    try {
      await apiService.testNotificationSystem();
      await loadNotifications(); // Refresh notifications
    } catch (err) {
      setError(t('messages.error_occurred'));
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'phishing_alert':
        return '🚨';
      case 'threat_blocked':
        return '🛡️';
      case 'security_update':
        return '📋';
      case 'system_status':
        return '⚡';
      default:
        return '📢';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString(language === 'nl' ? 'nl-NL' : 'en-US');
  };

  const formatTimeAgo = (dateString: string) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) {
      return language === 'nl' ? 'Nu' : 'Now';
    } else if (diffInMinutes < 60) {
      return language === 'nl' ? `${diffInMinutes} min geleden` : `${diffInMinutes} min ago`;
    } else if (diffInMinutes < 1440) {
      const hours = Math.floor(diffInMinutes / 60);
      return language === 'nl' ? `${hours} uur geleden` : `${hours} hours ago`;
    } else {
      return formatDate(dateString);
    }
  };

  if (loading) {
    return <div className="loading">{language === 'nl' ? 'Laden...' : 'Loading...'}</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>{t('notifications.title')}</h2>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setFilter('all')}
            style={{
              padding: '8px 16px',
              background: filter === 'all' ? '#1e3c72' : '#f8f9fa',
              color: filter === 'all' ? 'white' : '#495057',
              border: '1px solid #dee2e6',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            {language === 'nl' ? 'Alle' : 'All'}
          </button>
          <button
            onClick={() => setFilter('unread')}
            style={{
              padding: '8px 16px',
              background: filter === 'unread' ? '#1e3c72' : '#f8f9fa',
              color: filter === 'unread' ? 'white' : '#495057',
              border: '1px solid #dee2e6',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            {t('notifications.unread')}
          </button>
          <button
            onClick={testNotifications}
            style={{
              padding: '8px 16px',
              background: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            {language === 'nl' ? 'Test Notificaties' : 'Test Notifications'}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="notifications-container">
        {notifications.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#6c757d' }}>
            {language === 'nl' ? 'Geen notificaties gevonden' : 'No notifications found'}
          </div>
        ) : (
          notifications.map((notification) => (
            <div 
              key={notification.notification_id} 
              className="notification-item"
              style={{
                background: notification.read_at ? 'white' : '#f8f9ff',
                borderLeft: notification.read_at ? '4px solid #dee2e6' : '4px solid #1e3c72'
              }}
            >
              <div className="notification-icon">
                {getNotificationIcon(notification.type)}
              </div>
              
              <div className="notification-content">
                <h4>{notification.title}</h4>
                <p>{notification.message}</p>
                
                {/* Show additional data for phishing alerts */}
                {notification.type === 'phishing_alert' && notification.data && (
                  <div style={{ 
                    marginTop: '10px', 
                    padding: '10px', 
                    background: '#ffe6e6', 
                    borderRadius: '5px',
                    fontSize: '0.9rem'
                  }}>
                    <strong>{language === 'nl' ? 'Bedreiging Details:' : 'Threat Details:'}</strong>
                    {notification.data.threat && (
                      <div style={{ marginTop: '5px' }}>
                        <div><strong>{language === 'nl' ? 'Type:' : 'Type:'}</strong> {notification.data.threat.threat_type}</div>
                        <div><strong>{language === 'nl' ? 'Ernst:' : 'Severity:'}</strong> {notification.data.threat.severity}</div>
                        <div><strong>{language === 'nl' ? 'Bron:' : 'Source:'}</strong> {notification.data.threat.source}</div>
                      </div>
                    )}
                    {notification.data.instructions && (
                      <div style={{ marginTop: '10px', fontSize: '0.8rem', background: '#fff', padding: '8px', borderRadius: '3px' }}>
                        <pre style={{ whiteSpace: 'pre-wrap', margin: 0, fontFamily: 'inherit' }}>
                          {notification.data.instructions}
                        </pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
              
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '10px' }}>
                <div className="notification-time">
                  {formatTimeAgo(notification.created_at)}
                </div>
                
                {!notification.read_at && (
                  <button
                    onClick={() => markAsRead(notification.notification_id)}
                    style={{
                      padding: '4px 8px',
                      background: '#1e3c72',
                      color: 'white',
                      border: 'none',
                      borderRadius: '3px',
                      cursor: 'pointer',
                      fontSize: '0.8rem'
                    }}
                  >
                    {t('notifications.mark_as_read')}
                  </button>
                )}
                
                <span style={{
                  fontSize: '0.8rem',
                  color: notification.severity === 'critical' ? '#dc3545' : 
                        notification.severity === 'warning' ? '#ffc107' : '#6c757d',
                  fontWeight: '600',
                  textTransform: 'uppercase'
                }}>
                  {t(`notifications.severity.${notification.severity}`)}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default NotificationsPage;