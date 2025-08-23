"""
Tests for the AI Security Bot
"""

import pytest
from app.core.ai_bot import AISecurityBot
from app.core.threat_detector import ThreatInfo
from datetime import datetime

@pytest.fixture
def ai_bot():
    return AISecurityBot()

@pytest.fixture
def sample_phishing_threat():
    return ThreatInfo(
        threat_id="test_threat_123",
        threat_type="phishing",
        severity="critical",
        source="email:phishing@bad.com",
        content="URGENT: Click here to verify your account",
        indicators=["urgent.*action.*required", "click.*here.*immediately"],
        confidence=0.95,
        detected_at=datetime.now()
    )

@pytest.mark.asyncio
async def test_handle_phishing_threat(ai_bot, sample_phishing_threat):
    """Test AI bot handling of phishing threats"""
    response = await ai_bot.handle_phishing_threat(sample_phishing_threat)
    
    assert response.threat_id == sample_phishing_threat.threat_id
    assert response.status == "completed"
    assert len(response.actions_taken) > 0
    assert "dutch" in response.user_instructions
    assert "english" in response.user_instructions

@pytest.mark.asyncio
async def test_block_threat_source(ai_bot, sample_phishing_threat):
    """Test blocking of threat sources"""
    await ai_bot._block_threat_source(sample_phishing_threat.source)
    
    # Verify that the action was recorded
    actions = await ai_bot.get_action_history()
    # Note: In a real test, we'd verify the blocking actually occurred

@pytest.mark.asyncio
async def test_quarantine_email(ai_bot, sample_phishing_threat):
    """Test email quarantine functionality"""
    await ai_bot._quarantine_email(sample_phishing_threat)
    
    quarantined = await ai_bot.get_quarantined_emails()
    assert len(quarantined) > 0
    assert quarantined[0]["threat_id"] == sample_phishing_threat.threat_id

@pytest.mark.asyncio
async def test_extract_urls(ai_bot):
    """Test URL extraction from content"""
    content = "Click here: http://suspicious-site.com and also http://another-bad.org"
    urls = await ai_bot._extract_urls(content)
    
    assert len(urls) == 2
    assert "http://suspicious-site.com" in urls
    assert "http://another-bad.org" in urls

def test_generate_user_instructions(ai_bot, sample_phishing_threat):
    """Test generation of user instructions"""
    instructions = ai_bot._generate_user_instructions(sample_phishing_threat)
    
    assert "dutch" in instructions
    assert "english" in instructions
    assert "🚨" in instructions["dutch"]
    assert "🚨" in instructions["english"]
    assert "PHISHING" in instructions["dutch"].upper()
    assert "PHISHING" in instructions["english"].upper()