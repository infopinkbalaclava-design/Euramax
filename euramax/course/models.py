"""
Euramax Course Data Models
Nederlandse cybersecurity cursus datamodellen
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum
from datetime import datetime
import uuid


class QuestionType(Enum):
    """Types van quiz vragen"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SCENARIO = "scenario"


class DifficultyLevel(Enum):
    """Moeilijkheidsgraden"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class QuizAnswer:
    """Een quiz antwoord optie"""
    id: str
    text: str
    is_correct: bool
    explanation: str  # Nederlandse uitleg waarom dit antwoord juist/onjuist is


@dataclass
class QuizQuestion:
    """Een quiz vraag"""
    id: str
    question: str  # Nederlandse vraag
    question_type: QuestionType
    difficulty: DifficultyLevel
    answers: List[QuizAnswer]
    explanation: str  # Uitgebreide Nederlandse uitleg
    cybersecurity_topic: str  # Bijv. "phishing", "wachtwoorden", "malware"
    scenario_context: Optional[str] = None  # Voor scenario-gebaseerde vragen


@dataclass
class CourseModule:
    """Een cursus module"""
    id: str
    title: str  # Nederlandse titel
    description: str  # Nederlandse beschrijving
    content: str  # Volledige Nederlandse content (markdown/HTML)
    cybersecurity_topics: List[str]  # Onderwerpen die behandeld worden
    difficulty: DifficultyLevel
    estimated_time_minutes: int
    quiz_questions: List[QuizQuestion]
    prerequisites: List[str] = field(default_factory=list)  # ID's van vereiste modules
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class UserQuizAttempt:
    """Een poging van een gebruiker op een quiz"""
    id: str
    user_id: str
    module_id: str
    question_id: str
    selected_answer_id: str
    is_correct: bool
    timestamp: datetime
    time_spent_seconds: int


@dataclass
class ModuleProgress:
    """Voortgang van een gebruiker in een module"""
    user_id: str
    module_id: str
    is_completed: bool
    content_viewed: bool
    quiz_score: float  # Percentage correct (0.0 - 1.0)
    quiz_attempts: List[UserQuizAttempt]
    incorrect_questions: Set[str]  # Question ID's die fout beantwoord zijn
    time_spent_minutes: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    last_accessed: datetime = field(default_factory=datetime.now)


@dataclass
class UserProgress:
    """Totale voortgang van een gebruiker"""
    user_id: str
    total_modules: int
    completed_modules: int
    overall_score: float  # Gemiddelde score over alle modules
    total_time_spent_minutes: int
    module_progress: Dict[str, ModuleProgress]  # module_id -> progress
    achievements: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)


@dataclass
class User:
    """Gebruiker in het cursus systeem"""
    id: str
    email: str
    full_name: str
    department: str
    role: str
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True


# Nederlandse cursus inhoud data
DUTCH_CYBERSECURITY_MODULES = [
    {
        "id": "phishing-basics",
        "title": "Phishing Herkennen en Voorkomen",
        "description": "Leer hoe je phishing-aanvallen kunt herkennen en jezelf kunt beschermen tegen deze veelvoorkomende cyberthreat.",
        "cybersecurity_topics": ["phishing", "email_security", "social_engineering"],
        "difficulty": DifficultyLevel.BEGINNER,
        "estimated_time_minutes": 15
    },
    {
        "id": "password-security",
        "title": "Wachtwoordbeveiliging en Authenticatie",
        "description": "Ontdek beste praktijken voor sterke wachtwoorden en tweefactorauthenticatie.",
        "cybersecurity_topics": ["passwords", "authentication", "account_security"],
        "difficulty": DifficultyLevel.BEGINNER,
        "estimated_time_minutes": 12
    },
    {
        "id": "malware-protection",
        "title": "Malware Bescherming",
        "description": "Verstaan wat malware is en hoe je je systeem kunt beschermen tegen virussen, trojans en ransomware.",
        "cybersecurity_topics": ["malware", "antivirus", "ransomware"],
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "estimated_time_minutes": 20
    },
    {
        "id": "data-protection",
        "title": "Gegevensbescherming en Privacy",
        "description": "Leer over GDPR-compliance en hoe je gevoelige gegevens veilig kunt behandelen.",
        "cybersecurity_topics": ["data_protection", "privacy", "gdpr"],
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "estimated_time_minutes": 18
    },
    {
        "id": "social-engineering",
        "title": "Social Engineering Aanvallen",
        "description": "Herken en voorkom manipulatietechnieken die cybercriminelen gebruiken.",
        "cybersecurity_topics": ["social_engineering", "manipulation", "human_factors"],
        "difficulty": DifficultyLevel.ADVANCED,
        "estimated_time_minutes": 25
    }
]