"""
Course API Routes
Nederlandse cybersecurity cursus API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

from euramax.course.models import CourseModule, QuizQuestion, QuizAttempt, UserProgress
from euramax.course.content import cybersecurity_course
from euramax.course.quiz_service import quiz_service

router = APIRouter()


# Request/Response Models
class QuizSubmissionRequest(BaseModel):
    """Request model voor quiz inzending"""
    user_id: str
    module_id: str
    answers: Dict[str, int]  # question_id -> answer_index


class CourseProgressResponse(BaseModel):
    """Response model voor cursusvoortgang"""
    user_id: str
    completion_percentage: int
    completed_modules: int
    total_modules: int
    average_score: int
    modules_progress: Dict[str, UserProgress]


# Course Overview Endpoints
@router.get("/", tags=["Course Overview"])
async def get_course_overview() -> Dict[str, Any]:
    """Haal cursusoverzicht op"""
    return {
        "titel": cybersecurity_course.course_title,
        "beschrijving": cybersecurity_course.course_description,
        "totale_duur": cybersecurity_course.total_duration,
        "aantal_modules": len(cybersecurity_course.modules),
        "certificaat_beschikbaar": cybersecurity_course.completion_certificate,
        "modules": [
            {
                "id": module.id,
                "titel": module.title,
                "beschrijving": module.description,
                "moeilijkheidsgraad": module.difficulty,
                "geschatte_duur": module.estimated_duration,
                "aantal_quiz_vragen": len(module.quiz_questions)
            }
            for module in cybersecurity_course.modules
        ]
    }


@router.get("/modules", tags=["Course Modules"])
async def get_all_modules() -> List[Dict[str, Any]]:
    """Haal alle cursusmodules op"""
    return [
        {
            "id": module.id,
            "titel": module.title,
            "beschrijving": module.description,
            "moeilijkheidsgraad": module.difficulty,
            "geschatte_duur": module.estimated_duration,
            "leerdoelen": module.learning_objectives,
            "aantal_quiz_vragen": len(module.quiz_questions)
        }
        for module in cybersecurity_course.modules
    ]


@router.get("/modules/{module_id}", tags=["Course Modules"])
async def get_module_details(module_id: str) -> Dict[str, Any]:
    """Haal gedetailleerde module informatie op"""
    module = quiz_service.get_module_by_id(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module niet gevonden")
    
    return {
        "id": module.id,
        "titel": module.title,
        "beschrijving": module.description,
        "moeilijkheidsgraad": module.difficulty,
        "geschatte_duur": module.estimated_duration,
        "inhoud": module.content,
        "leerdoelen": module.learning_objectives,
        "aantal_quiz_vragen": len(module.quiz_questions)
    }


# Quiz Endpoints
@router.get("/modules/{module_id}/quiz", tags=["Quiz"])
async def get_module_quiz(
    module_id: str,
    randomize: bool = Query(True, description="Randomize question order")
) -> Dict[str, Any]:
    """Haal quiz vragen voor een module op"""
    questions = quiz_service.get_quiz_questions(module_id, randomize)
    if not questions:
        raise HTTPException(status_code=404, detail="Geen quiz vragen gevonden voor deze module")
    
    # Verwijder correct_answer uit response voor beveiliging
    quiz_questions = []
    for q in questions:
        quiz_questions.append({
            "id": q.id,
            "vraag_type": q.question_type,
            "vraag_tekst": q.question_text,
            "opties": q.options,
            "moeilijkheidsgraad": q.difficulty,
            "punten": q.points
        })
    
    module = quiz_service.get_module_by_id(module_id)
    return {
        "module_id": module_id,
        "module_titel": module.title if module else "Onbekende module",
        "totaal_vragen": len(quiz_questions),
        "totaal_punten": sum(q.points for q in questions),
        "vragen": quiz_questions
    }


@router.post("/modules/{module_id}/quiz/submit", tags=["Quiz"])
async def submit_quiz(module_id: str, submission: QuizSubmissionRequest) -> Dict[str, Any]:
    """Verwerk quiz inzending en geef resultaten terug"""
    try:
        if submission.module_id != module_id:
            raise HTTPException(status_code=400, detail="Module ID mismatch")
        
        attempt = quiz_service.submit_quiz_attempt(
            submission.user_id,
            submission.module_id,
            submission.answers
        )
        
        module = quiz_service.get_module_by_id(module_id)
        
        # Bepaal of gebruiker geslaagd is (80% of hoger)
        passed = attempt.score >= 80
        
        response = {
            "poging_id": f"{submission.user_id}_{module_id}_{attempt.attempt_date}",
            "module_titel": module.title if module else "Onbekende module",
            "score": attempt.score,
            "geslaagd": passed,
            "fout_beantwoorde_vragen": len(attempt.incorrect_questions),
            "totaal_vragen": len(submission.answers),
            "poging_datum": attempt.attempt_date
        }
        
        # Voeg feedback toe als er fouten zijn
        if attempt.incorrect_questions:
            response["feedback"] = {
                "bericht": "Je hebt enkele vragen fout beantwoord. Bestudeer de uitleg hieronder en probeer opnieuw.",
                "verbeteringspunten": attempt.feedback_content,
                "retry_beschikbaar": True
            }
        else:
            response["feedback"] = {
                "bericht": "Gefeliciteerd! Je hebt alle vragen correct beantwoord.",
                "retry_beschikbaar": False
            }
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fout bij verwerken van quiz")


@router.get("/modules/{module_id}/quiz/retry/{user_id}", tags=["Quiz"])
async def get_retry_quiz(module_id: str, user_id: str) -> Dict[str, Any]:
    """Haal retry quiz op met nieuwe vragen voor foute antwoorden"""
    retry_questions = quiz_service.get_retry_questions(user_id, module_id)
    
    if not retry_questions:
        return {
            "bericht": "Geen retry vragen beschikbaar",
            "reden": "Geen eerdere pogingen gevonden of alle antwoorden waren correct",
            "vragen": []
        }
    
    # Format vragen voor frontend
    quiz_questions = []
    for q in retry_questions:
        quiz_questions.append({
            "id": q.id,
            "vraag_type": q.question_type,
            "vraag_tekst": q.question_text,
            "opties": q.options,
            "moeilijkheidsgraad": q.difficulty,
            "punten": q.points
        })
    
    return {
        "module_id": module_id,
        "retry_type": "verbeterde_vragen",
        "totaal_vragen": len(quiz_questions),
        "bericht": "Deze vragen behandelen onderwerpen waar je eerder fouten maakte",
        "vragen": quiz_questions
    }


# User Progress Endpoints
@router.get("/progress/{user_id}", tags=["User Progress"])
async def get_user_progress(user_id: str) -> CourseProgressResponse:
    """Haal volledige gebruikersvoortgang op"""
    progress_data = quiz_service.get_user_progress(user_id)
    completed, total = quiz_service.calculate_course_completion(user_id)
    
    # Bereken gemiddelde score
    scores = [p.quiz_score for p in progress_data.values() if p.quiz_score is not None]
    average_score = int(sum(scores) / len(scores)) if scores else 0
    
    completion_percentage = int((completed / total) * 100) if total > 0 else 0
    
    return CourseProgressResponse(
        user_id=user_id,
        completion_percentage=completion_percentage,
        completed_modules=completed,
        total_modules=total,
        average_score=average_score,
        modules_progress=progress_data
    )


@router.get("/progress/{user_id}/statistics", tags=["User Progress"])
async def get_user_statistics(user_id: str) -> Dict[str, Any]:
    """Haal uitgebreide gebruikersstatistieken op"""
    stats = quiz_service.get_course_statistics(user_id)
    
    return {
        "gebruiker_id": user_id,
        "cursus_voortgang": {
            "voltooiingspercentage": stats["completion_percentage"],
            "voltooide_modules": stats["completed_modules"],
            "totaal_modules": stats["total_modules"],
            "gemiddelde_score": stats["average_score"]
        },
        "prestatie_metrics": {
            "sterkste_onderwerp": stats["strongest_topic"],
            "zwakste_onderwerp": stats["weakest_topic"],
            "totaal_tijd_besteed": stats["total_time_spent"],
            "totaal_pogingen": stats["total_attempts"]
        },
        "module_scores": stats["module_scores"],
        "aanbevelingen": {
            "volgende_module": "Ga door naar de volgende module" if stats["completion_percentage"] < 100 else "Cursus voltooid!",
            "focus_gebieden": [stats["weakest_topic"]] if stats["weakest_topic"] != "Geen data" else []
        }
    }


@router.get("/progress/{user_id}/modules/{module_id}", tags=["User Progress"])
async def get_module_progress(user_id: str, module_id: str) -> Dict[str, Any]:
    """Haal voortgang voor specifieke module op"""
    progress = quiz_service.get_user_progress(user_id, module_id).get(module_id)
    
    if not progress:
        raise HTTPException(status_code=404, detail="Geen voortgang gevonden voor deze module")
    
    module = quiz_service.get_module_by_id(module_id)
    needs_improvement = quiz_service.needs_improvement(user_id, module_id)
    
    response = {
        "gebruiker_id": user_id,
        "module_id": module_id,
        "module_titel": module.title if module else "Onbekende module",
        "voltooid": progress.completed,
        "quiz_score": progress.quiz_score,
        "tijd_besteed": progress.time_spent,
        "voltooiingsdatum": progress.completion_date,
        "verbetering_nodig": needs_improvement
    }
    
    # Voeg verbeteringsinhoud toe als nodig
    if needs_improvement:
        improvement_content = quiz_service.get_improvement_content(user_id, module_id)
        response["verbetering"] = {
            "reden": "Score onder 80% of module niet voltooid",
            "aanbevolen_acties": [
                "Bestudeer de module inhoud opnieuw",
                "Focus op de onderwerpen waar je fouten maakte",
                "Probeer de quiz opnieuw"
            ],
            "extra_studie_materiaal": improvement_content
        }
    
    return response


# Improvement and Remediation Endpoints
@router.get("/improvement/{user_id}/{module_id}", tags=["Improvement"])
async def get_improvement_recommendations(user_id: str, module_id: str) -> Dict[str, Any]:
    """Haal specifieke verbeteringsaanbevelingen op"""
    needs_improvement = quiz_service.needs_improvement(user_id, module_id)
    
    if not needs_improvement:
        return {
            "verbetering_nodig": False,
            "bericht": "Module succesvol voltooid - geen verbetering nodig"
        }
    
    improvement_content = quiz_service.get_improvement_content(user_id, module_id)
    module = quiz_service.get_module_by_id(module_id)
    progress = quiz_service.get_user_progress(user_id, module_id).get(module_id)
    
    return {
        "verbetering_nodig": True,
        "module_titel": module.title if module else "Onbekende module",
        "huidige_score": progress.quiz_score if progress else None,
        "doel_score": 80,
        "aanbevelingen": {
            "algemeen": [
                "Bestudeer de module inhoud grondig opnieuw",
                "Let extra op de onderwerpen waar je fouten maakte",
                "Maak aantekeningen van belangrijke concepten",
                "Probeer de quiz opnieuw na bestudering"
            ],
            "specifiek": improvement_content
        },
        "volgende_stappen": [
            "1. Bestudeer de aanbevolen content hieronder",
            "2. Ga terug naar de module inhoud",
            "3. Focus op je zwakke punten",
            "4. Probeer de quiz opnieuw"
        ]
    }


# Health check endpoint
@router.get("/health", tags=["System"])
async def course_health_check():
    """Controleer de status van de cursus service"""
    return {
        "status": "operationeel",
        "service": "cybersecurity_course",
        "modules_geladen": len(cybersecurity_course.modules),
        "totaal_quiz_vragen": sum(len(m.quiz_questions) for m in cybersecurity_course.modules),
        "versie": "1.0.0"
    }