"""
Quiz Service
Handles quiz logic, scoring, and user progress tracking
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random

from euramax.course.models import (
    QuizQuestion, QuizAttempt, UserProgress, 
    CourseModule, DifficultyLevel
)
from euramax.course.content import cybersecurity_course


class QuizService:
    """Service voor het beheren van quizzes en gebruikersvoortgang"""
    
    def __init__(self):
        self.course = cybersecurity_course
        self.user_progress: Dict[str, Dict[str, UserProgress]] = {}
        self.quiz_attempts: Dict[str, List[QuizAttempt]] = {}
    
    def get_module_by_id(self, module_id: str) -> Optional[CourseModule]:
        """Haal een module op basis van ID"""
        for module in self.course.modules:
            if module.id == module_id:
                return module
        return None
    
    def get_quiz_questions(self, module_id: str, randomize: bool = True) -> List[QuizQuestion]:
        """Haal quiz vragen voor een module op"""
        module = self.get_module_by_id(module_id)
        if not module:
            return []
        
        questions = module.quiz_questions.copy()
        if randomize:
            random.shuffle(questions)
        return questions
    
    def submit_quiz_attempt(self, user_id: str, module_id: str, answers: Dict[str, int]) -> QuizAttempt:
        """Verwerk een quiz inzending en bereken de score"""
        questions = self.get_quiz_questions(module_id, randomize=False)
        
        if not questions:
            raise ValueError(f"Geen quiz vragen gevonden voor module {module_id}")
        
        # Bereken score en vind onjuiste antwoorden
        total_points = sum(q.points for q in questions)
        earned_points = 0
        incorrect_questions = []
        
        for question in questions:
            user_answer = answers.get(question.id)
            if user_answer is not None and user_answer == question.correct_answer:
                earned_points += question.points
            else:
                incorrect_questions.append(question.id)
        
        # Bereken percentage score
        score_percentage = int((earned_points / total_points) * 100) if total_points > 0 else 0
        
        # Genereer feedback voor onjuiste antwoorden
        feedback_content = []
        for question_id in incorrect_questions:
            question = next((q for q in questions if q.id == question_id), None)
            if question:
                feedback_content.append(f"**Vraag**: {question.question_text}")
                feedback_content.append(f"**Correct antwoord**: {question.options[question.correct_answer]}")
                feedback_content.append(f"**Uitleg**: {question.explanation}")
                feedback_content.append("---")
        
        # Maak quiz attempt object
        attempt = QuizAttempt(
            user_id=user_id,
            module_id=module_id,
            answers=answers,
            score=score_percentage,
            incorrect_questions=incorrect_questions,
            feedback_content=feedback_content,
            attempt_date=datetime.now().isoformat()
        )
        
        # Sla poging op
        if user_id not in self.quiz_attempts:
            self.quiz_attempts[user_id] = []
        self.quiz_attempts[user_id].append(attempt)
        
        # Update gebruikersvoortgang
        self.update_user_progress(user_id, module_id, score_percentage, incorrect_questions)
        
        return attempt
    
    def update_user_progress(self, user_id: str, module_id: str, score: int, incorrect_answers: List[str]):
        """Update de voortgang van een gebruiker"""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        
        # Bepaal of module voltooid is (score >= 80%)
        completed = score >= 80
        
        # Bereken tijd besteed (simulatie - zou in echte app getrackt worden)
        module = self.get_module_by_id(module_id)
        estimated_time = module.estimated_duration if module else 0
        
        progress = UserProgress(
            user_id=user_id,
            module_id=module_id,
            completed=completed,
            quiz_score=score,
            incorrect_answers=incorrect_answers,
            time_spent=estimated_time,
            completion_date=datetime.now().isoformat() if completed else None
        )
        
        self.user_progress[user_id][module_id] = progress
    
    def get_user_progress(self, user_id: str, module_id: Optional[str] = None) -> Dict[str, UserProgress]:
        """Haal gebruikersvoortgang op"""
        user_data = self.user_progress.get(user_id, {})
        
        if module_id:
            return {module_id: user_data.get(module_id)} if module_id in user_data else {}
        
        return user_data
    
    def get_retry_questions(self, user_id: str, module_id: str) -> List[QuizQuestion]:
        """Haal nieuwe vragen voor retry na onjuiste antwoorden"""
        # Haal de laatste poging op
        user_attempts = self.quiz_attempts.get(user_id, [])
        module_attempts = [a for a in user_attempts if a.module_id == module_id]
        
        if not module_attempts:
            return []
        
        last_attempt = module_attempts[-1]
        
        # Vind alle vragen voor deze module
        all_questions = self.get_quiz_questions(module_id, randomize=False)
        
        # Genereer nieuwe vragen voor onderwerpen waar fouten gemaakt zijn
        retry_questions = []
        
        for incorrect_q_id in last_attempt.incorrect_questions:
            original_question = next((q for q in all_questions if q.id == incorrect_q_id), None)
            if original_question:
                # Genereer vergelijkbare vraag (in echte app zou dit een database query zijn)
                retry_question = self._generate_similar_question(original_question)
                if retry_question:
                    retry_questions.append(retry_question)
        
        return retry_questions
    
    def _generate_similar_question(self, original: QuizQuestion) -> Optional[QuizQuestion]:
        """Genereer een vergelijkbare vraag voor retry (vereenvoudigde implementatie)"""
        # In een echte implementatie zou dit slimmere vraag generatie zijn
        # Voor nu, geef een aangepaste versie van de originele vraag
        
        retry_questions_map = {
            "phishing_q1": QuizQuestion(
                id="phishing_q1_retry",
                module_id=original.module_id,
                question_type=original.question_type,
                question_text="Een collega ontvangt een verdachte e-mail die om wachtwoord verificatie vraagt. Wat raad je aan?",
                options=[
                    "Direct het wachtwoord verstrekken als het dringend lijkt",
                    "Eerst de afzender e-mailen om te bevestigen",
                    "Het bedrijf contacteren via een bekend telefoonnummer",
                    "De e-mail delen met andere collega's voor advies"
                ],
                correct_answer=2,
                explanation="Contacteren via een bekend nummer is de veiligste manier om de legitimiteit te verifiëren.",
                difficulty=original.difficulty,
                points=original.points
            ),
            "password_q2": QuizQuestion(
                id="password_q2_retry", 
                module_id=original.module_id,
                question_type=original.question_type,
                question_text="Je wilt tijd besparen door hetzelfde complexe wachtwoord te gebruiken voor je werk e-mail en bankaccount. Is dit een goede strategie?",
                options=["Ja, als het wachtwoord maar complex genoeg is", "Nee, elk account moet een uniek wachtwoord hebben"],
                correct_answer=1,
                explanation="Elk account heeft een uniek wachtwoord nodig. Als één account gehackt wordt, blijven andere veilig.",
                difficulty=original.difficulty,
                points=original.points
            )
        }
        
        return retry_questions_map.get(original.id)
    
    def calculate_course_completion(self, user_id: str) -> Tuple[int, int]:
        """Bereken algehele cursusvoortgang (voltooid, totaal)"""
        user_data = self.user_progress.get(user_id, {})
        total_modules = len(self.course.modules)
        completed_modules = sum(1 for progress in user_data.values() if progress.completed)
        
        return completed_modules, total_modules
    
    def get_course_statistics(self, user_id: str) -> Dict:
        """Haal uitgebreide cursusstatistieken op voor een gebruiker"""
        user_data = self.user_progress.get(user_id, {})
        user_attempts = self.quiz_attempts.get(user_id, [])
        
        completed, total = self.calculate_course_completion(user_id)
        completion_percentage = int((completed / total) * 100) if total > 0 else 0
        
        # Bereken gemiddelde score
        scores = [progress.quiz_score for progress in user_data.values() if progress.quiz_score is not None]
        average_score = int(sum(scores) / len(scores)) if scores else 0
        
        # Bereken totale tijd besteed
        total_time = sum(progress.time_spent for progress in user_data.values())
        
        # Vind sterkste en zwakste onderwerpen
        module_scores = {}
        for module_id, progress in user_data.items():
            if progress.quiz_score is not None:
                module = self.get_module_by_id(module_id)
                if module:
                    module_scores[module.title] = progress.quiz_score
        
        strongest_topic = max(module_scores.items(), key=lambda x: x[1])[0] if module_scores else "Geen data"
        weakest_topic = min(module_scores.items(), key=lambda x: x[1])[0] if module_scores else "Geen data"
        
        return {
            "completion_percentage": completion_percentage,
            "completed_modules": completed,
            "total_modules": total,
            "average_score": average_score,
            "total_time_spent": total_time,
            "total_attempts": len(user_attempts),
            "strongest_topic": strongest_topic,
            "weakest_topic": weakest_topic,
            "module_scores": module_scores
        }
    
    def needs_improvement(self, user_id: str, module_id: str) -> bool:
        """Controleer of een gebruiker verbetering nodig heeft voor een module"""
        progress = self.get_user_progress(user_id, module_id).get(module_id)
        if not progress:
            return True
        
        return not progress.completed or (progress.quiz_score and progress.quiz_score < 80)
    
    def get_improvement_content(self, user_id: str, module_id: str) -> List[str]:
        """Haal specifieke inhoud op voor verbetering gebaseerd op fouten"""
        progress = self.get_user_progress(user_id, module_id).get(module_id)
        if not progress or not progress.incorrect_answers:
            return []
        
        module = self.get_module_by_id(module_id)
        if not module:
            return []
        
        # Map foute antwoorden naar relevante content secties
        improvement_content = []
        
        # Voor elke foute vraag, voeg relevante cursusinhoud toe
        for question_id in progress.incorrect_answers:
            question = next((q for q in module.quiz_questions if q.id == question_id), None)
            if question:
                # Voeg uitleg van de vraag toe
                improvement_content.append(f"**Onderwerp**: {question.question_text}")
                improvement_content.append(f"**Uitleg**: {question.explanation}")
                
                # Voeg relevante module content toe (vereenvoudigd)
                if "phishing" in question_id:
                    improvement_content.extend([
                        "**Extra Study Materiaal:**",
                        "Review de sectie over 'Rode Vlaggen van Phishing E-mails'",
                        "Oefen met het herkennen van verdachte URL's",
                        "Bestudeer de 'Hoe Te Reageren' sectie opnieuw"
                    ])
                elif "password" in question_id:
                    improvement_content.extend([
                        "**Extra Study Materiaal:**",
                        "Herbekijk 'Kenmerken van Sterke Wachtwoorden'",
                        "Leer meer over wachtwoordmanagers",
                        "Bestudeer tweefactorauthenticatie opties"
                    ])
                
                improvement_content.append("---")
        
        return improvement_content


# Globale quiz service instantie
quiz_service = QuizService()