"""
Euramax Notifications API Endpoints
Nederlandse API voor notificatiebeheer en gebruikersvoorkeuren
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime

from euramax.notifications.push_service import PushNotificationService


logger = structlog.get_logger()
router = APIRouter()


class UserPreferencesUpdate(BaseModel):
    """Model voor het updaten van gebruiker notificatie voorkeuren"""
    email: Optional[bool] = None
    push: Optional[bool] = None
    sms: Optional[bool] = None
    desktop: Optional[bool] = None


class TestNotificationRequest(BaseModel):
    """Model voor test notificatie verzoek"""
    test_type: str = "phishing"
    severity: str = "medium"
    target_users: Optional[List[str]] = None


@router.get("/history")
async def get_notification_history(
    limit: int = 50,
    app_request: Request = None
) -> Dict[str, Any]:
    """
    Verkrijg notificatie geschiedenis
    
    Nederlandse weergave van verzonden beveiligingsmeldingen
    """
    try:
        notification_service: PushNotificationService = app_request.app.state.notification_service
        
        history = await notification_service.get_notification_history(limit=limit)
        
        return {
            "status": "success",
            "notificatie_geschiedenis": history,
            "totaal_records": len(history),
            "limiet": limit,
            "laatste_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Notificatie geschiedenis ophalen gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Notificatie geschiedenis kon niet worden opgehaald"
        )


@router.get("/users/{user_id}/preferences")
async def get_user_notification_preferences(
    user_id: str,
    app_request: Request
) -> Dict[str, Any]:
    """
    Verkrijg notificatie voorkeuren voor gebruiker
    
    Nederlandse weergave van gebruiker instellingen
    """
    try:
        notification_service: PushNotificationService = app_request.app.state.notification_service
        
        preferences = await notification_service.get_user_preferences(user_id)
        
        if not preferences:
            raise HTTPException(
                status_code=404,
                detail="Gebruiker niet gevonden"
            )
        
        return {
            "status": "success",
            "gebruiker_voorkeuren": preferences,
            "beschikbare_kanalen": {
                "email": "E-mail notificaties",
                "push": "Push notificaties",
                "sms": "SMS berichten",
                "desktop": "Desktop meldingen"
            },
            "laatste_update": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Gebruiker voorkeuren ophalen gefaald", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Gebruiker voorkeuren konden niet worden opgehaald"
        )


@router.put("/users/{user_id}/preferences")
async def update_user_notification_preferences(
    user_id: str,
    preferences: UserPreferencesUpdate,
    app_request: Request
) -> Dict[str, Any]:
    """
    Update notificatie voorkeuren voor gebruiker
    
    Nederlandse interface voor het aanpassen van notificatie instellingen
    """
    try:
        notification_service: PushNotificationService = app_request.app.state.notification_service
        
        # Converteer naar dictionary, filter None waarden
        preferences_dict = {k: v for k, v in preferences.dict().items() if v is not None}
        
        if not preferences_dict:
            raise HTTPException(
                status_code=400,
                detail="Geen geldige voorkeuren opgegeven"
            )
        
        success = await notification_service.update_user_preferences(user_id, preferences_dict)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Gebruiker niet gevonden"
            )
        
        logger.info("Gebruiker voorkeuren bijgewerkt", user_id=user_id, changes=preferences_dict)
        
        return {
            "status": "success",
            "bericht": "Notificatie voorkeuren succesvol bijgewerkt",
            "gebruiker_id": user_id,
            "bijgewerkte_voorkeuren": preferences_dict,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Gebruiker voorkeuren updaten gefaald", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Voorkeuren konden niet worden bijgewerkt"
        )


@router.get("/channels/status")
async def get_notification_channels_status(app_request: Request) -> Dict[str, Any]:
    """
    Verkrijg status van notificatie kanalen
    
    Nederlandse weergave van systeemstatus
    """
    try:
        notification_service: PushNotificationService = app_request.app.state.notification_service
        
        health_status = await notification_service.health_check()
        
        return {
            "status": "success",
            "kanaal_status": {
                "email": "operationeel",
                "push": "operationeel", 
                "sms": "operationeel",
                "desktop": "operationeel",
                "webhook": "operationeel"
            },
            "algehele_status": health_status,
            "laatste_controle": datetime.now().isoformat(),
            "systeem_informatie": {
                "service": "Euramax Push Notification Service",
                "versie": "1.0.0",
                "taal": "Nederlands"
            }
        }
        
    except Exception as e:
        logger.error("Kanaal status controle gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kanaal status kon niet worden gecontroleerd"
        )


@router.post("/test")
async def send_test_notification(
    request: TestNotificationRequest,
    app_request: Request
) -> Dict[str, Any]:
    """
    Verstuur test notificatie
    
    Voor het testen van notificatie systeem en gebruiker voorkeuren
    """
    try:
        notification_service: PushNotificationService = app_request.app.state.notification_service
        
        # Valideer test type
        valid_test_types = ["phishing", "malware", "ddos", "ransomware"]
        if request.test_type not in valid_test_types:
            raise HTTPException(
                status_code=400,
                detail=f"Ongeldig test type. Geldige types: {', '.join(valid_test_types)}"
            )
        
        # Valideer severity
        valid_severities = ["critical", "high", "medium", "low", "info"]
        if request.severity not in valid_severities:
            raise HTTPException(
                status_code=400,
                detail=f"Ongeldig ernst niveau. Geldige niveaus: {', '.join(valid_severities)}"
            )
        
        # Maak test threat result
        from euramax.ai.threat_detector import ThreatDetectionResult, ThreatType, SeverityLevel
        
        test_result = ThreatDetectionResult(
            threat_type=ThreatType(request.test_type),
            severity=SeverityLevel(request.severity),
            confidence=0.95,
            description=f"TEST: {request.test_type} detectie test",
            indicators=["Dit is een test notificatie", "Geen actie vereist"],
            recommended_actions=["Test notificatie - negeer dit bericht"],
            dutch_description=f"TEST NOTIFICATIE: {request.test_type} detectie test uitgevoerd",
            timestamp=datetime.now(),
            source_data={"test": True, "test_type": request.test_type}
        )
        
        # Verstuur test notificatie
        result = await notification_service.send_threat_notification(
            test_result, 
            target_users=request.target_users
        )
        
        logger.info(
            "Test notificatie verzonden",
            test_type=request.test_type,
            severity=request.severity,
            target_users=request.target_users
        )
        
        return {
            "status": "success",
            "bericht": "Test notificatie succesvol verzonden",
            "test_details": {
                "type": request.test_type,
                "ernst": request.severity,
                "doel_gebruikers": request.target_users or "alle gebruikers"
            },
            "verzend_resultaat": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Test notificatie gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Test notificatie kon niet worden verzonden"
        )


@router.get("/templates")
async def get_notification_templates() -> Dict[str, Any]:
    """
    Verkrijg beschikbare notificatie templates
    
    Nederlandse weergave van alle beschikbare templates
    """
    try:
        from euramax.notifications.push_service import DutchNotificationTemplates
        
        templates_info = {
            "phishing_templates": {
                "critical": "Kritieke phishing-aanval template",
                "high": "Hoge risico phishing template", 
                "medium": "Medium risico phishing template"
            },
            "malware_templates": {
                "critical": "Kritieke malware detectie template"
            },
            "ddos_templates": {
                "high": "DDoS-aanval detectie template"
            }
        }
        
        return {
            "status": "success",
            "beschikbare_templates": templates_info,
            "taal": "Nederlands",
            "template_kenmerken": {
                "titel": "Nederlandse bedreiging titel",
                "bericht": "Uitgebreide Nederlandse beschrijving",
                "instructies": "Stap-voor-stap Nederlandse instructies",
                "educatieve_content": "Nederlandse educatieve informatie",
                "urgentie_niveau": "Nederlandse urgentie classificatie",
                "actie_knoppen": "Nederlandse actie opties"
            },
            "laatste_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Templates ophalen gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Templates konden niet worden opgehaald"
        )