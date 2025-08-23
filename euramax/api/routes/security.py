"""
Euramax Security API Endpoints
Nederlandse cybersecurity API voor bedreigingsdetectie en -respons
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request, UploadFile, File
from pydantic import BaseModel, EmailStr, field_validator
from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime

from euramax.ai.threat_detector import ThreatDetectionEngine


logger = structlog.get_logger()
router = APIRouter()


class EmailAnalysisRequest(BaseModel):
    """Request model voor email analyse"""
    email_content: str
    sender: EmailStr
    subject: str
    recipients: Optional[List[EmailStr]] = []
    
    @field_validator('email_content')
    @classmethod
    def validate_content(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Email content mag niet leeg zijn')
        if len(v) > 1000000:  # 1MB limit
            raise ValueError('Email content te groot (max 1MB)')
        return v


class FileAnalysisRequest(BaseModel):
    """Request model voor bestand analyse"""
    filename: str
    file_hash: Optional[str] = None
    file_size: Optional[int] = None


class NetworkAnalysisRequest(BaseModel):
    """Request model voor netwerk analyse"""
    source_ip: str
    destination_ip: str
    protocol: str
    payload_sample: Optional[str] = None


class ThreatResponse(BaseModel):
    """Response model voor bedreigingsdetectie"""
    threat_detected: bool
    threat_type: str
    severity: str
    confidence: float
    dutch_description: str
    indicators: List[str]
    recommended_actions: List[str]
    timestamp: datetime
    analysis_id: str


@router.post("/analyze/email", response_model=ThreatResponse)
async def analyze_email(
    request: EmailAnalysisRequest,
    background_tasks: BackgroundTasks,
    app_request: Request
):
    """
    Analyseer email op phishing en andere bedreigingen
    
    Nederlandse cybersecurity analyse met AI-detectie
    """
    try:
        # Verkrijg threat detection engine
        threat_engine: ThreatDetectionEngine = app_request.app.state.threat_engine
        
        # Voer analyse uit
        result = await threat_engine.analyze_email(
            email_content=request.email_content,
            sender=str(request.sender),
            subject=request.subject
        )
        
        # Als bedreiging gedetecteerd, verstuur notificaties op achtergrond
        if result.confidence > 0.5:
            background_tasks.add_task(
                _send_threat_notification,
                app_request.app.state.notification_service,
                result
            )
            
            logger.warning(
                "Email bedreiging gedetecteerd via API",
                sender=str(request.sender),
                threat_type=result.threat_type.value,
                confidence=result.confidence
            )
        
        return ThreatResponse(
            threat_detected=result.confidence > 0.5,
            threat_type=result.threat_type.value,
            severity=result.severity.value,
            confidence=result.confidence,
            dutch_description=result.dutch_description,
            indicators=result.indicators,
            recommended_actions=result.recommended_actions,
            timestamp=result.timestamp,
            analysis_id=f"email_{id(result)}"
        )
        
    except Exception as e:
        logger.error("Email analyse gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Email analyse kon niet worden voltooid"
        )


@router.post("/analyze/file", response_model=ThreatResponse)
async def analyze_file(
    file: UploadFile = File(...),
    app_request: Request = None,
    background_tasks: BackgroundTasks = None
):
    """
    Analyseer geüpload bestand op malware
    
    Ondersteunt alle bestandstypen met AI-detectie
    """
    try:
        # Lees bestand content
        file_content = await file.read()
        
        # Controleer bestand grootte (max 25MB zoals in config)
        if len(file_content) > 25 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Bestand te groot (maximaal 25MB)"
            )
        
        # Verkrijg threat detection engine
        threat_engine: ThreatDetectionEngine = app_request.app.state.threat_engine
        
        # Voer malware analyse uit
        result = await threat_engine.analyze_file(
            file_content=file_content,
            filename=file.filename
        )
        
        # Verstuur notificaties als malware gedetecteerd
        if result.confidence > 0.5:
            background_tasks.add_task(
                _send_threat_notification,
                app_request.app.state.notification_service,
                result
            )
            
            logger.warning(
                "Malware gedetecteerd in bestand via API",
                filename=file.filename,
                threat_type=result.threat_type.value,
                confidence=result.confidence
            )
        
        return ThreatResponse(
            threat_detected=result.confidence > 0.5,
            threat_type=result.threat_type.value,
            severity=result.severity.value,
            confidence=result.confidence,
            dutch_description=result.dutch_description,
            indicators=result.indicators,
            recommended_actions=result.recommended_actions,
            timestamp=result.timestamp,
            analysis_id=f"file_{id(result)}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Bestand analyse gefaald", filename=file.filename, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Bestand analyse kon niet worden voltooid"
        )


@router.post("/analyze/network", response_model=ThreatResponse)
async def analyze_network_activity(
    request: NetworkAnalysisRequest,
    background_tasks: BackgroundTasks,
    app_request: Request
):
    """
    Analyseer netwerkactiviteit op verdachte patronen
    
    DDoS, APT en andere netwerkbedreigingen detectie
    """
    try:
        # Verkrijg threat detection engine
        threat_engine: ThreatDetectionEngine = app_request.app.state.threat_engine
        
        # Converteer payload sample naar bytes
        payload = b""
        if request.payload_sample:
            payload = request.payload_sample.encode('utf-8', errors='ignore')
        
        # Voer netwerkanalyse uit
        result = await threat_engine.analyze_network_activity(
            source_ip=request.source_ip,
            destination_ip=request.destination_ip,
            payload=payload
        )
        
        # Verstuur notificaties voor verdachte activiteit
        if result.confidence > 0.6:
            background_tasks.add_task(
                _send_threat_notification,
                app_request.app.state.notification_service,
                result
            )
            
            logger.warning(
                "Verdachte netwerkactiviteit gedetecteerd",
                source_ip=request.source_ip,
                destination_ip=request.destination_ip,
                threat_type=result.threat_type.value
            )
        
        return ThreatResponse(
            threat_detected=result.confidence > 0.6,
            threat_type=result.threat_type.value,
            severity=result.severity.value,
            confidence=result.confidence,
            dutch_description=result.dutch_description,
            indicators=result.indicators,
            recommended_actions=result.recommended_actions,
            timestamp=result.timestamp,
            analysis_id=f"network_{id(result)}"
        )
        
    except Exception as e:
        logger.error("Netwerk analyse gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Netwerk analyse kon niet worden voltooid"
        )


@router.get("/threats/statistics")
async def get_threat_statistics(app_request: Request) -> Dict[str, Any]:
    """
    Verkrijg cybersecurity statistieken
    
    Nederlandse statistieken van gedetecteerde bedreigingen
    """
    try:
        threat_engine: ThreatDetectionEngine = app_request.app.state.threat_engine
        stats = await threat_engine.get_statistics()
        
        return {
            "statistieken": stats,
            "systeem_informatie": {
                "naam": "Euramax Cybersecurity Systeem",
                "versie": "1.0.0",
                "taal": "Nederlands",
                "status": "operationeel"
            },
            "laatste_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Statistieken ophalen gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Statistieken konden niet worden opgehaald"
        )


@router.post("/threats/manual-report")
async def manual_threat_report(
    threat_description: str,
    threat_type: str,
    severity: str,
    source: str,
    background_tasks: BackgroundTasks,
    app_request: Request
):
    """
    Handmatige melding van cybersecurity bedreiging
    
    Voor gebruikers om handmatig bedreigingen te rapporteren
    """
    try:
        # Valideer input
        valid_types = ["phishing", "malware", "ransomware", "ddos", "social_engineering", "data_breach", "insider_threat", "apt"]
        valid_severities = ["critical", "high", "medium", "low", "info"]
        
        if threat_type not in valid_types:
            raise HTTPException(status_code=400, detail="Ongeldig bedreigingstype")
        
        if severity not in valid_severities:
            raise HTTPException(status_code=400, detail="Ongeldig ernst niveau")
        
        # Log handmatige melding
        logger.info(
            "Handmatige bedreiging gemeld",
            threat_type=threat_type,
            severity=severity,
            source=source,
            description=threat_description[:100]
        )
        
        # Verstuur notificatie naar beveiligingsteam
        notification_service = app_request.app.state.notification_service
        
        # Create een basis threat result voor notificatie
        from euramax.ai.threat_detector import ThreatDetectionResult, ThreatType, SeverityLevel
        
        manual_result = ThreatDetectionResult(
            threat_type=ThreatType(threat_type),
            severity=SeverityLevel(severity),
            confidence=0.9,  # Hoge confidence voor handmatige meldingen
            description=f"Handmatige melding: {threat_description}",
            indicators=[f"Gemeld door gebruiker via {source}"],
            recommended_actions=["Onderzoek handmatige melding", "Verifieer met beveiligingsteam"],
            dutch_description=f"Handmatige bedreiging melding ontvangen: {threat_description}",
            timestamp=datetime.now(),
            source_data={"manual_report": True, "source": source}
        )
        
        background_tasks.add_task(
            _send_threat_notification,
            notification_service,
            manual_result
        )
        
        return {
            "status": "success",
            "bericht": "Bedreiging melding ontvangen en doorgegeven aan beveiligingsteam",
            "melding_id": f"manual_{id(manual_result)}",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Handmatige melding gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Melding kon niet worden verwerkt"
        )


async def _send_threat_notification(notification_service, threat_result):
    """Helper functie voor het versturen van threat notificaties"""
    try:
        await notification_service.send_threat_notification(threat_result)
    except Exception as e:
        logger.error("Notificatie versturen gefaald", error=str(e))