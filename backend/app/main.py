"""
Euramax AI-Powered Cybersecurity Defense System
Main FastAPI application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import asyncio
from typing import List

from app.api import threats, notifications, dashboard
from app.core.ai_bot import AISecurityBot
from app.core.notification_service import NotificationService
from app.core.threat_detector import ThreatDetector
from app.database.database import engine, SessionLocal
from app.database import models

# Initialize database
models.Base.metadata.create_all(bind=engine)

# Initialize core services
threat_detector = ThreatDetector()
ai_bot = AISecurityBot()
notification_service = NotificationService()

app = FastAPI(
    title="Euramax AI Cybersecurity Defense",
    description="AI-Powered Phishing Protection and Cybersecurity Defense System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(threats.router, prefix="/api/threats", tags=["threats"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

# WebSocket connection manager for real-time notifications
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            # Echo back for now (can be extended for bidirectional communication)
            await manager.send_personal_message(f"Message received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {
        "message": "Welkom bij Euramax AI Cybersecurity Defense System",
        "description": "AI-gestuurde phishing bescherming en cybersecurity verdediging",
        "version": "1.0.0",
        "endpoints": {
            "api_docs": "/api/docs",
            "dashboard": "/dashboard",
            "websocket": "/ws"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "threat_detector": "active",
            "ai_bot": "active", 
            "notification_service": "active"
        }
    }

# Background task for continuous threat monitoring
@app.on_event("startup")
async def startup_event():
    """Initialize background services on startup"""
    asyncio.create_task(background_threat_monitoring())

async def background_threat_monitoring():
    """Background task that continuously monitors for threats"""
    while True:
        try:
            # Simulate threat detection check
            threats = await threat_detector.scan_for_threats()
            
            for threat in threats:
                if threat.threat_type == "phishing":
                    # AI bot takes automatic action
                    response = await ai_bot.handle_phishing_threat(threat)
                    
                    # Send real-time notification
                    notification_data = {
                        "type": "phishing_detected",
                        "threat": threat.dict(),
                        "ai_response": response.dict(),
                        "timestamp": threat.detected_at.isoformat()
                    }
                    
                    await manager.broadcast(json.dumps(notification_data))
                    
        except Exception as e:
            print(f"Error in threat monitoring: {e}")
        
        # Check every 30 seconds
        await asyncio.sleep(30)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)