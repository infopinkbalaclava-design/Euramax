"""
Course Content Model
Nederlandse cybersecurity cursus inhoud definities
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class DifficultyLevel(str, Enum):
    """Moeilijkheidsgraad van cursusmodules"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"


class QuestionType(str, Enum):
    """Type quiz vragen"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SCENARIO = "scenario"


class CourseModule(BaseModel):
    """Een enkele cursusmodule"""
    id: str = Field(..., description="Unieke module identifier")
    title: str = Field(..., description="Nederlandse titel van de module")
    description: str = Field(..., description="Beschrijving van de module")
    difficulty: DifficultyLevel = Field(..., description="Moeilijkheidsgraad")
    estimated_duration: int = Field(..., description="Geschatte duur in minuten")
    content: List[str] = Field(..., description="Cursusinhoud als lijst van secties")
    learning_objectives: List[str] = Field(..., description="Leerdoelen")
    quiz_questions: List['QuizQuestion'] = Field(default=[], description="Quiz vragen voor deze module")


class QuizQuestion(BaseModel):
    """Een quiz vraag met antwoordmogelijkheden"""
    id: str = Field(..., description="Unieke vraag identifier")
    module_id: str = Field(..., description="Module waartoe deze vraag behoort")
    question_type: QuestionType = Field(..., description="Type vraag")
    question_text: str = Field(..., description="De feitelijke vraag in Nederlands")
    options: List[str] = Field(..., description="Antwoordopties")
    correct_answer: int = Field(..., description="Index van het juiste antwoord")
    explanation: str = Field(..., description="Uitleg bij het juiste antwoord")
    difficulty: DifficultyLevel = Field(..., description="Moeilijkheidsgraad van deze vraag")
    points: int = Field(default=1, description="Punten voor deze vraag")


class UserProgress(BaseModel):
    """Voortgang van een gebruiker"""
    user_id: str = Field(..., description="Gebruiker identifier")
    module_id: str = Field(..., description="Module identifier")
    completed: bool = Field(default=False, description="Of de module voltooid is")
    quiz_score: Optional[int] = Field(None, description="Quiz score percentage")
    incorrect_answers: List[str] = Field(default=[], description="IDs van fout beantwoorde vragen")
    time_spent: int = Field(default=0, description="Tijd besteed in minuten")
    completion_date: Optional[str] = Field(None, description="Datum van voltooiing")


class QuizAttempt(BaseModel):
    """Een quiz poging van een gebruiker"""
    user_id: str = Field(..., description="Gebruiker identifier")
    module_id: str = Field(..., description="Module identifier")
    answers: Dict[str, int] = Field(..., description="Antwoorden: question_id -> answer_index")
    score: int = Field(..., description="Behaalde score percentage")
    incorrect_questions: List[str] = Field(..., description="IDs van fout beantwoorde vragen")
    feedback_content: List[str] = Field(..., description="Feedback inhoud voor onjuiste antwoorden")
    attempt_date: str = Field(..., description="Datum van de poging")


class CourseStructure(BaseModel):
    """Complete cursusstructuur"""
    course_title: str = Field(..., description="Titel van de volledige cursus")
    course_description: str = Field(..., description="Beschrijving van de cursus")
    modules: List[CourseModule] = Field(..., description="Alle cursusmodules")
    total_duration: int = Field(..., description="Totale cursusduur in minuten")
    completion_certificate: bool = Field(default=True, description="Of er een certificaat wordt uitgegeven")


# Fix forward reference
CourseModule.model_rebuild()