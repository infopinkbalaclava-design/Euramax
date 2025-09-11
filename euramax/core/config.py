"""
Euramax Core Configuration
Nederlandse configuratie voor het cybersecurity systeem
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Centrale configuratie voor het Euramax systeem"""
    
    # Basis Applicatie Instellingen
    app_name: str = "Euramax Cybersecurity Systeem"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # Database Configuratie
    database_url: str = "postgresql://user:password@localhost:5432/euramax"
    redis_url: str = "redis://localhost:6379/0"
    
    # Beveiliging Configuratie
    secret_key: str = "geheime-sleutel-hier"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email & Notificatie Configuratie
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = "admin@euramax.eu"
    smtp_password: str = "password"
    email_from: str = "noreply@euramax.eu"
    
    # Push Notificatie Configuratie
    push_service_key: Optional[str] = None
    notification_webhook_url: str = "https://api.euramax.eu/notifications"
    
    # AI Model Configuratie
    ai_model_path: str = "./models/"
    threat_detection_threshold: float = 0.85
    phishing_model_endpoint: str = "https://api.euramax.eu/ai/phishing"
    
    # Nederlandse Taal Configuratie
    dutch_language_model: str = "nl_core_news_sm"
    localization_path: str = "./locales/nl/"
    
    # CORS & API Configuratie
    cors_origins: List[str] = ["http://localhost:3000", "https://app.euramax.eu"]
    rate_limit_per_minute: int = 100
    max_email_size_mb: int = 25
    
    # Kafka Configuratie
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_security_topic: str = "euramax-security"
    kafka_notification_topic: str = "euramax-notifications"
    
    # Monitoring Configuratie
    prometheus_port: int = 8000
    log_level: str = "INFO"
    sentry_dsn: Optional[str] = None
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Globale instellingen instantie
settings = Settings()


class AppConfig:
    """Applicatie configuratie constanten"""
    
    # Nederlandse Interface Labels
    DUTCH_LABELS = {
        "phishing_detected": "Phishing-aanval gedetecteerd",
        "malware_detected": "Malware gedetecteerd", 
        "threat_blocked": "Bedreiging geblokkeerd",
        "security_alert": "Beveiligingswaarschuwing",
        "user_education": "Gebruikersvoorlichting",
        "automated_response": "Automatische reactie",
        "quarantine_success": "Quarantaine succesvol",
        "network_isolated": "Netwerk geïsoleerd"
    }
    
    # Threat Detection Types (Nederlandse beschrijvingen)
    THREAT_TYPES = {
        "phishing": "Phishing-aanval",
        "malware": "Kwaadaardige software",
        "ransomware": "Losgeld software",
        "ddos": "DDoS-aanval",
        "social_engineering": "Social engineering",
        "data_breach": "Datalek",
        "insider_threat": "Interne bedreiging",
        "apt": "Geavanceerde aanhoudende bedreiging"
    }
    
    # Notification Severity Levels
    SEVERITY_LEVELS = {
        "critical": "Kritiek",
        "high": "Hoog", 
        "medium": "Medium",
        "low": "Laag",
        "info": "Informatie"
    }
    
    # Default AI Model Settings
    AI_MODELS = {
        "phishing_detector": "phishing_nl_v1",
        "malware_scanner": "malware_detection_v2", 
        "behavioral_analyzer": "behavior_nl_v1",
        "threat_classifier": "threat_classification_v3"
    }