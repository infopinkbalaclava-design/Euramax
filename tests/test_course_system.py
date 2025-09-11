"""
Test cases voor Euramax Course System
Nederlandse unit tests voor cybersecurity cursus functionaliteit
"""

import pytest
import asyncio
from datetime import datetime
from euramax.course.service import CourseService
from euramax.course.models import (
    QuestionType, DifficultyLevel, CourseModule, UserProgress, ModuleProgress
)


class TestCourseService:
    """Test cases voor course service"""
    
    @pytest.fixture
    async def course_service(self):
        service = CourseService()
        await service.initialize()
        return service
    
    @pytest.mark.asyncio
    async def test_service_initialization(self, course_service):
        """Test initialisatie van course service"""
        assert course_service.is_initialized == True
        assert len(course_service.modules) == 5
        assert len(course_service.users) == 1  # Demo user
        assert "demo_user" in course_service.users
        
    @pytest.mark.asyncio
    async def test_get_all_modules(self, course_service):
        """Test ophalen van alle modules"""
        modules = await course_service.get_all_modules()
        
        assert len(modules) == 5
        
        # Check module structure
        for module in modules:
            assert hasattr(module, 'id')
            assert hasattr(module, 'title')
            assert hasattr(module, 'description')
            assert hasattr(module, 'content')
            assert hasattr(module, 'quiz_questions')
            assert len(module.quiz_questions) > 0
            
        # Check specific modules exist
        module_ids = [m.id for m in modules]
        expected_modules = [
            'phishing-basics', 'password-security', 'malware-protection',
            'data-protection', 'social-engineering'
        ]
        for expected_id in expected_modules:
            assert expected_id in module_ids
    
    @pytest.mark.asyncio
    async def test_get_specific_module(self, course_service):
        """Test ophalen van specifieke module"""
        module = await course_service.get_module('phishing-basics')
        
        assert module is not None
        assert module.id == 'phishing-basics'
        assert 'Phishing' in module.title
        assert module.difficulty == DifficultyLevel.BEGINNER
        assert len(module.quiz_questions) == 3
        assert 'phishing' in module.cybersecurity_topics
        
        # Test non-existent module
        non_existent = await course_service.get_module('non-existent')
        assert non_existent is None
    
    @pytest.mark.asyncio
    async def test_start_module(self, course_service):
        """Test starten van een module"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        success = await course_service.start_module(user_id, module_id)
        assert success == True
        
        # Check user progress was created
        progress = await course_service.get_user_progress(user_id)
        assert progress is not None
        assert module_id in progress.module_progress
        
        module_progress = progress.module_progress[module_id]
        assert module_progress.user_id == user_id
        assert module_progress.module_id == module_id
        assert module_progress.is_completed == False
        assert module_progress.content_viewed == False
        assert module_progress.quiz_score == 0.0
        
    @pytest.mark.asyncio
    async def test_complete_module_content(self, course_service):
        """Test voltooien van module content"""
        user_id = "test_user"
        module_id = "phishing-basics"
        time_spent = 15
        
        # Start module first
        await course_service.start_module(user_id, module_id)
        
        # Complete content
        success = await course_service.complete_module_content(user_id, module_id, time_spent)
        assert success == True
        
        # Check progress updated
        progress = await course_service.get_user_progress(user_id)
        module_progress = progress.module_progress[module_id]
        
        assert module_progress.content_viewed == True
        assert module_progress.time_spent_minutes == time_spent
        assert progress.total_time_spent_minutes == time_spent
        
    @pytest.mark.asyncio
    async def test_quiz_questions(self, course_service):
        """Test ophalen van quiz vragen"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        await course_service.start_module(user_id, module_id)
        
        # Get quiz questions
        questions = await course_service.get_quiz_questions(user_id, module_id)
        
        assert len(questions) > 0
        assert len(questions) <= 3  # Should be shuffled
        
        for question in questions:
            assert hasattr(question, 'id')
            assert hasattr(question, 'question')
            assert hasattr(question, 'question_type')
            assert hasattr(question, 'answers')
            assert len(question.answers) >= 2
            
            # Check answer structure
            for answer in question.answers:
                assert hasattr(answer, 'id')
                assert hasattr(answer, 'text')
                assert hasattr(answer, 'is_correct')
                assert hasattr(answer, 'explanation')
    
    @pytest.mark.asyncio
    async def test_submit_quiz_answer_correct(self, course_service):
        """Test correct quiz antwoord"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        await course_service.start_module(user_id, module_id)
        
        # Get first question
        questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct=False)
        question = questions[0]
        
        # Find correct answer
        correct_answer = next(a for a in question.answers if a.is_correct)
        
        # Submit correct answer
        result = await course_service.submit_quiz_answer(
            user_id, module_id, question.id, correct_answer.id, 30
        )
        
        assert result["is_correct"] == True
        assert "explanation" in result
        assert result["correct_answer"] is None  # Only shown for incorrect answers
        
        # Check progress updated
        progress = await course_service.get_user_progress(user_id)
        module_progress = progress.module_progress[module_id]
        assert len(module_progress.quiz_attempts) == 1
        assert question.id not in module_progress.incorrect_questions
        
    @pytest.mark.asyncio
    async def test_submit_quiz_answer_incorrect(self, course_service):
        """Test incorrect quiz antwoord"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        await course_service.start_module(user_id, module_id)
        
        # Get first question
        questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct=False)
        question = questions[0]
        
        # Find incorrect answer
        incorrect_answer = next(a for a in question.answers if not a.is_correct)
        correct_answer = next(a for a in question.answers if a.is_correct)
        
        # Submit incorrect answer
        result = await course_service.submit_quiz_answer(
            user_id, module_id, question.id, incorrect_answer.id, 30
        )
        
        assert result["is_correct"] == False
        assert "explanation" in result
        assert result["correct_answer"] == correct_answer.text
        
        # Check progress updated
        progress = await course_service.get_user_progress(user_id)
        module_progress = progress.module_progress[module_id]
        assert len(module_progress.quiz_attempts) == 1
        assert question.id in module_progress.incorrect_questions
        
    @pytest.mark.asyncio
    async def test_quiz_score_calculation(self, course_service):
        """Test quiz score berekening"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        await course_service.start_module(user_id, module_id)
        
        # Get all questions
        questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct=False)
        
        # Answer 2 out of 3 correctly
        for i, question in enumerate(questions):
            if i < 2:
                # Correct answer
                correct_answer = next(a for a in question.answers if a.is_correct)
                await course_service.submit_quiz_answer(
                    user_id, module_id, question.id, correct_answer.id, 30
                )
            else:
                # Incorrect answer
                incorrect_answer = next(a for a in question.answers if not a.is_correct)
                await course_service.submit_quiz_answer(
                    user_id, module_id, question.id, incorrect_answer.id, 30
                )
        
        # Check score
        progress = await course_service.get_user_progress(user_id)
        module_progress = progress.module_progress[module_id]
        
        expected_score = 2.0 / 3.0  # 2 out of 3 correct
        assert abs(module_progress.quiz_score - expected_score) < 0.01
        
    @pytest.mark.asyncio
    async def test_module_completion(self, course_service):
        """Test module voltooiing"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        await course_service.start_module(user_id, module_id)
        
        # Complete content
        await course_service.complete_module_content(user_id, module_id, 15)
        
        # Answer all questions correctly (80%+ needed for completion)
        questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct=False)
        
        for question in questions:
            correct_answer = next(a for a in question.answers if a.is_correct)
            await course_service.submit_quiz_answer(
                user_id, module_id, question.id, correct_answer.id, 30
            )
        
        # Check module is completed
        progress = await course_service.get_user_progress(user_id)
        module_progress = progress.module_progress[module_id]
        
        assert module_progress.is_completed == True
        assert module_progress.completed_at is not None
        assert progress.completed_modules == 1
        assert module_progress.quiz_score == 1.0  # 100% correct
        
    @pytest.mark.asyncio
    async def test_incorrect_questions_review(self, course_service):
        """Test review van incorrecte vragen"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        await course_service.start_module(user_id, module_id)
        
        # Get questions and answer some incorrectly
        questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct=False)
        incorrect_questions = []
        
        for i, question in enumerate(questions):
            if i < 2:
                # Answer incorrectly
                incorrect_answer = next(a for a in question.answers if not a.is_correct)
                await course_service.submit_quiz_answer(
                    user_id, module_id, question.id, incorrect_answer.id, 30
                )
                incorrect_questions.append(question.id)
            else:
                # Answer correctly
                correct_answer = next(a for a in question.answers if a.is_correct)
                await course_service.submit_quiz_answer(
                    user_id, module_id, question.id, correct_answer.id, 30
                )
        
        # Get incorrect questions for review
        review_questions = await course_service.get_incorrect_questions(user_id, module_id)
        
        assert len(review_questions) == 2
        review_question_ids = [q.id for q in review_questions]
        for incorrect_id in incorrect_questions:
            assert incorrect_id in review_question_ids
            
    @pytest.mark.asyncio
    async def test_smart_question_selection(self, course_service):
        """Test slimme vraag selectie (exclude correct answers)"""
        user_id = "test_user"
        module_id = "phishing-basics"
        
        # Start module
        await course_service.start_module(user_id, module_id)
        
        # Get all questions first
        all_questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct=False)
        
        # Answer first question correctly
        first_question = all_questions[0]
        correct_answer = next(a for a in first_question.answers if a.is_correct)
        await course_service.submit_quiz_answer(
            user_id, module_id, first_question.id, correct_answer.id, 30
        )
        
        # Get questions with exclude_correct=True
        remaining_questions = await course_service.get_quiz_questions(user_id, module_id, exclude_correct=True)
        
        # Should have fewer questions now
        assert len(remaining_questions) < len(all_questions)
        
        # First question should not be in remaining questions
        remaining_ids = [q.id for q in remaining_questions]
        assert first_question.id not in remaining_ids
        
    @pytest.mark.asyncio
    async def test_overall_progress_calculation(self, course_service):
        """Test overall voortgang berekening"""
        user_id = "test_user"
        
        # Complete first module
        module1 = "phishing-basics"
        await course_service.start_module(user_id, module1)
        await course_service.complete_module_content(user_id, module1, 15)
        
        questions = await course_service.get_quiz_questions(user_id, module1, exclude_correct=False)
        for question in questions:
            correct_answer = next(a for a in question.answers if a.is_correct)
            await course_service.submit_quiz_answer(
                user_id, module1, question.id, correct_answer.id, 30
            )
            
        # Start second module but don't complete
        module2 = "password-security"
        await course_service.start_module(user_id, module2)
        
        # Check progress
        progress = await course_service.get_user_progress(user_id)
        
        assert progress.total_modules == 5
        assert progress.completed_modules == 1
        completion_percentage = (progress.completed_modules / progress.total_modules * 100) if progress.total_modules > 0 else 0
        assert completion_percentage == 20.0  # 1/5 * 100
        assert progress.overall_score > 0  # Should have some score from completed module
        
    @pytest.mark.asyncio
    async def test_health_check(self, course_service):
        """Test health check van service"""
        health = await course_service.health_check()
        assert health == "operationeel"
        
        # Test before initialization
        new_service = CourseService()
        health = await new_service.health_check()
        assert health == "not_initialized"


class TestCourseModels:
    """Test cases voor course models"""
    
    def test_difficulty_levels(self):
        """Test difficulty level enum"""
        assert DifficultyLevel.BEGINNER.value == "beginner"
        assert DifficultyLevel.INTERMEDIATE.value == "intermediate"
        assert DifficultyLevel.ADVANCED.value == "advanced"
        
    def test_question_types(self):
        """Test question type enum"""
        assert QuestionType.MULTIPLE_CHOICE.value == "multiple_choice"
        assert QuestionType.TRUE_FALSE.value == "true_false"
        assert QuestionType.SCENARIO.value == "scenario"
        
    def test_dutch_module_data(self):
        """Test Nederlandse module data"""
        from euramax.course.models import DUTCH_CYBERSECURITY_MODULES
        
        assert len(DUTCH_CYBERSECURITY_MODULES) == 5
        
        for module_data in DUTCH_CYBERSECURITY_MODULES:
            assert 'id' in module_data
            assert 'title' in module_data
            assert 'description' in module_data
            assert 'cybersecurity_topics' in module_data
            assert 'difficulty' in module_data
            assert 'estimated_time_minutes' in module_data
            
            # Check Dutch content
            assert isinstance(module_data['title'], str)
            assert len(module_data['title']) > 0
            assert isinstance(module_data['description'], str)
            assert len(module_data['description']) > 0


# pytest configuratie voor asyncio tests
pytest_plugins = ('pytest_asyncio',)


if __name__ == "__main__":
    # Run tests als script wordt uitgevoerd
    pytest.main([__file__, "-v"])