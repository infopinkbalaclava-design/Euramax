"""
AI Security Bot - Autonomous threat response system
Automatically handles phishing and other cybersecurity threats
"""

import asyncio
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass
from app.core.threat_detector import ThreatInfo

@dataclass
class BotResponse:
    action_id: str
    threat_id: str
    actions_taken: List[str]
    status: str
    timestamp: datetime
    user_instructions: Dict[str, str]  # Dutch and English instructions
    
    def dict(self):
        return {
            'action_id': self.action_id,
            'threat_id': self.threat_id,
            'actions_taken': self.actions_taken,
            'status': self.status,
            'timestamp': self.timestamp.isoformat(),
            'user_instructions': self.user_instructions
        }

class AISecurityBot:
    def __init__(self):
        self.action_history = []
        self.blocked_domains = set()
        self.quarantined_emails = []
        
    async def handle_phishing_threat(self, threat: ThreatInfo) -> BotResponse:
        """Main handler for phishing threats with automatic responses"""
        
        actions_taken = []
        action_id = f"action_{datetime.now().timestamp()}"
        
        # Automatic actions based on threat severity
        if threat.severity in ["critical", "high"]:
            # Block source immediately
            await self._block_threat_source(threat.source)
            actions_taken.append(f"Blocked source: {threat.source}")
            
            # Quarantine if email
            if "email:" in threat.source:
                await self._quarantine_email(threat)
                actions_taken.append("Email placed in quarantine")
            
            # Alert security team
            await self._alert_security_team(threat)
            actions_taken.append("Security team notified")
            
        # Additional actions for phishing
        if threat.threat_type == "phishing":
            # Extract and block malicious URLs
            urls = await self._extract_urls(threat.content)
            for url in urls:
                await self._block_domain(url)
                actions_taken.append(f"Blocked malicious domain: {url}")
        
        # Generate user instructions in Dutch and English
        user_instructions = self._generate_user_instructions(threat)
        
        response = BotResponse(
            action_id=action_id,
            threat_id=threat.threat_id,
            actions_taken=actions_taken,
            status="completed",
            timestamp=datetime.now(),
            user_instructions=user_instructions
        )
        
        self.action_history.append(response)
        return response
    
    async def _block_threat_source(self, source: str):
        """Block the source of the threat"""
        if "email:" in source:
            email_address = source.split(":", 1)[1]
            # In production, this would integrate with email security systems
            print(f"Blocking email address: {email_address}")
        
        elif "web:" in source:
            domain = source.split(":", 1)[1]
            await self._block_domain(domain)
    
    async def _quarantine_email(self, threat: ThreatInfo):
        """Place suspicious email in quarantine"""
        quarantine_entry = {
            'threat_id': threat.threat_id,
            'source': threat.source,
            'content': threat.content,
            'quarantined_at': datetime.now()
        }
        self.quarantined_emails.append(quarantine_entry)
        # In production, this would integrate with email systems
    
    async def _alert_security_team(self, threat: ThreatInfo):
        """Send alert to security team for high-severity threats"""
        # In production, this would send notifications via email, Slack, etc.
        print(f"SECURITY ALERT: {threat.threat_type.upper()} threat detected - Severity: {threat.severity}")
    
    async def _extract_urls(self, content: str) -> List[str]:
        """Extract URLs from content that might be malicious"""
        import re
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, content)
        
        # Filter out known safe domains (whitelist)
        safe_domains = ['google.com', 'microsoft.com', 'apple.com']
        suspicious_urls = []
        
        for url in urls:
            is_safe = any(domain in url for domain in safe_domains)
            if not is_safe:
                suspicious_urls.append(url)
        
        return suspicious_urls
    
    async def _block_domain(self, domain: str):
        """Add domain to blocked list"""
        self.blocked_domains.add(domain)
        # In production, this would integrate with firewall/DNS systems
        print(f"Domain blocked: {domain}")
    
    def _generate_user_instructions(self, threat: ThreatInfo) -> Dict[str, str]:
        """Generate step-by-step instructions for users in Dutch and English"""
        
        if threat.threat_type == "phishing":
            return {
                "dutch": f"""
🚨 PHISHING AANVAL GEDETECTEERD 🚨

ONMIDDELLIJKE ACTIES:
1. KLIK NIET op verdachte links in het bericht
2. Geef GEEN persoonlijke informatie prijs
3. Verwijder het bericht NIET (voor onderzoek)
4. Meld dit aan de IT-beveiligingsafdeling

HERKENNINGSKENMERKEN:
• Urgente taal: "onmiddellijk handelen vereist"
• Dreigingen over accountopschorting
• Verzoeken om persoonlijke gegevens
• Verdachte afzender: {threat.source}

STATUS: Automatisch geblokkeerd door AI-systeem
VEILIGHEID: Uw account is beveiligd
""",
                "english": f"""
🚨 PHISHING ATTACK DETECTED 🚨

IMMEDIATE ACTIONS:
1. DO NOT click any suspicious links in the message
2. DO NOT provide any personal information
3. DO NOT delete the message (needed for investigation)
4. Report this to IT Security department

RECOGNITION INDICATORS:
• Urgent language: "immediate action required"
• Threats about account suspension
• Requests for personal information
• Suspicious sender: {threat.source}

STATUS: Automatically blocked by AI system
SECURITY: Your account is protected
"""
            }
        
        # Default instructions for other threat types
        return {
            "dutch": f"""
🚨 CYBERBEDREIGING GEDETECTEERD 🚨

Type: {threat.threat_type.upper()}
Ernst: {threat.severity.upper()}

ONMIDDELLIJKE ACTIES:
1. Stop alle activiteit gerelateerd aan dit bericht
2. Neem contact op met IT-beveiliging
3. Wijzig indien nodig uw wachtwoorden

STATUS: Automatisch behandeld door AI-systeem
""",
            "english": f"""
🚨 CYBER THREAT DETECTED 🚨

Type: {threat.threat_type.upper()}
Severity: {threat.severity.upper()}

IMMEDIATE ACTIONS:
1. Stop all activity related to this message
2. Contact IT Security
3. Change your passwords if necessary

STATUS: Automatically handled by AI system
"""
        }
    
    async def get_action_history(self) -> List[BotResponse]:
        """Get history of all actions taken by the AI bot"""
        return self.action_history
    
    async def get_blocked_domains(self) -> List[str]:
        """Get list of currently blocked domains"""
        return list(self.blocked_domains)
    
    async def get_quarantined_emails(self) -> List[Dict]:
        """Get list of quarantined emails"""
        return self.quarantined_emails
    
    async def manual_override(self, action_id: str, action: str) -> bool:
        """Allow manual override of AI decisions"""
        # In production, this would require proper authentication and authorization
        if action == "unblock_domain":
            # Implementation for manual unblocking
            pass
        elif action == "release_quarantine":
            # Implementation for releasing quarantined emails
            pass
        
        return True