# Euramax API Reference

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API is open for development. Production deployment will include proper authentication.

## Endpoints

### System Information

#### GET /
Get basic system information
```json
{
  "message": "Welkom bij Euramax AI Cybersecurity Defense System",
  "description": "AI-gestuurde phishing bescherming en cybersecurity verdediging",
  "version": "1.0.0",
  "endpoints": {
    "api_docs": "/api/docs",
    "dashboard": "/dashboard",
    "websocket": "/ws"
  }
}
```

#### GET /health
Get system health status
```json
{
  "status": "healthy",
  "services": {
    "threat_detector": "active",
    "ai_bot": "active",
    "notification_service": "active"
  }
}
```

### Dashboard

#### GET /api/dashboard/overview
Get dashboard overview with key metrics
```json
{
  "system_status": "operational",
  "threat_detection": {
    "status": "active",
    "threats_detected_today": 15,
    "phishing_attempts": 12,
    "blocked_automatically": 14,
    "success_rate": "98.5%"
  },
  "ai_bot": {
    "status": "active",
    "actions_taken_today": 14,
    "blocked_domains": 5,
    "quarantined_emails": 8,
    "response_time_avg": "1.2s"
  },
  "notifications": {
    "total": 25,
    "unread": 3,
    "sent_today": 15
  },
  "security_score": 95,
  "last_updated": "2024-01-01T12:00:00Z"
}
```

### Threats

#### GET /api/threats
Get list of detected threats

**Query Parameters:**
- `threat_type` (optional): Filter by threat type (phishing, malware, etc.)
- `severity` (optional): Filter by severity (low, medium, high, critical)
- `limit` (optional): Number of results (default: 50)

```json
[
  {
    "threat_id": "threat_1703123456.789",
    "threat_type": "phishing",
    "severity": "critical",
    "source": "email:suspicious@fake-bank.com",
    "content": "URGENT: Your bank account has been compromised...",
    "indicators": ["urgent.*action.*required", "click.*here.*immediately"],
    "confidence": 0.95,
    "detected_at": "2024-01-01T12:00:00Z",
    "status": "blocked"
  }
]
```

#### POST /api/threats/scan
Scan content for threats

**Request Body:**
```json
{
  "content": "URGENT: Click here to verify your account",
  "source": "manual_scan"
}
```

**Response:**
```json
{
  "threat_id": "threat_1703123456.789",
  "threat_type": "phishing",
  "severity": "critical",
  "source": "manual_scan",
  "content": "URGENT: Click here to verify your account",
  "indicators": ["urgent.*action.*required"],
  "confidence": 0.95,
  "detected_at": "2024-01-01T12:00:00Z"
}
```

#### GET /api/threats/statistics
Get threat detection statistics
```json
{
  "total_threats_today": 15,
  "phishing_attempts": 12,
  "malware_detected": 2,
  "blocked_automatically": 14,
  "manual_review_needed": 1
}
```

### Notifications

#### GET /api/notifications
Get notifications

**Query Parameters:**
- `recipient` (optional): Filter by recipient (default: "all")
- `unread_only` (optional): Show only unread notifications (default: false)
- `limit` (optional): Number of results (default: 50)

```json
[
  {
    "notification_id": "notif_1703123456.789",
    "type": "phishing_alert",
    "title": "🚨 Phishing Aanval Gedetecteerd",
    "message": "Een verdachte phishing-poging is gedetecteerd en automatisch geblokkeerd.",
    "severity": "critical",
    "recipient": "all_users",
    "channel": "websocket",
    "language": "nl",
    "data": {
      "threat": {...},
      "ai_response": {...},
      "instructions": "..."
    },
    "created_at": "2024-01-01T12:00:00Z",
    "sent_at": "2024-01-01T12:00:01Z",
    "read_at": null
  }
]
```

#### POST /api/notifications/send
Send a custom notification

**Request Body:**
```json
{
  "type": "phishing_alert",
  "recipient": "all_users",
  "language": "nl",
  "data": {
    "threat": {...},
    "ai_response": {...}
  }
}
```

#### POST /api/notifications/{notification_id}/read
Mark notification as read

```json
{
  "status": "marked_as_read"
}
```

#### GET /api/notifications/test
Test the notification system (development only)

```json
{
  "status": "test_completed",
  "notifications_sent": [
    "notif_1703123456.789",
    "notif_1703123456.790"
  ]
}
```

### WebSocket

#### WS /ws
Real-time notifications and updates

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

**Message Format:**
```json
{
  "type": "phishing_detected",
  "threat": {...},
  "ai_response": {...},
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Responses

All endpoints return errors in the following format:

```json
{
  "detail": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Rate Limiting

Currently no rate limiting is implemented for development. Production deployment will include appropriate rate limits.

## Dutch Language Support

All API responses support Dutch localization through the `language` parameter:
- `nl`: Nederlands (default)
- `en`: English

Example:
```
GET /api/notifications?language=nl
```