"""
Tests for the threat detection system
"""

import pytest
from app.core.threat_detector import ThreatDetector
import asyncio

@pytest.fixture
def threat_detector():
    return ThreatDetector()

@pytest.mark.asyncio
async def test_phishing_detection(threat_detector):
    """Test phishing detection with known phishing content"""
    phishing_content = "URGENT: Your bank account has been compromised. Click here to secure it immediately."
    source = "email:test@phishing.com"
    
    threat = await threat_detector.analyze_content(phishing_content, source)
    
    assert threat is not None
    assert threat.threat_type == "phishing"
    assert threat.severity in ["high", "critical"]
    assert threat.confidence > 0.7

@pytest.mark.asyncio
async def test_legitimate_content(threat_detector):
    """Test that legitimate content is not flagged as threat"""
    legitimate_content = "Meeting scheduled for tomorrow at 2 PM in conference room A."
    source = "email:colleague@company.com"
    
    threat = await threat_detector.analyze_content(legitimate_content, source)
    
    assert threat is None

@pytest.mark.asyncio
async def test_threat_statistics(threat_detector):
    """Test threat statistics retrieval"""
    stats = await threat_detector.get_threat_statistics()
    
    assert isinstance(stats, dict)
    assert "total_threats_today" in stats
    assert "phishing_attempts" in stats
    assert "blocked_automatically" in stats

def test_suspicious_patterns(threat_detector):
    """Test that suspicious patterns are loaded correctly"""
    patterns = threat_detector.suspicious_patterns
    
    assert "phishing" in patterns
    assert "malware" in patterns
    assert "social_engineering" in patterns
    assert len(patterns["phishing"]) > 0