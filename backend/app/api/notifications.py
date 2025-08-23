"""
API endpoints for notification management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.core.notification_service import NotificationService, Notification
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Initialize notification service
notification_service = NotificationService()

class NotificationResponse(BaseModel):
    notification_id: str
    type: str
    title: str
    message: str
    severity: str
    recipient: str
    channel: str
    language: str
    data: dict
    created_at: datetime
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None

class SendNotificationRequest(BaseModel):
    type: str
    recipient: str
    language: str = "nl"
    data: dict = {}

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    recipient: str = "all",
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get notifications for a user or all users"""
    notifications = await notification_service.get_notifications(recipient, limit)
    
    if unread_only:
        notifications = [n for n in notifications if n.read_at is None]
    
    return [
        NotificationResponse(
            notification_id=n.notification_id,
            type=n.type.value,
            title=n.title,
            message=n.message,
            severity=n.severity,
            recipient=n.recipient,
            channel=n.channel,
            language=n.language,
            data=n.data,
            created_at=n.created_at,
            sent_at=n.sent_at,
            read_at=n.read_at
        )
        for n in notifications
    ]

@router.post("/send")
async def send_notification(
    request: SendNotificationRequest,
    db: Session = Depends(get_db)
):
    """Send a custom notification"""
    if request.type == "phishing_alert":
        notification = await notification_service.send_phishing_alert(
            threat_data=request.data.get("threat", {}),
            ai_response=request.data.get("ai_response", {}),
            language=request.language
        )
    elif request.type == "threat_blocked":
        notification = await notification_service.send_threat_blocked_notification(
            threat_data=request.data.get("threat", {}),
            language=request.language
        )
    elif request.type == "security_update":
        notification = await notification_service.send_security_update(
            update_data=request.data,
            language=request.language
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid notification type")
    
    return {"status": "sent", "notification_id": notification.notification_id}

@router.post("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    success = await notification_service.mark_as_read(notification_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"status": "marked_as_read"}

@router.get("/statistics")
async def get_notification_statistics(db: Session = Depends(get_db)):
    """Get notification statistics"""
    return await notification_service.get_notification_stats()

@router.get("/test")
async def test_notification_system():
    """Test the notification system with sample alerts"""
    # Create test phishing alert
    test_threat = {
        "threat_id": "test_threat_123",
        "threat_type": "phishing",
        "severity": "critical",
        "source": "email:test@example.com",
        "content": "Test phishing email content"
    }
    
    test_ai_response = {
        "action_id": "test_action_123",
        "actions_taken": ["Blocked sender", "Quarantined email"],
        "user_instructions": {
            "nl": "Test Nederlandse instructies",
            "en": "Test English instructions"
        }
    }
    
    # Send notifications in both languages
    nl_notification = await notification_service.send_phishing_alert(
        test_threat, test_ai_response, "nl"
    )
    en_notification = await notification_service.send_phishing_alert(
        test_threat, test_ai_response, "en"
    )
    
    return {
        "status": "test_completed",
        "notifications_sent": [
            nl_notification.notification_id,
            en_notification.notification_id
        ]
    }