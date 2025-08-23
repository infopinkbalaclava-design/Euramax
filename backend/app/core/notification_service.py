"""
Real-time notification service for security alerts
Supports push notifications, email, and WebSocket communication
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class NotificationType(Enum):
    PHISHING_ALERT = "phishing_alert"
    THREAT_BLOCKED = "threat_blocked"
    SECURITY_UPDATE = "security_update"
    SYSTEM_STATUS = "system_status"

@dataclass
class Notification:
    notification_id: str
    type: NotificationType
    title: str
    message: str
    severity: str
    recipient: str
    channel: str  # websocket, email, sms
    language: str  # nl, en
    data: Dict
    created_at: datetime
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    
    def dict(self):
        return {
            'notification_id': self.notification_id,
            'type': self.type.value,
            'title': self.title,
            'message': self.message,
            'severity': self.severity,
            'recipient': self.recipient,
            'channel': self.channel,
            'language': self.language,
            'data': self.data,
            'created_at': self.created_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

class NotificationService:
    def __init__(self):
        self.notifications = []
        self.subscribers = {}  # WebSocket connections by user
        self.notification_templates = self._load_notification_templates()
    
    def _load_notification_templates(self) -> Dict:
        """Load notification templates in multiple languages"""
        return {
            "phishing_alert": {
                "nl": {
                    "title": "🚨 Phishing Aanval Gedetecteerd",
                    "message": "Een verdachte phishing-poging is gedetecteerd en automatisch geblokkeerd. Bekijk details voor meer informatie."
                },
                "en": {
                    "title": "🚨 Phishing Attack Detected", 
                    "message": "A suspicious phishing attempt has been detected and automatically blocked. View details for more information."
                }
            },
            "threat_blocked": {
                "nl": {
                    "title": "🛡️ Bedreiging Geblokkeerd",
                    "message": "Een cyberbedreiging is succesvol geblokkeerd door ons AI-systeem."
                },
                "en": {
                    "title": "🛡️ Threat Blocked",
                    "message": "A cyber threat has been successfully blocked by our AI system."
                }
            },
            "security_update": {
                "nl": {
                    "title": "📋 Beveiligingsupdate",
                    "message": "Nieuwe beveiligingsmaatregelen zijn geïmplementeerd."
                },
                "en": {
                    "title": "📋 Security Update",
                    "message": "New security measures have been implemented."
                }
            },
            "system_status": {
                "nl": {
                    "title": "⚡ Systeemstatus",
                    "message": "Systeemstatus update beschikbaar."
                },
                "en": {
                    "title": "⚡ System Status",
                    "message": "System status update available."
                }
            }
        }
    
    async def send_phishing_alert(self, threat_data: Dict, ai_response: Dict, language: str = "nl") -> Notification:
        """Send immediate phishing alert notification"""
        
        template = self.notification_templates["phishing_alert"][language]
        
        notification = Notification(
            notification_id=f"notif_{datetime.now().timestamp()}",
            type=NotificationType.PHISHING_ALERT,
            title=template["title"],
            message=template["message"],
            severity="critical",
            recipient="all_users",
            channel="websocket",
            language=language,
            data={
                "threat": threat_data,
                "ai_response": ai_response,
                "instructions": ai_response.get("user_instructions", {}).get(language, "")
            },
            created_at=datetime.now()
        )
        
        await self._deliver_notification(notification)
        return notification
    
    async def send_threat_blocked_notification(self, threat_data: Dict, language: str = "nl") -> Notification:
        """Send notification when threat is successfully blocked"""
        
        template = self.notification_templates["threat_blocked"][language]
        
        notification = Notification(
            notification_id=f"notif_{datetime.now().timestamp()}",
            type=NotificationType.THREAT_BLOCKED,
            title=template["title"],
            message=template["message"],
            severity="info",
            recipient="security_team",
            channel="websocket",
            language=language,
            data={"threat": threat_data},
            created_at=datetime.now()
        )
        
        await self._deliver_notification(notification)
        return notification
    
    async def send_security_update(self, update_data: Dict, language: str = "nl") -> Notification:
        """Send security update notification"""
        
        template = self.notification_templates["security_update"][language]
        
        notification = Notification(
            notification_id=f"notif_{datetime.now().timestamp()}",
            type=NotificationType.SECURITY_UPDATE,
            title=template["title"],
            message=update_data.get("message", template["message"]),
            severity="medium",
            recipient="all_users",
            channel="websocket",
            language=language,
            data=update_data,
            created_at=datetime.now()
        )
        
        await self._deliver_notification(notification)
        return notification
    
    async def _deliver_notification(self, notification: Notification):
        """Deliver notification through appropriate channel"""
        
        if notification.channel == "websocket":
            await self._send_websocket_notification(notification)
        elif notification.channel == "email":
            await self._send_email_notification(notification)
        elif notification.channel == "sms":
            await self._send_sms_notification(notification)
        
        notification.sent_at = datetime.now()
        self.notifications.append(notification)
    
    async def _send_websocket_notification(self, notification: Notification):
        """Send notification via WebSocket (real-time)"""
        # This would integrate with the WebSocket manager in main.py
        message = json.dumps(notification.dict())
        
        # In production, this would send to specific user connections
        print(f"WebSocket notification: {notification.title}")
        print(f"Message: {notification.message}")
    
    async def _send_email_notification(self, notification: Notification):
        """Send notification via email"""
        # In production, this would integrate with email service (SendGrid, AWS SES, etc.)
        print(f"Email notification to {notification.recipient}: {notification.title}")
    
    async def _send_sms_notification(self, notification: Notification):
        """Send notification via SMS"""
        # In production, this would integrate with SMS service (Twilio, etc.)
        print(f"SMS notification to {notification.recipient}: {notification.title}")
    
    async def get_notifications(self, recipient: str = "all", limit: int = 50) -> List[Notification]:
        """Get notifications for a specific recipient"""
        filtered_notifications = [
            n for n in self.notifications 
            if recipient == "all" or n.recipient == recipient or n.recipient == "all_users"
        ]
        
        # Return most recent first
        return sorted(filtered_notifications, key=lambda x: x.created_at, reverse=True)[:limit]
    
    async def mark_as_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        for notification in self.notifications:
            if notification.notification_id == notification_id:
                notification.read_at = datetime.now()
                return True
        return False
    
    async def get_notification_stats(self) -> Dict:
        """Get notification statistics"""
        total = len(self.notifications)
        unread = sum(1 for n in self.notifications if n.read_at is None)
        by_type = {}
        
        for notification in self.notifications:
            notif_type = notification.type.value
            by_type[notif_type] = by_type.get(notif_type, 0) + 1
        
        return {
            "total_notifications": total,
            "unread_notifications": unread,
            "read_notifications": total - unread,
            "notifications_by_type": by_type,
            "last_notification": self.notifications[-1].created_at.isoformat() if self.notifications else None
        }
    
    def subscribe_websocket(self, user_id: str, websocket):
        """Subscribe user to WebSocket notifications"""
        self.subscribers[user_id] = websocket
    
    def unsubscribe_websocket(self, user_id: str):
        """Unsubscribe user from WebSocket notifications"""
        if user_id in self.subscribers:
            del self.subscribers[user_id]