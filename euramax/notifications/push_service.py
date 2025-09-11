"""
Euramax Push Notification Service
Real-time beveiligingsmeldingen met Nederlandse educatieve content
"""

import asyncio
import json
import structlog
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import aiofiles
import httpx

from euramax.core.config import settings, AppConfig
from euramax.ai.threat_detector import ThreatDetectionResult, ThreatType, SeverityLevel


logger = structlog.get_logger()


class NotificationChannel(Enum):
    """Notificatie kanalen"""
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"
    DESKTOP = "desktop"
    WEBHOOK = "webhook"


@dataclass
class NotificationTemplate:
    """Template voor Nederlandse beveiligingsnotificaties"""
    title: str
    message: str
    instructions: List[str]
    educational_content: str
    urgency_level: str
    action_buttons: List[Dict[str, str]]


@dataclass
class User:
    """Gebruiker informatie voor notificaties"""
    user_id: str
    email: str
    phone: Optional[str]
    push_token: Optional[str]
    notification_preferences: Dict[str, bool]
    role: str
    department: str


class DutchNotificationTemplates:
    """Nederlandse notificatie templates voor verschillende bedreigingen"""
    
    PHISHING_TEMPLATES = {
        SeverityLevel.CRITICAL: NotificationTemplate(
            title="🚨 KRITIEKE PHISHING-AANVAL GEDETECTEERD",
            message="Er is een zeer gevaarlijke phishing-aanval onderschept die gericht is op uw organisatie. Onmiddellijke actie is vereist.",
            instructions=[
                "OPEN GEEN verdachte emails die u recent heeft ontvangen",
                "Controleer uw inbox op emails van onbekende afzenders",
                "Rapporteer verdachte emails aan security@euramax.eu",
                "Verander uw wachtwoorden als u recent op links heeft geklikt",
                "Neem contact op met IT-beveiliging voor hulp"
            ],
            educational_content="Phishing-aanvallen gebruiken vaak urgente taal en vragen om persoonlijke gegevens. Herken ze aan: onjuiste spelfouten, verdachte afzenders, urgente actie-oproepen en links naar onbekende websites.",
            urgency_level="KRITIEK",
            action_buttons=[
                {"text": "Rapporteer Verdachte Email", "action": "report_email"},
                {"text": "Neem Contact Op Met IT", "action": "contact_it"},
                {"text": "Bekijk Veiligheidstips", "action": "view_tips"}
            ]
        ),
        SeverityLevel.HIGH: NotificationTemplate(
            title="⚠️ Phishing-Aanval Gedetecteerd",
            message="Een phishing-poging is automatisch geblokkeerd. Controleer uw email voor verdachte berichten.",
            instructions=[
                "Controleer uw inbox op vergelijkbare emails",
                "Verwijder verdachte emails zonder te openen",
                "Rapporteer incident aan IT-beveiliging",
                "Deel deze waarschuwing met collega's"
            ],
            educational_content="Deze phishing-aanval toont typische kenmerken zoals neppe urgentie en oplichting. Wees altijd voorzichtig met emails die om persoonlijke informatie vragen.",
            urgency_level="HOOG",
            action_buttons=[
                {"text": "Controleer Email", "action": "check_email"},
                {"text": "Rapporteer Incident", "action": "report_incident"}
            ]
        ),
        SeverityLevel.MEDIUM: NotificationTemplate(
            title="🔍 Verdachte Email Activiteit",
            message="Onze AI heeft verdachte email activiteit gedetecteerd. Extra voorzichtigheid is aangeraden.",
            instructions=[
                "Wees extra voorzichtig met emails vandaag",
                "Controleer afzenders voordat u reageert",
                "Rapporteer ongewone emails",
                "Herinner collega's aan email beveiliging"
            ],
            educational_content="Verdachte email patronen kunnen wijzen op gerichte aanvallen. Blijf waakzaam en vertrouw uw instinct bij twijfelachtige emails.",
            urgency_level="MEDIUM",
            action_buttons=[
                {"text": "Bekijk Richtlijnen", "action": "view_guidelines"}
            ]
        )
    }
    
    MALWARE_TEMPLATES = {
        SeverityLevel.CRITICAL: NotificationTemplate(
            title="🦠 KRITIEKE MALWARE GEDETECTEERD",
            message="Gevaarlijke malware is gedetecteerd en automatisch in quarantaine geplaatst. Uw systeem wordt beschermd.",
            instructions=[
                "STOP met het gebruiken van het geïnfecteerde systeem",
                "Koppel het systeem los van het netwerk",
                "Neem onmiddellijk contact op met IT-beveiliging",
                "Voer geen bestanden uit van USB-sticks of downloads",
                "Waarschuw collega's over mogelijke besmetting"
            ],
            educational_content="Malware kan zich snel verspreiden en systemen beschadigen. Herken malware door: onverwachte pop-ups, langzame prestaties, onbekende programma's en verdachte netwerkactiviteit.",
            urgency_level="KRITIEK",
            action_buttons=[
                {"text": "Noodprotocol Activeren", "action": "activate_emergency"},
                {"text": "Isoleer Systeem", "action": "isolate_system"},
                {"text": "Contact IT-Beveiliging", "action": "contact_security"}
            ]
        )
    }
    
    DDOS_TEMPLATES = {
        SeverityLevel.HIGH: NotificationTemplate(
            title="🌐 DDoS-Aanval Gedetecteerd",
            message="Een DDoS-aanval op onze systemen is gedetecteerd. Automatische verdediging is geactiveerd.",
            instructions=[
                "Verwacht mogelijke vertragingen in systemen",
                "Gebruik kritieke systemen met voorzichtigheid", 
                "Rapporteer ongewone netwerkproblemen",
                "Volg updates via officiële kanalen"
            ],
            educational_content="DDoS-aanvallen overbelasten netwerken met verkeer. Onze systemen zijn uitgerust met automatische verdediging om de impact te minimaliseren.",
            urgency_level="HOOG",
            action_buttons=[
                {"text": "Bekijk Systeemstatus", "action": "view_status"},
                {"text": "Rapporteer Problemen", "action": "report_issues"}
            ]
        )
    }


class PushNotificationService:
    """Service voor real-time push notificaties"""
    
    def __init__(self):
        self.templates = DutchNotificationTemplates()
        self.active_users: Dict[str, User] = {}
        self.notification_history: List[Dict[str, Any]] = []
        self.is_initialized = False
    
    async def initialize(self):
        """Initialiseer notification service"""
        logger.info("Initialiseren van Push Notification Service")
        
        # Laad gebruikers configuratie (placeholder)
        await self._load_user_configurations()
        
        # Setup webhook endpoints
        await self._setup_webhooks()
        
        self.is_initialized = True
        logger.info("Push Notification Service operationeel")
    
    async def _load_user_configurations(self):
        """Laad gebruikers configuraties"""
        # Placeholder - in productie zou dit uit database komen
        self.active_users = {
            "admin": User(
                user_id="admin",
                email="admin@euramax.eu",
                phone="+31612345678",
                push_token="admin_push_token",
                notification_preferences={
                    "email": True,
                    "push": True,
                    "sms": True,
                    "desktop": True
                },
                role="administrator",
                department="IT-Beveiliging"
            ),
            "user1": User(
                user_id="user1",
                email="gebruiker@euramax.eu",
                phone="+31687654321",
                push_token="user1_push_token",
                notification_preferences={
                    "email": True,
                    "push": True,
                    "sms": False,
                    "desktop": True
                },
                role="employee",
                department="Algemeen"
            )
        }
        logger.info("Gebruikers configuraties geladen", user_count=len(self.active_users))
    
    async def _setup_webhooks(self):
        """Setup webhook endpoints voor externe integraties"""
        # Placeholder voor webhook setup
        logger.info("Webhook endpoints geconfigureerd")
    
    async def send_threat_notification(self, threat_result: ThreatDetectionResult, 
                                     target_users: Optional[List[str]] = None) -> Dict[str, Any]:
        """Verstuur bedreiging notificatie naar gebruikers"""
        if not self.is_initialized:
            logger.error("Notification service niet geïnitialiseerd")
            return {"status": "error", "message": "Service niet beschikbaar"}
        
        # Selecteer juiste template
        template = self._select_template(threat_result.threat_type, threat_result.severity)
        
        # Bepaal doelgebruikers
        users_to_notify = target_users or list(self.active_users.keys())
        
        notification_results = {}
        
        for user_id in users_to_notify:
            user = self.active_users.get(user_id)
            if not user:
                continue
            
            # Personaliseer notificatie voor gebruiker
            personalized_template = self._personalize_template(template, user, threat_result)
            
            # Verstuur via verschillende kanalen
            channels_sent = []
            
            if user.notification_preferences.get("push", False):
                await self._send_push_notification(user, personalized_template)
                channels_sent.append("push")
            
            if user.notification_preferences.get("email", False):
                await self._send_email_notification(user, personalized_template, threat_result)
                channels_sent.append("email")
            
            if user.notification_preferences.get("desktop", False):
                await self._send_desktop_notification(user, personalized_template)
                channels_sent.append("desktop")
            
            if threat_result.severity == SeverityLevel.CRITICAL and user.notification_preferences.get("sms", False):
                await self._send_sms_notification(user, personalized_template)
                channels_sent.append("sms")
            
            notification_results[user_id] = {
                "status": "sent",
                "channels": channels_sent,
                "timestamp": datetime.now().isoformat()
            }
        
        # Log notificatie
        notification_record = {
            "threat_id": id(threat_result),
            "threat_type": threat_result.threat_type.value,
            "severity": threat_result.severity.value,
            "users_notified": len(notification_results),
            "timestamp": datetime.now().isoformat(),
            "template_used": template.title
        }
        self.notification_history.append(notification_record)
        
        logger.info(
            "Bedreiging notificatie verzonden",
            threat_type=threat_result.threat_type.value,
            severity=threat_result.severity.value,
            users_notified=len(notification_results)
        )
        
        return {
            "status": "success",
            "message": f"Notificatie verzonden naar {len(notification_results)} gebruikers",
            "results": notification_results,
            "notification_id": notification_record["threat_id"]
        }
    
    def _select_template(self, threat_type: ThreatType, severity: SeverityLevel) -> NotificationTemplate:
        """Selecteer juiste template voor bedreiging"""
        if threat_type == ThreatType.PHISHING:
            return self.templates.PHISHING_TEMPLATES.get(
                severity, 
                self.templates.PHISHING_TEMPLATES[SeverityLevel.MEDIUM]
            )
        elif threat_type == ThreatType.MALWARE:
            return self.templates.MALWARE_TEMPLATES.get(
                severity,
                self.templates.MALWARE_TEMPLATES[SeverityLevel.CRITICAL]
            )
        elif threat_type == ThreatType.DDOS:
            return self.templates.DDOS_TEMPLATES.get(
                severity,
                self.templates.DDOS_TEMPLATES[SeverityLevel.HIGH]
            )
        else:
            # Fallback template voor andere bedreigingen
            return NotificationTemplate(
                title=f"🔒 {AppConfig.THREAT_TYPES[threat_type.value]} Gedetecteerd",
                message="Een beveiligingsbedreiging is gedetecteerd en gemonitord.",
                instructions=["Volg standaard beveiligingsprotocollen", "Rapporteer verdachte activiteiten"],
                educational_content="Blijf waakzaam voor cybersecurity bedreigingen en volg altijd de beveiligingsrichtlijnen.",
                urgency_level=severity.value.upper(),
                action_buttons=[{"text": "Bekijk Details", "action": "view_details"}]
            )
    
    def _personalize_template(self, template: NotificationTemplate, user: User, 
                            threat_result: ThreatDetectionResult) -> NotificationTemplate:
        """Personaliseer template voor specifieke gebruiker"""
        # Voeg rol-specifieke instructies toe
        personalized_instructions = template.instructions.copy()
        
        if user.role == "administrator":
            personalized_instructions.extend([
                "Controleer systeem logs voor verdere analyse",
                "Overweeg escalatie naar externe beveiligingsexperts",
                "Update beveiligingsbeleid indien nodig"
            ])
        elif user.role == "manager":
            personalized_instructions.extend([
                "Informeer uw team over deze bedreiging",
                "Overweeg werkstromen aanpassingen voor verhoogde beveiliging"
            ])
        
        # Personaliseer bericht met gebruiker details
        personalized_message = template.message
        if threat_result.source_data:
            source_info = threat_result.source_data
            if "sender" in source_info:
                personalized_message += f"\n\nAfzender: {source_info['sender']}"
            if "filename" in source_info:
                personalized_message += f"\n\nBestand: {source_info['filename']}"
        
        return NotificationTemplate(
            title=template.title,
            message=personalized_message,
            instructions=personalized_instructions,
            educational_content=template.educational_content,
            urgency_level=template.urgency_level,
            action_buttons=template.action_buttons
        )
    
    async def _send_push_notification(self, user: User, template: NotificationTemplate):
        """Verstuur push notificatie"""
        # Placeholder voor echte push notification service (FCM, APNS, etc.)
        logger.info(
            "Push notificatie verzonden",
            user_id=user.user_id,
            title=template.title
        )
    
    async def _send_email_notification(self, user: User, template: NotificationTemplate, 
                                     threat_result: ThreatDetectionResult):
        """Verstuur email notificatie met uitgebreide details"""
        email_body = f"""
        Beste {user.user_id},

        {template.message}

        URGENTIE: {template.urgency_level}

        INSTRUCTIES:
        {"".join(f"• {instruction}" for instruction in template.instructions)}

        EDUCATIEVE INFORMATIE:
        {template.educational_content}

        TECHNISCHE DETAILS:
        • Bedreiging Type: {AppConfig.THREAT_TYPES[threat_result.threat_type.value]}
        • Ernst Niveau: {AppConfig.SEVERITY_LEVELS[threat_result.severity.value]}
        • Betrouwbaarheid: {threat_result.confidence:.2%}
        • Detectie Tijd: {threat_result.timestamp.strftime('%d-%m-%Y %H:%M:%S')}

        Dit is een automatisch gegenereerd bericht van het Euramax Cybersecurity Systeem.

        Met vriendelijke groet,
        Het Euramax Beveiligingsteam
        """
        
        # Placeholder voor echte email verzending
        logger.info(
            "Email notificatie verzonden",
            user_id=user.user_id,
            email=user.email,
            subject=template.title
        )
    
    async def _send_desktop_notification(self, user: User, template: NotificationTemplate):
        """Verstuur desktop notificatie"""
        # Placeholder voor desktop notification (Windows/Mac/Linux)
        logger.info(
            "Desktop notificatie verzonden",
            user_id=user.user_id,
            title=template.title
        )
    
    async def _send_sms_notification(self, user: User, template: NotificationTemplate):
        """Verstuur SMS notificatie voor kritieke bedreigingen"""
        if not user.phone:
            return
        
        sms_message = f"EURAMAX BEVEILIGING: {template.title} - {template.message[:100]}... Controleer email voor details."
        
        # Placeholder voor SMS service
        logger.info(
            "SMS notificatie verzonden",
            user_id=user.user_id,
            phone=user.phone[:6] + "***"  # Partial masking for privacy
        )
    
    async def get_notification_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Verkrijg notificatie geschiedenis"""
        return self.notification_history[-limit:]
    
    async def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Verkrijg gebruiker notificatie voorkeuren"""
        user = self.active_users.get(user_id)
        if user:
            return {
                "user_id": user.user_id,
                "email": user.email,
                "notification_preferences": user.notification_preferences,
                "role": user.role,
                "department": user.department
            }
        return None
    
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, bool]) -> bool:
        """Update gebruiker notificatie voorkeuren"""
        user = self.active_users.get(user_id)
        if user:
            user.notification_preferences.update(preferences)
            logger.info("Gebruiker voorkeuren bijgewerkt", user_id=user_id)
            return True
        return False
    
    async def health_check(self) -> str:
        """Controleer gezondheid van notification service"""
        if not self.is_initialized:
            return "niet_geinitialiseerd"
        
        # Controleer connectiviteit met externe services (placeholder)
        return "operationeel"
    
    async def shutdown(self):
        """Sluit notification service af"""
        logger.info("Push Notification Service wordt afgesloten")
        self.is_initialized = False