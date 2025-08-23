import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Dashboard endpoints
  async getDashboardOverview() {
    const response = await axios.get(`${this.baseURL}/api/dashboard/overview`);
    return response.data;
  }

  async getSystemHealth() {
    const response = await axios.get(`${this.baseURL}/api/dashboard/health`);
    return response.data;
  }

  // Threats endpoints
  async getThreats(threatType?: string, severity?: string, limit: number = 50) {
    const params = new URLSearchParams();
    if (threatType) params.append('threat_type', threatType);
    if (severity) params.append('severity', severity);
    params.append('limit', limit.toString());

    const response = await axios.get(`${this.baseURL}/api/threats?${params.toString()}`);
    return response.data;
  }

  async scanContent(content: string, source: string) {
    const response = await axios.post(`${this.baseURL}/api/threats/scan`, {
      content,
      source
    });
    return response.data;
  }

  async getThreatDetails(threatId: string) {
    const response = await axios.get(`${this.baseURL}/api/threats/${threatId}`);
    return response.data;
  }

  async getThreatStatistics() {
    const response = await axios.get(`${this.baseURL}/api/threats/statistics`);
    return response.data;
  }

  // Notifications endpoints
  async getNotifications(unreadOnly: boolean = false, limit: number = 50) {
    const params = new URLSearchParams();
    params.append('unread_only', unreadOnly.toString());
    params.append('limit', limit.toString());

    const response = await axios.get(`${this.baseURL}/api/notifications?${params.toString()}`);
    return response.data;
  }

  async markNotificationRead(notificationId: string) {
    const response = await axios.post(`${this.baseURL}/api/notifications/${notificationId}/read`);
    return response.data;
  }

  async sendNotification(type: string, recipient: string, language: string = 'nl', data: any = {}) {
    const response = await axios.post(`${this.baseURL}/api/notifications/send`, {
      type,
      recipient,
      language,
      data
    });
    return response.data;
  }

  async getNotificationStatistics() {
    const response = await axios.get(`${this.baseURL}/api/notifications/statistics`);
    return response.data;
  }

  async testNotificationSystem() {
    const response = await axios.get(`${this.baseURL}/api/notifications/test`);
    return response.data;
  }

  // Dashboard specific endpoints
  async getThreatsTimeline(hours: number = 24) {
    const response = await axios.get(`${this.baseURL}/api/dashboard/threats/timeline?hours=${hours}`);
    return response.data;
  }

  async getThreatGeographicData() {
    const response = await axios.get(`${this.baseURL}/api/dashboard/threats/geographic`);
    return response.data;
  }

  async getAIBotActions(limit: number = 20) {
    const response = await axios.get(`${this.baseURL}/api/dashboard/ai-bot/actions?limit=${limit}`);
    return response.data;
  }

  async getBlockedDomains() {
    const response = await axios.get(`${this.baseURL}/api/dashboard/security/blocked-domains`);
    return response.data;
  }

  async getQuarantinedEmails() {
    const response = await axios.get(`${this.baseURL}/api/dashboard/security/quarantined`);
    return response.data;
  }

  async getSystemPerformance() {
    const response = await axios.get(`${this.baseURL}/api/dashboard/performance`);
    return response.data;
  }

  // System health check
  async healthCheck() {
    const response = await axios.get(`${this.baseURL}/health`);
    return response.data;
  }

  // Root endpoint
  async getSystemInfo() {
    const response = await axios.get(`${this.baseURL}/`);
    return response.data;
  }
}

export const apiService = new ApiService();