"""
API endpoints for threat management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.core.threat_detector import ThreatDetector
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Initialize threat detector
threat_detector = ThreatDetector()

class ThreatResponse(BaseModel):
    threat_id: str
    threat_type: str
    severity: str
    source: str
    content: str
    indicators: List[str]
    confidence: float
    detected_at: datetime
    status: str = "detected"

class ThreatScanRequest(BaseModel):
    content: str
    source: str

@router.get("/", response_model=List[ThreatResponse])
async def get_threats(
    threat_type: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get list of detected threats with optional filtering"""
    # In production, this would query the database
    # For now, return sample data
    
    sample_threats = [
        ThreatResponse(
            threat_id="threat_1703123456.789",
            threat_type="phishing",
            severity="critical",
            source="email:suspicious@fake-bank.com",
            content="URGENT: Your bank account has been compromised. Click here to secure it immediately.",
            indicators=["urgent.*action.*required", "click.*here.*immediately"],
            confidence=0.95,
            detected_at=datetime.now(),
            status="blocked"
        ),
        ThreatResponse(
            threat_id="threat_1703123457.123",
            threat_type="phishing", 
            severity="high",
            source="email:winner@fake-lottery.org",
            content="Congratulations! You have won €10,000 in our lottery. Click to claim your prize now!",
            indicators=["claim.*prize", "congratulations.*won"],
            confidence=0.88,
            detected_at=datetime.now(),
            status="blocked"
        )
    ]
    
    # Apply filters
    if threat_type:
        sample_threats = [t for t in sample_threats if t.threat_type == threat_type]
    if severity:
        sample_threats = [t for t in sample_threats if t.severity == severity]
    
    return sample_threats[:limit]

@router.post("/scan", response_model=Optional[ThreatResponse])
async def scan_content(
    request: ThreatScanRequest,
    db: Session = Depends(get_db)
):
    """Scan specific content for threats"""
    threat = await threat_detector.analyze_content(request.content, request.source)
    
    if threat:
        return ThreatResponse(
            threat_id=threat.threat_id,
            threat_type=threat.threat_type,
            severity=threat.severity,
            source=threat.source,
            content=threat.content,
            indicators=threat.indicators,
            confidence=threat.confidence,
            detected_at=threat.detected_at
        )
    
    return None

@router.get("/statistics")
async def get_threat_statistics(db: Session = Depends(get_db)):
    """Get threat detection statistics"""
    return await threat_detector.get_threat_statistics()

@router.get("/{threat_id}")
async def get_threat_details(threat_id: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific threat"""
    # In production, this would query the database
    if threat_id.startswith("threat_"):
        return {
            "threat_id": threat_id,
            "threat_type": "phishing",
            "severity": "critical",
            "source": "email:suspicious@fake-bank.com",
            "content": "URGENT: Your bank account has been compromised...",
            "indicators": ["urgent.*action.*required", "click.*here.*immediately"],
            "confidence": 0.95,
            "detected_at": datetime.now().isoformat(),
            "status": "blocked",
            "ai_actions": [
                "Blocked source email address",
                "Quarantined email",
                "Notified security team"
            ]
        }
    
    raise HTTPException(status_code=404, detail="Threat not found")