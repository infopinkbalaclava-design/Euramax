"""
Euramax Course API Routes
Nederlandse cybersecurity cursus API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime

from euramax.course.service import CourseService
from euramax.course.models import CourseModule, UserProgress, QuizQuestion


logger = structlog.get_logger()
router = APIRouter()


# Dependency to get course service from app state
async def get_course_service(request: Request) -> CourseService:
    """Get course service from app state"""
    if not hasattr(request.app.state, 'course_service'):
        raise HTTPException(
            status_code=503,
            detail="Course service niet beschikbaar"
        )
    return request.app.state.course_service


@router.get("/modules", response_model=List[Dict[str, Any]])
async def get_all_modules(
    course_service: CourseService = Depends(get_course_service)
) -> List[Dict[str, Any]]:
    """Krijg alle beschikbare cursus modules"""
    try:
        modules = await course_service.get_all_modules()
        
        return [
            {
                "id": module.id,
                "title": module.title,
                "description": module.description,
                "cybersecurity_topics": module.cybersecurity_topics,
                "difficulty": module.difficulty.value,
                "estimated_time_minutes": module.estimated_time_minutes,
                "quiz_question_count": len(module.quiz_questions),
                "prerequisites": module.prerequisites,
                "created_at": module.created_at.isoformat(),
                "updated_at": module.updated_at.isoformat()
            }
            for module in modules
        ]
    except Exception as e:
        logger.error("Fout bij ophalen modules", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan modules niet ophalen"
        )


@router.get("/modules/{module_id}", response_model=Dict[str, Any])
async def get_module(
    module_id: str,
    course_service: CourseService = Depends(get_course_service)
) -> Dict[str, Any]:
    """Krijg een specifieke cursus module"""
    try:
        module = await course_service.get_module(module_id)
        
        if not module:
            raise HTTPException(
                status_code=404,
                detail=f"Module '{module_id}' niet gevonden"
            )
        
        return {
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "content": module.content,
            "cybersecurity_topics": module.cybersecurity_topics,
            "difficulty": module.difficulty.value,
            "estimated_time_minutes": module.estimated_time_minutes,
            "prerequisites": module.prerequisites,
            "quiz_question_count": len(module.quiz_questions),
            "created_at": module.created_at.isoformat(),
            "updated_at": module.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Fout bij ophalen module", module_id=module_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan module niet ophalen"
        )


@router.get("/users/{user_id}/progress", response_model=Dict[str, Any])
async def get_user_progress(
    user_id: str,
    course_service: CourseService = Depends(get_course_service)
) -> Dict[str, Any]:
    """Krijg voortgang van een gebruiker"""
    try:
        progress = await course_service.get_user_progress(user_id)
        
        if not progress:
            raise HTTPException(
                status_code=404,
                detail=f"Voortgang voor gebruiker '{user_id}' niet gevonden"
            )
        
        # Convert module progress to serializable format
        module_progress_data = {}
        for module_id, module_progress in progress.module_progress.items():
            module_progress_data[module_id] = {
                "is_completed": module_progress.is_completed,
                "content_viewed": module_progress.content_viewed,
                "quiz_score": module_progress.quiz_score,
                "incorrect_questions_count": len(module_progress.incorrect_questions),
                "time_spent_minutes": module_progress.time_spent_minutes,
                "started_at": module_progress.started_at.isoformat(),
                "completed_at": module_progress.completed_at.isoformat() if module_progress.completed_at else None,
                "last_accessed": module_progress.last_accessed.isoformat(),
                "total_attempts": len(module_progress.quiz_attempts)
            }
        
        return {
            "user_id": progress.user_id,
            "total_modules": progress.total_modules,
            "completed_modules": progress.completed_modules,
            "completion_percentage": (progress.completed_modules / progress.total_modules * 100) if progress.total_modules > 0 else 0,
            "overall_score": progress.overall_score,
            "total_time_spent_minutes": progress.total_time_spent_minutes,
            "achievements": progress.achievements,
            "started_at": progress.started_at.isoformat(),
            "last_activity": progress.last_activity.isoformat(),
            "module_progress": module_progress_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Fout bij ophalen gebruikersvoortgang", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan gebruikersvoortgang niet ophalen"
        )


@router.post("/users/{user_id}/modules/{module_id}/start")
async def start_module(
    user_id: str,
    module_id: str,
    course_service: CourseService = Depends(get_course_service)
) -> Dict[str, Any]:
    """Start een module voor een gebruiker"""
    try:
        success = await course_service.start_module(user_id, module_id)
        
        if not success:
            raise HTTPException(
                status_code=400,
                detail=f"Kan module '{module_id}' niet starten"
            )
        
        return {
            "status": "success",
            "message": f"Module '{module_id}' gestart voor gebruiker '{user_id}'",
            "started_at": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Fout bij starten module", user_id=user_id, module_id=module_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan module niet starten"
        )


@router.post("/users/{user_id}/modules/{module_id}/complete-content")
async def complete_module_content(
    user_id: str,
    module_id: str,
    request_data: Dict[str, int],
    course_service: CourseService = Depends(get_course_service)
) -> Dict[str, Any]:
    """Markeer module content als voltooid"""
    try:
        time_spent = request_data.get("time_spent_minutes", 0)
        
        success = await course_service.complete_module_content(user_id, module_id, time_spent)
        
        if not success:
            raise HTTPException(
                status_code=400,
                detail=f"Kan module content niet voltooien"
            )
        
        return {
            "status": "success",
            "message": "Module content voltooid",
            "time_spent_minutes": time_spent
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Fout bij voltooien module content", user_id=user_id, module_id=module_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan module content niet voltooien"
        )


@router.get("/users/{user_id}/modules/{module_id}/quiz", response_model=List[Dict[str, Any]])
async def get_quiz_questions(
    user_id: str,
    module_id: str,
    exclude_correct: bool = True,
    course_service: CourseService = Depends(get_course_service)
) -> List[Dict[str, Any]]:
    """Krijg quiz vragen voor een module"""
    try:
        questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct)
        
        return [
            {
                "id": question.id,
                "question": question.question,
                "question_type": question.question_type.value,
                "difficulty": question.difficulty.value,
                "cybersecurity_topic": question.cybersecurity_topic,
                "scenario_context": question.scenario_context,
                "answers": [
                    {
                        "id": answer.id,
                        "text": answer.text
                        # Note: is_correct and explanation are not included for security
                    }
                    for answer in question.answers
                ]
            }
            for question in questions
        ]
    except Exception as e:
        logger.error("Fout bij ophalen quiz vragen", user_id=user_id, module_id=module_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan quiz vragen niet ophalen"
        )


@router.post("/users/{user_id}/modules/{module_id}/quiz/submit")
async def submit_quiz_answer(
    user_id: str,
    module_id: str,
    answer_data: Dict[str, Any],
    course_service: CourseService = Depends(get_course_service)
) -> Dict[str, Any]:
    """Submit een quiz antwoord"""
    try:
        question_id = answer_data.get("question_id")
        selected_answer_id = answer_data.get("selected_answer_id")
        time_spent = answer_data.get("time_spent_seconds", 0)
        
        if not question_id or not selected_answer_id:
            raise HTTPException(
                status_code=400,
                detail="question_id en selected_answer_id zijn verplicht"
            )
        
        result = await course_service.submit_quiz_answer(
            user_id, module_id, question_id, selected_answer_id, time_spent
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return {
            "status": "success",
            "is_correct": result["is_correct"],
            "explanation": result["explanation"],
            "correct_answer": result.get("correct_answer"),
            "question_explanation": result["question_explanation"],
            "submitted_at": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Fout bij submit quiz antwoord", user_id=user_id, module_id=module_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan quiz antwoord niet verwerken"
        )


@router.get("/users/{user_id}/modules/{module_id}/review", response_model=List[Dict[str, Any]])
async def get_incorrect_questions_for_review(
    user_id: str,
    module_id: str,
    course_service: CourseService = Depends(get_course_service)
) -> List[Dict[str, Any]]:
    """Krijg incorrect beantwoorde vragen voor review"""
    try:
        questions = await course_service.get_incorrect_questions(user_id, module_id)
        
        return [
            {
                "id": question.id,
                "question": question.question,
                "question_type": question.question_type.value,
                "difficulty": question.difficulty.value,
                "cybersecurity_topic": question.cybersecurity_topic,
                "scenario_context": question.scenario_context,
                "explanation": question.explanation,
                "answers": [
                    {
                        "id": answer.id,
                        "text": answer.text,
                        "is_correct": answer.is_correct,
                        "explanation": answer.explanation
                    }
                    for answer in question.answers
                ]
            }
            for question in questions
        ]
    except Exception as e:
        logger.error("Fout bij ophalen review vragen", user_id=user_id, module_id=module_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan review vragen niet ophalen"
        )


@router.get("/statistics", response_model=Dict[str, Any])
async def get_course_statistics(
    course_service: CourseService = Depends(get_course_service)
) -> Dict[str, Any]:
    """Krijg algemene cursus statistieken"""
    try:
        modules = await course_service.get_all_modules()
        
        # Calculate statistics
        total_modules = len(modules)
        total_questions = sum(len(module.quiz_questions) for module in modules)
        
        difficulty_counts = {}
        topic_counts = {}
        
        for module in modules:
            # Count by difficulty
            difficulty = module.difficulty.value
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            
            # Count by topics
            for topic in module.cybersecurity_topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # User statistics
        total_users = len(course_service.users)
        active_users = len(course_service.user_progress)
        
        return {
            "course_overview": {
                "total_modules": total_modules,
                "total_questions": total_questions,
                "total_users": total_users,
                "active_users": active_users
            },
            "module_distribution": {
                "by_difficulty": difficulty_counts,
                "by_topic": topic_counts
            },
            "service_status": {
                "is_initialized": course_service.is_initialized,
                "health": await course_service.health_check()
            }
        }
    except Exception as e:
        logger.error("Fout bij ophalen cursus statistieken", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Kan cursus statistieken niet ophalen"
        )