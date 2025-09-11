#!/usr/bin/env python3
"""
Simple test server for the cybersecurity course
Run this to test the course web interface
"""

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from euramax.course.content import cybersecurity_course
from euramax.course.quiz_service import quiz_service


class CourseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/v1/course/':
            self.send_course_overview()
        elif parsed_path.path.startswith('/api/v1/course/modules/') and parsed_path.path.endswith('/quiz'):
            module_id = parsed_path.path.split('/')[-2]
            self.send_quiz_questions(module_id)
        elif parsed_path.path.startswith('/api/v1/course/modules/'):
            module_id = parsed_path.path.split('/')[-1]
            self.send_module_details(module_id)
        elif parsed_path.path.startswith('/api/v1/course/progress/'):
            user_id = parsed_path.path.split('/')[-1]
            self.send_user_progress(user_id)
        else:
            # Serve static files
            super().do_GET()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path.endswith('/quiz/submit'):
            module_id = parsed_path.path.split('/')[-3]
            self.handle_quiz_submission(module_id)
        else:
            self.send_error(404)
    
    def send_json_response(self, data):
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(response.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def send_course_overview(self):
        data = {
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
        self.send_json_response(data)
    
    def send_module_details(self, module_id):
        module = quiz_service.get_module_by_id(module_id)
        if not module:
            self.send_error(404)
            return
        
        data = {
            "id": module.id,
            "titel": module.title,
            "beschrijving": module.description,
            "moeilijkheidsgraad": module.difficulty,
            "geschatte_duur": module.estimated_duration,
            "inhoud": module.content,
            "leerdoelen": module.learning_objectives,
            "aantal_quiz_vragen": len(module.quiz_questions)
        }
        self.send_json_response(data)
    
    def send_quiz_questions(self, module_id):
        questions = quiz_service.get_quiz_questions(module_id, randomize=True)
        if not questions:
            self.send_error(404)
            return
        
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
        data = {
            "module_id": module_id,
            "module_titel": module.title if module else "Onbekende module",
            "totaal_vragen": len(quiz_questions),
            "totaal_punten": sum(q.points for q in questions),
            "vragen": quiz_questions
        }
        self.send_json_response(data)
    
    def handle_quiz_submission(self, module_id):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            submission = json.loads(post_data.decode('utf-8'))
            
            attempt = quiz_service.submit_quiz_attempt(
                submission['user_id'],
                submission['module_id'],
                submission['answers']
            )
            
            module = quiz_service.get_module_by_id(module_id)
            passed = attempt.score >= 80
            
            response = {
                "poging_id": f"{submission['user_id']}_{module_id}_{attempt.attempt_date}",
                "module_titel": module.title if module else "Onbekende module",
                "score": attempt.score,
                "geslaagd": passed,
                "fout_beantwoorde_vragen": len(attempt.incorrect_questions),
                "totaal_vragen": len(submission['answers']),
                "poging_datum": attempt.attempt_date
            }
            
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
            
            self.send_json_response(response)
            
        except Exception as e:
            print(f"Error processing quiz submission: {e}")
            self.send_error(500)
    
    def send_user_progress(self, user_id):
        progress_data = quiz_service.get_user_progress(user_id)
        completed, total = quiz_service.calculate_course_completion(user_id)
        
        scores = [p.quiz_score for p in progress_data.values() if p.quiz_score is not None]
        average_score = int(sum(scores) / len(scores)) if scores else 0
        completion_percentage = int((completed / total) * 100) if total > 0 else 0
        
        data = {
            "user_id": user_id,
            "completion_percentage": completion_percentage,
            "completed_modules": completed,
            "total_modules": total,
            "average_score": average_score,
            "modules_progress": {k: {
                "user_id": v.user_id,
                "module_id": v.module_id,
                "completed": v.completed,
                "quiz_score": v.quiz_score,
                "incorrect_answers": v.incorrect_answers,
                "time_spent": v.time_spent,
                "completion_date": v.completion_date
            } for k, v in progress_data.items()}
        }
        self.send_json_response(data)


def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CourseHandler)
    print(f"""
🚀 Cybersecurity Course Test Server Started!

📖 Open your browser and navigate to:
   http://localhost:{port}/cybersecurity-course.html

🛡️ Nederlandse Cybersecurity Cursus voor Werknemers
   - 6 interactieve modules
   - Quizzes met feedback
   - Voortgang tracking
   - Verbeteringsaanbevelingen

Press Ctrl+C to stop the server.
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Bedankt voor het testen!")
        httpd.server_close()


if __name__ == '__main__':
    run_server()