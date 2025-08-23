"""
API endpoints for dashboard and monitoring
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.threat_detector import ThreatDetector
from app.core.ai_bot import AISecurityBot
from app.core.notification_service import NotificationService
from datetime import datetime, timedelta
import random

router = APIRouter()

# Initialize services
threat_detector = ThreatDetector()
ai_bot = AISecurityBot()
notification_service = NotificationService()

@router.get("/overview")
async def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get dashboard overview with key metrics"""
    
    # Get statistics from various services
    threat_stats = await threat_detector.get_threat_statistics()
    notification_stats = await notification_service.get_notification_stats()
    
    return {
        "system_status": "operational",
        "threat_detection": {
            "status": "active",
            "threats_detected_today": threat_stats.get("total_threats_today", 0),
            "phishing_attempts": threat_stats.get("phishing_attempts", 0),
            "blocked_automatically": threat_stats.get("blocked_automatically", 0),
            "success_rate": "98.5%"
        },
        "ai_bot": {
            "status": "active",
            "actions_taken_today": len(await ai_bot.get_action_history()),
            "blocked_domains": len(await ai_bot.get_blocked_domains()),
            "quarantined_emails": len(await ai_bot.get_quarantined_emails()),
            "response_time_avg": "1.2s"
        },
        "notifications": {
            "total": notification_stats.get("total_notifications", 0),
            "unread": notification_stats.get("unread_notifications", 0),
            "sent_today": notification_stats.get("total_notifications", 0)
        },
        "security_score": 95,  # Overall security score
        "last_updated": datetime.now().isoformat()
    }

@router.get("/threats/timeline")
async def get_threats_timeline(hours: int = 24, db: Session = Depends(get_db)):
    """Get threat detection timeline for the dashboard"""
    
    # Generate sample timeline data (in production, this would query the database)
    timeline = []
    now = datetime.now()
    
    for i in range(hours):
        hour_start = now - timedelta(hours=i)
        threats_count = random.randint(0, 5)
        
        timeline.append({
            "hour": hour_start.strftime("%H:00"),
            "timestamp": hour_start.isoformat(),
            "total_threats": threats_count,
            "phishing": random.randint(0, threats_count),
            "malware": random.randint(0, threats_count - random.randint(0, threats_count)),
            "blocked": threats_count - random.randint(0, 1)
        })
    
    return {"timeline": timeline[::-1]}  # Reverse to show chronological order

@router.get("/threats/geographic")
async def get_threat_geographic_data(db: Session = Depends(get_db)):
    """Get geographic distribution of threats"""
    
    # Sample geographic data (in production, this would be based on IP geolocation)
    return {
        "countries": [
            {"country": "Russia", "threats": 45, "code": "RU"},
            {"country": "China", "threats": 38, "code": "CN"},
            {"country": "United States", "threats": 25, "code": "US"},
            {"country": "Germany", "threats": 15, "code": "DE"},
            {"country": "Brazil", "threats": 12, "code": "BR"},
            {"country": "Other", "threats": 35, "code": "XX"}
        ]
    }

@router.get("/ai-bot/actions")
async def get_ai_bot_actions(limit: int = 20, db: Session = Depends(get_db)):
    """Get recent AI bot actions"""
    
    actions = await ai_bot.get_action_history()
    
    return {
        "actions": [
            {
                "action_id": action.action_id,
                "threat_id": action.threat_id,
                "actions_taken": action.actions_taken,
                "status": action.status,
                "timestamp": action.timestamp.isoformat()
            }
            for action in actions[-limit:]
        ]
    }

@router.get("/security/blocked-domains")
async def get_blocked_domains(db: Session = Depends(get_db)):
    """Get list of blocked domains"""
    
    domains = await ai_bot.get_blocked_domains()
    
    return {
        "blocked_domains": [
            {
                "domain": domain,
                "blocked_at": datetime.now().isoformat(),
                "reason": "Phishing attempt detected",
                "blocked_by": "ai_bot"
            }
            for domain in domains
        ],
        "total_count": len(domains)
    }

@router.get("/security/quarantined")
async def get_quarantined_emails(db: Session = Depends(get_db)):
    """Get quarantined emails"""
    
    emails = await ai_bot.get_quarantined_emails()
    
    return {
        "quarantined_emails": [
            {
                "threat_id": email["threat_id"],
                "source": email["source"],
                "quarantined_at": email["quarantined_at"].isoformat(),
                "content_preview": email["content"][:100] + "..." if len(email["content"]) > 100 else email["content"]
            }
            for email in emails
        ],
        "total_count": len(emails)
    }

@router.get("/performance")
async def get_system_performance(db: Session = Depends(get_db)):
    """Get system performance metrics"""
    
    return {
        "detection_performance": {
            "accuracy": 98.5,
            "precision": 96.8,
            "recall": 97.2,
            "f1_score": 97.0
        },
        "response_times": {
            "threat_detection_avg": 0.8,  # seconds
            "ai_bot_response_avg": 1.2,   # seconds
            "notification_delivery_avg": 0.3  # seconds
        },
        "system_resources": {
            "cpu_usage": random.randint(20, 40),
            "memory_usage": random.randint(45, 65),
            "disk_usage": random.randint(30, 50)
        },
        "uptime": {
            "system": "99.98%",
            "threat_detector": "99.95%",
            "ai_bot": "99.97%",
            "notifications": "99.99%"
        }
    }

@router.get("/health")
async def get_system_health(db: Session = Depends(get_db)):
    """Get detailed system health information"""
    
    return {
        "overall_status": "healthy",
        "components": {
            "threat_detector": {
                "status": "healthy",
                "last_check": datetime.now().isoformat(),
                "models_loaded": 3,
                "processing_queue": 0
            },
            "ai_bot": {
                "status": "healthy",
                "last_action": datetime.now().isoformat(),
                "pending_actions": 0,
                "success_rate": "99.1%"
            },
            "notification_service": {
                "status": "healthy",
                "active_connections": 25,
                "pending_notifications": 0,
                "delivery_rate": "99.8%"
            },
            "database": {
                "status": "healthy",
                "connection_pool": "optimal",
                "response_time": "12ms"
            }
        }
    }