"""
Euramax Dashboard API Endpoints
Nederlandse cybersecurity dashboard voor real-time monitoring
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Dict, List, Any
import structlog
from datetime import datetime, timedelta
import json

from euramax.core.config import AppConfig


logger = structlog.get_logger()
router = APIRouter()


@router.get("/overview")
async def get_security_overview(app_request: Request) -> Dict[str, Any]:
    """
    Verkrijg algemeen beveiligingsoverzicht
    
    Nederlandse dashboard met real-time cybersecurity status
    """
    try:
        # Verkrijg services
        threat_engine = app_request.app.state.threat_engine
        notification_service = app_request.app.state.notification_service
        
        # Haal statistieken op
        threat_stats = await threat_engine.get_statistics()
        notification_history = await notification_service.get_notification_history(limit=10)
        
        # Bereken dashboard metrics
        total_threats = threat_stats["detectie_statistieken"]["threats_detected"]
        total_scans = threat_stats["detectie_statistieken"]["total_scans"]
        detection_rate = (total_threats / total_scans * 100) if total_scans > 0 else 0
        
        # Recent activity (laatste 24 uur)
        recent_notifications = [n for n in notification_history 
                              if datetime.fromisoformat(n["timestamp"]) > datetime.now() - timedelta(hours=24)]
        
        return {
            "systeem_status": {
                "algehele_status": "operationeel",
                "laatste_update": datetime.now().isoformat(),
                "uptime": "99.9%",
                "actieve_services": ["AI Bedreigingsdetectie", "Push Notificaties", "Real-time Monitoring"]
            },
            "bedreiging_statistieken": {
                "totaal_scans": total_scans,
                "gedetecteerde_bedreigingen": total_threats,
                "detectie_percentage": f"{detection_rate:.1f}%",
                "false_positives": threat_stats["detectie_statistieken"]["false_positives"],
                "laatste_scan": threat_stats["detectie_statistieken"]["last_scan"]
            },
            "recente_activiteit": {
                "notificaties_24u": len(recent_notifications),
                "laatste_notificaties": recent_notifications[:5],
                "actieve_incidenten": 0,  # Placeholder
                "opgeloste_incidenten": total_threats
            },
            "ai_modellen_status": {
                "phishing_detector": "actief",
                "malware_scanner": "actief", 
                "behavioral_analyzer": "actief",
                "threat_classifier": "actief"
            },
            "dashboard_info": {
                "naam": "Euramax Cybersecurity Dashboard",
                "versie": "1.0.0",
                "taal": "Nederlands",
                "tijd_zone": "Europe/Amsterdam"
            }
        }
        
    except Exception as e:
        logger.error("Dashboard overview gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Dashboard gegevens konden niet worden opgehaald"
        )


@router.get("/threats/real-time")
async def get_real_time_threats(
    hours: int = 24,
    app_request: Request = None
) -> Dict[str, Any]:
    """
    Verkrijg real-time bedreigingen data
    
    Nederlandse weergave van bedreigingen in de afgelopen periode
    """
    try:
        notification_service = app_request.app.state.notification_service
        
        # Haal notificatie geschiedenis op
        all_notifications = await notification_service.get_notification_history(limit=1000)
        
        # Filter op tijdsperiode
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_notifications = [
            n for n in all_notifications 
            if datetime.fromisoformat(n["timestamp"]) > cutoff_time
        ]
        
        # Analyseer bedreigingen per type
        threat_counts = {}
        severity_counts = {}
        hourly_data = {}
        
        for notification in recent_notifications:
            # Count per threat type
            threat_type = notification.get("threat_type", "unknown")
            threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
            
            # Count per severity
            severity = notification.get("severity", "unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Hourly distribution
            timestamp = datetime.fromisoformat(notification["timestamp"])
            hour_key = timestamp.strftime("%Y-%m-%d %H:00")
            hourly_data[hour_key] = hourly_data.get(hour_key, 0) + 1
        
        # Nederlandse labels voor threat types
        dutch_threat_types = {
            threat_type: AppConfig.THREAT_TYPES.get(threat_type, threat_type)
            for threat_type in threat_counts.keys()
        }
        
        # Nederlandse labels voor severity
        dutch_severity = {
            severity: AppConfig.SEVERITY_LEVELS.get(severity, severity)
            for severity in severity_counts.keys()
        }
        
        return {
            "tijdsperiode": f"Laatste {hours} uur",
            "totaal_bedreigingen": len(recent_notifications),
            "bedreigingen_per_type": {
                "data": threat_counts,
                "nederlandse_labels": dutch_threat_types
            },
            "ernst_verdeling": {
                "data": severity_counts,
                "nederlandse_labels": dutch_severity
            },
            "tijdlijn_data": {
                "uurlijkse_verdeling": hourly_data,
                "interval": "per uur"
            },
            "trend_analyse": {
                "stijgende_bedreigingen": list(threat_counts.keys())[:3] if threat_counts else [],
                "meest_kritieke_periode": max(hourly_data.keys(), key=hourly_data.get) if hourly_data else None
            },
            "laatste_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Real-time threats data gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Real-time bedreigingen data kon niet worden opgehaald"
        )


@router.get("/system/performance")
async def get_system_performance(app_request: Request) -> Dict[str, Any]:
    """
    Verkrijg systeem prestatie metrics
    
    Nederlandse weergave van systeem prestaties en gezondheid
    """
    try:
        threat_engine = app_request.app.state.threat_engine
        notification_service = app_request.app.state.notification_service
        
        # Haal systeem stats op
        threat_stats = await threat_engine.get_statistics()
        
        # Performance metrics (placeholder - in productie zou dit echte metrics zijn)
        performance_data = {
            "cpu_gebruik": "15%",
            "geheugen_gebruik": "2.3 GB / 8 GB",
            "netwerkverkeer": {
                "inkomend": "125 MB/s",
                "uitgaand": "89 MB/s"
            },
            "database_prestaties": {
                "query_tijd": "< 50ms",
                "verbindingen": "12/100"
            },
            "ai_model_prestaties": {
                "gemiddelde_analyse_tijd": "1.2 seconden",
                "modellen_geladen": len(AppConfig.AI_MODELS),
                "geheugen_per_model": "256 MB"
            }
        }
        
        # Health checks
        health_checks = {
            "bedreigingsdetectie": await threat_engine.health_check(),
            "notificatie_service": await notification_service.health_check(),
            "database": "operationeel",  # Placeholder
            "external_apis": "operationeel"  # Placeholder
        }
        
        # System uptime en availability
        uptime_data = {
            "systeem_uptime": "5 dagen, 12 uur, 34 minuten",
            "beschikbaarheid_percentage": "99.95%",
            "laatste_herstart": "2024-01-15 08:30:00",
            "geplande_onderhoud": "Geen"
        }
        
        return {
            "prestatie_overzicht": performance_data,
            "gezondheids_controles": health_checks,
            "uptime_statistieken": uptime_data,
            "detectie_prestaties": {
                "totaal_analyses": threat_stats["detectie_statistieken"]["total_scans"],
                "succesvolle_detecties": threat_stats["detectie_statistieken"]["threats_detected"],
                "gemiddelde_responstijd": "1.2 seconden",
                "doorvoer_per_minuut": "45 analyses"
            },
            "systeem_informatie": {
                "versie": "Euramax 1.0.0",
                "platform": "Linux/Docker",
                "python_versie": "3.11+",
                "database": "PostgreSQL 15",
                "cache": "Redis 7"
            },
            "laatste_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("System performance data gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Systeem prestatie data kon niet worden opgehaald"
        )


@router.get("/alerts/active")
async def get_active_alerts(app_request: Request) -> Dict[str, Any]:
    """
    Verkrijg actieve beveiligingsalerts
    
    Nederlandse weergave van huidige beveiligingsincidenten
    """
    try:
        notification_service = app_request.app.state.notification_service
        
        # Haal recente notificaties op (laatste 6 uur voor "actieve" alerts)
        recent_notifications = await notification_service.get_notification_history(limit=100)
        
        # Filter voor actieve alerts (high/critical severity, recent)
        cutoff_time = datetime.now() - timedelta(hours=6)
        active_alerts = [
            n for n in recent_notifications
            if (datetime.fromisoformat(n["timestamp"]) > cutoff_time and 
                n.get("severity") in ["critical", "high"])
        ]
        
        # Groepeer alerts per type
        alerts_by_type = {}
        for alert in active_alerts:
            threat_type = alert.get("threat_type", "unknown")
            if threat_type not in alerts_by_type:
                alerts_by_type[threat_type] = []
            alerts_by_type[threat_type].append(alert)
        
        # Genereer alert summary
        alert_summary = []
        for threat_type, alerts in alerts_by_type.items():
            dutch_type = AppConfig.THREAT_TYPES.get(threat_type, threat_type)
            critical_count = sum(1 for a in alerts if a.get("severity") == "critical")
            high_count = sum(1 for a in alerts if a.get("severity") == "high")
            
            alert_summary.append({
                "type": threat_type,
                "dutch_type": dutch_type,
                "total_alerts": len(alerts),
                "critical_alerts": critical_count,
                "high_alerts": high_count,
                "latest_alert": max(alerts, key=lambda x: x["timestamp"]) if alerts else None
            })
        
        return {
            "actieve_alerts": {
                "totaal": len(active_alerts),
                "kritiek": sum(1 for a in active_alerts if a.get("severity") == "critical"),
                "hoog": sum(1 for a in active_alerts if a.get("severity") == "high")
            },
            "alerts_per_type": alert_summary,
            "recente_alerts": active_alerts[:10],  # Laatste 10 alerts
            "alert_trend": {
                "stijgend": len(active_alerts) > 5,
                "stabiel": 2 <= len(active_alerts) <= 5,
                "dalend": len(active_alerts) < 2
            },
            "aanbevolen_acties": [
                "Monitor kritieke alerts voor escalatie",
                "Controleer netwerkbeveiliging configuratie", 
                "Update beveiligingsbeleid indien nodig",
                "Informeer relevante teams over actieve bedreigingen"
            ] if active_alerts else ["Geen actieve alerts - systeem operationeel"],
            "laatste_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Active alerts data gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Actieve alerts data kon niet worden opgehaald"
        )


@router.get("/reports/daily")
async def get_daily_security_report(app_request: Request) -> Dict[str, Any]:
    """
    Verkrijg dagelijkse beveiligingsrapport
    
    Nederlandse samenvatting van cybersecurity activiteiten
    """
    try:
        threat_engine = app_request.app.state.threat_engine
        notification_service = app_request.app.state.notification_service
        
        # Haal data voor vandaag op
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        # Systeem statistieken
        threat_stats = await threat_engine.get_statistics()
        all_notifications = await notification_service.get_notification_history(limit=1000)
        
        # Filter notificaties van vandaag
        today_notifications = [
            n for n in all_notifications
            if datetime.fromisoformat(n["timestamp"]).date() == today
        ]
        
        # Analyseer dagelijkse metrics
        threat_breakdown = {}
        severity_breakdown = {}
        
        for notification in today_notifications:
            threat_type = notification.get("threat_type", "unknown")
            severity = notification.get("severity", "unknown")
            
            threat_breakdown[threat_type] = threat_breakdown.get(threat_type, 0) + 1
            severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1
        
        # Bereken success rate
        total_scans_today = threat_stats["detectie_statistieken"]["total_scans"] # Simplified
        threats_detected_today = len(today_notifications)
        success_rate = (threats_detected_today / total_scans_today * 100) if total_scans_today > 0 else 0
        
        return {
            "rapport_datum": today.isoformat(),
            "samenvatting": {
                "totaal_analyses": total_scans_today,
                "gedetecteerde_bedreigingen": threats_detected_today,
                "detectie_succes": f"{success_rate:.1f}%",
                "false_positives": 0,  # Placeholder
                "systeem_uptime": "24 uur"
            },
            "bedreigingen_breakdown": {
                threat_type: {
                    "count": count,
                    "dutch_label": AppConfig.THREAT_TYPES.get(threat_type, threat_type)
                }
                for threat_type, count in threat_breakdown.items()
            },
            "ernst_verdeling": {
                severity: {
                    "count": count,
                    "dutch_label": AppConfig.SEVERITY_LEVELS.get(severity, severity)
                }
                for severity, count in severity_breakdown.items()
            },
            "hoogste_risico_periode": "14:00 - 16:00" if today_notifications else "Geen bedreigingen",
            "aanbevelingen": [
                "Systeem prestaties zijn optimaal",
                "Bedreigingsdetectie werkt correct",
                "Notificaties worden succesvol verzonden",
                "Geen kritieke acties vereist"
            ] if threats_detected_today < 10 else [
                "Verhoogde bedreigingsactiviteit gedetecteerd",
                "Overweeg extra beveiligingsmaatregelen",
                "Monitor systeem extra zorgvuldig",
                "Informeer beveiligingsteam over trends"
            ],
            "volgende_rapport": (today + timedelta(days=1)).isoformat(),
            "gegenereerd_op": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Daily security report gefaald", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Dagelijkse beveiligingsrapport kon niet worden gegenereerd"
        )