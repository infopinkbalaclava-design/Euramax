"""
Test cases voor Euramax Cybersecurity Systeem
Nederlandse unit tests voor AI bedreigingsdetectie
"""

import pytest
import asyncio
from datetime import datetime
from euramax.ai.threat_detector import (
    ThreatDetectionEngine, 
    PhishingDetector, 
    MalwareDetector,
    ThreatType,
    SeverityLevel
)
from euramax.notifications.push_service import PushNotificationService


class TestPhishingDetector:
    """Test cases voor phishing detectie"""
    
    @pytest.fixture
    def detector(self):
        return PhishingDetector()
    
    @pytest.mark.asyncio
    async def test_phishing_email_detection(self, detector):
        """Test detectie van verdachte phishing email"""
        email_content = "Urgent! Your account will be suspended. Click here to verify: http://suspicious-link.com"
        sender = "security@fake-bank.com"
        subject = "URGENT: Account Verification Required"
        
        result = await detector.analyze_email(email_content, sender, subject)
        
        assert result.threat_type == ThreatType.PHISHING
        assert result.confidence > 0.3  # Moet verdachte patronen detecteren
        assert len(result.indicators) > 0
        assert "verify" in str(result.indicators).lower() or "urgent" in str(result.indicators).lower()
        assert result.dutch_description is not None
        assert len(result.recommended_actions) > 0
    
    @pytest.mark.asyncio  
    async def test_legitimate_email_detection(self, detector):
        """Test dat legitieme emails niet als phishing worden gemarkeerd"""
        email_content = "Bedankt voor uw bestelling. Uw pakket wordt morgen bezorgd."
        sender = "service@bol.com"
        subject = "Bevestiging van uw bestelling"
        
        result = await detector.analyze_email(email_content, sender, subject)
        
        assert result.confidence < 0.5  # Lage verdachte score
        assert result.severity in [SeverityLevel.LOW, SeverityLevel.INFO]


class TestMalwareDetector:
    """Test cases voor malware detectie"""
    
    @pytest.fixture
    def detector(self):
        return MalwareDetector()
    
    @pytest.mark.asyncio
    async def test_suspicious_executable_detection(self, detector):
        """Test detectie van verdachte executable bestanden"""
        suspicious_content = b"powershell -exec bypass -c (new-object system.net.webclient).downloadfile"
        filename = "suspicious_file.exe"
        
        result = await detector.analyze_file(suspicious_content, filename)
        
        assert result.threat_type == ThreatType.MALWARE
        assert result.confidence > 0.5  # Moet verdachte content detecteren
        assert filename in str(result.source_data)
        assert any("PowerShell" in indicator for indicator in result.indicators)
    
    @pytest.mark.asyncio
    async def test_safe_file_detection(self, detector):
        """Test dat veilige bestanden niet als malware worden gemarkeerd"""
        safe_content = b"Dit is een veilig tekstbestand met normale content."
        filename = "document.txt"
        
        result = await detector.analyze_file(safe_content, filename)
        
        assert result.confidence < 0.7  # Lage malware score voor veilige bestanden


class TestThreatDetectionEngine:
    """Test cases voor de hoofddetectie engine"""
    
    @pytest.fixture
    def engine(self):
        return ThreatDetectionEngine()
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self, engine):
        """Test initialisatie van threat detection engine"""
        await engine.initialize()
        
        assert engine.is_running == True
        assert engine.phishing_detector is not None
        assert engine.malware_detector is not None
        assert engine.detection_stats["total_scans"] == 0
    
    @pytest.mark.asyncio
    async def test_email_analysis_integration(self, engine):
        """Test volledige email analyse workflow"""
        await engine.initialize()
        
        result = await engine.analyze_email(
            "Klik hier voor gratis geld! http://scam.com",
            "scammer@evil.com", 
            "GRATIS GELD WACHT OP U!"
        )
        
        assert result is not None
        assert engine.detection_stats["total_scans"] == 1
        assert result.timestamp is not None
        assert result.dutch_description is not None
    
    @pytest.mark.asyncio
    async def test_network_analysis(self, engine):
        """Test netwerkactiviteit analyse"""
        await engine.initialize()
        
        result = await engine.analyze_network_activity(
            "192.168.1.100",  # Verdachte IP
            "8.8.8.8",
            b"GET / HTTP/1.1\r\n" * 1000  # Groot request
        )
        
        assert result is not None
        assert result.threat_type in [ThreatType.DDOS, ThreatType.APT]
        assert "IP" in str(result.indicators) or "request" in str(result.indicators)
    
    @pytest.mark.asyncio
    async def test_statistics_tracking(self, engine):
        """Test statistieken bijhouden"""
        await engine.initialize()
        
        # Voer meerdere analyses uit
        await engine.analyze_email("test", "test@test.com", "test")
        await engine.analyze_file(b"test content", "test.txt")
        
        stats = await engine.get_statistics()
        
        assert stats["detectie_statistieken"]["total_scans"] >= 2
        assert "systeem_status" in stats
        assert stats["ai_modellen"]["status"] == "actief"


class TestPushNotificationService:
    """Test cases voor push notification service"""
    
    @pytest.fixture
    def service(self):
        return PushNotificationService()
    
    @pytest.mark.asyncio
    async def test_service_initialization(self, service):
        """Test initialisatie van notification service"""
        await service.initialize()
        
        assert service.is_initialized == True
        assert len(service.active_users) > 0
        assert service.templates is not None
    
    @pytest.mark.asyncio
    async def test_threat_notification_sending(self, service):
        """Test versturen van threat notificaties"""
        await service.initialize()
        
        # Maak een test threat result
        from euramax.ai.threat_detector import ThreatDetectionResult
        
        test_threat = ThreatDetectionResult(
            threat_type=ThreatType.PHISHING,
            severity=SeverityLevel.HIGH,
            confidence=0.9,
            description="Test phishing threat",
            indicators=["Test indicator"],
            recommended_actions=["Test action"],
            dutch_description="Test Nederlandse beschrijving",
            timestamp=datetime.now(),
            source_data={"test": True}
        )
        
        result = await service.send_threat_notification(test_threat)
        
        assert result["status"] == "success"
        assert "gebruikers" in result["message"] or "users_notified" in result["message"]
        assert len(service.notification_history) > 0
    
    @pytest.mark.asyncio
    async def test_user_preferences_management(self, service):
        """Test beheren van gebruiker voorkeuren"""
        await service.initialize()
        
        user_id = "admin"
        new_preferences = {"email": False, "sms": True}
        
        # Update voorkeuren
        success = await service.update_user_preferences(user_id, new_preferences)
        assert success == True
        
        # Controleer of voorkeuren zijn bijgewerkt
        preferences = await service.get_user_preferences(user_id)
        assert preferences["notification_preferences"]["email"] == False
        assert preferences["notification_preferences"]["sms"] == True


class TestDutchLocalization:
    """Test cases voor Nederlandse lokalisatie"""
    
    def test_dutch_threat_labels(self):
        """Test Nederlandse labels voor bedreigingen"""
        from euramax.core.config import AppConfig
        
        # Controleer of alle threat types Nederlandse labels hebben
        for threat_type in ["phishing", "malware", "ransomware", "ddos"]:
            assert threat_type in AppConfig.THREAT_TYPES
            dutch_label = AppConfig.THREAT_TYPES[threat_type]
            assert dutch_label is not None
            assert len(dutch_label) > 0
            assert dutch_label != threat_type  # Moet vertaald zijn
    
    def test_dutch_severity_labels(self):
        """Test Nederlandse labels voor ernst niveaus"""
        from euramax.core.config import AppConfig
        
        for severity in ["critical", "high", "medium", "low"]:
            assert severity in AppConfig.SEVERITY_LEVELS
            dutch_label = AppConfig.SEVERITY_LEVELS[severity]
            assert dutch_label is not None
            assert len(dutch_label) > 0
    
    def test_dutch_interface_labels(self):
        """Test Nederlandse interface labels"""
        from euramax.core.config import AppConfig
        
        expected_labels = [
            "phishing_detected", "malware_detected", "threat_blocked", 
            "security_alert", "user_education", "automated_response"
        ]
        
        for label in expected_labels:
            assert label in AppConfig.DUTCH_LABELS
            dutch_text = AppConfig.DUTCH_LABELS[label]
            assert dutch_text is not None
            assert len(dutch_text) > 0


# pytest configuratie voor asyncio tests
pytest_plugins = ('pytest_asyncio',)


if __name__ == "__main__":
    # Run tests als script wordt uitgevoerd
    pytest.main([__file__, "-v"])