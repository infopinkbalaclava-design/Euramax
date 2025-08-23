"""
Database models for the cybersecurity defense system
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, JSON
from sqlalchemy.sql import func
from app.database.database import Base

class Threat(Base):
    __tablename__ = "threats"
    
    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(String, unique=True, index=True)
    threat_type = Column(String, index=True)  # phishing, malware, social_engineering, etc.
    severity = Column(String, index=True)  # low, medium, high, critical
    source = Column(String)  # email, web, network, etc.
    content = Column(Text)
    indicators = Column(JSON)  # List of detected patterns/indicators
    confidence = Column(Float)  # AI confidence score
    status = Column(String, default="detected")  # detected, blocked, resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))

class AIResponse(Base):
    __tablename__ = "ai_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(String, unique=True, index=True)
    threat_id = Column(String, index=True)
    actions_taken = Column(JSON)  # List of actions performed by AI
    status = Column(String)  # completed, failed, pending
    user_instructions = Column(JSON)  # Instructions in different languages
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(String, unique=True, index=True)
    type = Column(String, index=True)  # phishing_alert, threat_blocked, etc.
    title = Column(String)
    message = Column(Text)
    severity = Column(String, index=True)
    recipient = Column(String, index=True)
    channel = Column(String)  # websocket, email, sms
    language = Column(String)  # nl, en
    data = Column(JSON)  # Additional notification data
    sent_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    language_preference = Column(String, default="nl")  # nl, en
    notification_preferences = Column(JSON)  # Notification settings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))

class SecuritySettings(Base):
    __tablename__ = "security_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_name = Column(String, unique=True, index=True)
    setting_value = Column(JSON)
    description = Column(Text)
    updated_by = Column(String)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class BlockedDomains(Base):
    __tablename__ = "blocked_domains"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    blocked_by = Column(String)  # ai_bot, manual, etc.
    reason = Column(String)
    threat_id = Column(String)  # Associated threat if applicable
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # Optional expiration

class QuarantinedEmails(Base):
    __tablename__ = "quarantined_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String, unique=True, index=True)
    sender = Column(String, index=True)
    recipient = Column(String, index=True)
    subject = Column(String)
    content = Column(Text)
    threat_id = Column(String)
    quarantined_by = Column(String)  # ai_bot, manual
    is_released = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    released_at = Column(DateTime(timezone=True))