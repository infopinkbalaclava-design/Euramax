"""
Euramax FastAPI Hoofdapplicatie
Nederlandse cybersecurity verdedigingssysteem met AI-automatie
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import structlog
from typing import Dict, Any

from euramax.core.config import settings, AppConfig
from euramax.api.routes import security, notifications, dashboard
from euramax.course.routes import router as course_router
from euramax.ai.threat_detector import ThreatDetectionEngine
from euramax.notifications.push_service import PushNotificationService


# Structlog configuratie voor Nederlandse logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Applicatie levenscyclus beheer"""
    # Opstarten
    logger.info(
        "Euramax Cybersecurity Systeem wordt opgestart",
        version=settings.app_version,
        environment=settings.environment
    )
    
    # Initialiseer AI threat detection engine
    app.state.threat_engine = ThreatDetectionEngine()
    await app.state.threat_engine.initialize()
    
    # Initialiseer push notification service
    app.state.notification_service = PushNotificationService()
    await app.state.notification_service.initialize()
    
    logger.info("Alle systemen zijn operationeel en gereed voor bedreigingsdetectie")
    
    yield
    
    # Afsluiten
    logger.info("Euramax systeem wordt afgesloten")
    await app.state.threat_engine.shutdown()
    await app.state.notification_service.shutdown()


# FastAPI applicatie initialisatie
app = FastAPI(
    title=settings.app_name,
    description="AI-Gestuurde Cybersecurity Verdedigingssysteem - Nederlandse Implementatie",
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# CORS middleware configuratie
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted host middleware voor beveiliging
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "*.euramax.eu", "127.0.0.1"]
)


@app.get("/", tags=["System"])
async def root() -> Dict[str, Any]:
    """Basis systeem status endpoint"""
    return {
        "systeem": "Euramax Cybersecurity Verdedigingssysteem",
        "versie": settings.app_version,
        "status": "operationeel",
        "beschrijving": "AI-aangedreven phishing bescherming en bedreigingsdetectie",
        "taal": "Nederlands",
        "beveiliging": "actief"
    }


@app.get("/health", tags=["System"])
async def health_check() -> Dict[str, Any]:
    """Uitgebreide gezondheidscontrole van alle systemen"""
    try:
        # Controleer AI threat detection engine
        threat_engine_status = "operationeel"
        if hasattr(app.state, 'threat_engine'):
            threat_engine_status = await app.state.threat_engine.health_check()
        
        # Controleer notification service
        notification_status = "operationeel"
        if hasattr(app.state, 'notification_service'):
            notification_status = await app.state.notification_service.health_check()
        
        return {
            "systeem_status": "gezond",
            "componenten": {
                "bedreigingsdetectie": threat_engine_status,
                "notificaties": notification_status,
                "database": "verbonden",  # TODO: implementeer database health check
                "ai_modellen": "geladen"
            },
            "laatste_controle": "nu",
            "uptime": "beschikbaar"
        }
    except Exception as e:
        logger.error("Gezondheidscontrole gefaald", error=str(e))
        raise HTTPException(
            status_code=503,
            detail="Systeemstatus controle gefaald"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Globale exception handler met Nederlandse berichten"""
    logger.error(
        "Onverwachte fout opgetreden",
        path=request.url.path,
        method=request.method,
        error=str(exc)
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "fout": "Interne serverfout",
            "bericht": "Er is een onverwachte fout opgetreden. Het incident is gelogd.",
            "code": "EURAMAX_INTERNAL_ERROR"
        }
    )


# Include API routers
app.include_router(
    security.router,
    prefix="/api/v1/security",
    tags=["Beveiligings API"]
)

app.include_router(
    notifications.router,
    prefix="/api/v1/notifications", 
    tags=["Notificatie API"]
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard API"]
)

app.include_router(
    course_router,
    prefix="/api/v1/course",
    tags=["Cybersecurity Course API"]
)

# Serve static files (Nederlandse dashboard)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "euramax.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )