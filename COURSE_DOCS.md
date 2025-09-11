# Euramax Cybersecurity Cursus - Documentatie

## Overzicht

De Euramax Cybersecurity Cursus is een uitgebreide Nederlandse educatieve applicatie ontworpen voor werknemers die gevoelige gegevens behandelen. De cursus biedt interactieve leerervaringen met intelligente quiz-systemen, voortgangsregistratie en geavanceerde foutanalyse.

## Functies

### 📚 Educatieve Content
- **5 Uitgebreide Modules**: Van beginner tot gevorderd niveau
- **Nederlandse Lokalisatie**: Volledige Nederlandse interface en content
- **Cybersecurity Topics**: Phishing, wachtwoorden, malware, gegevensbescherming, social engineering
- **Interactieve Content**: Rich text met voorbeelden, scenario's en praktische tips

### 📝 Intelligente Quiz Systemen
- **Adaptieve Vraagstelling**: Toont alleen vragen die nog niet correct beantwoord zijn
- **Verschillende Vraagtypen**: Multiple choice, waar/onwaar, scenario-gebaseerd
- **Directe Feedback**: Onmiddellijke uitleg bij elke vraag
- **Moeilijkheidsgraad**: Beginner, gemiddeld, gevorderd

### 🔄 Fout Review & Herhaling
- **Error Analysis**: Gedetailleerde analyse van foute antwoorden
- **Review Functionaliteit**: Mogelijkheid om alleen foute vragen opnieuw te bekijken
- **Educatieve Uitleg**: Uitgebreide uitleg waarom een antwoord juist/onjuist is
- **Retry Mechanisme**: Herhaal specifieke vragen totdat deze correct beantwoord zijn

### 📊 Voortgangsregistratie
- **Module Progress**: Individuele voortgang per module
- **Overall Score**: Gemiddelde score over alle modules
- **Time Tracking**: Bijhouden van bestede tijd per module
- **Completion Status**: Markering van voltooide modules (80%+ vereist)

### 📱 Responsive Design
- **Mobile-First**: Ontworpen voor gebruik op alle apparaten
- **Touch-Friendly**: Geoptimaliseerd voor touch interfaces
- **Accessible**: Voldoet aan moderne toegankelijkheidseisen
- **Progressive**: Werkt ook bij slechte internetverbindingen

## Technische Architectuur

### Backend (FastAPI)
```
euramax/course/
├── __init__.py          # Module initialisatie
├── models.py            # Data modellen voor cursus
├── service.py           # Business logic en content management
└── api/routes/course.py # REST API endpoints
```

### Frontend (Vanilla JavaScript)
```
static/course.html       # Single-page applicatie met volledige UI
```

### Database Modellen

#### CourseModule
- **Basis Info**: ID, titel, beschrijving, geschatte tijd
- **Content**: Volledige module content in markdown
- **Quiz**: Lijst van quiz vragen
- **Metadata**: Moeilijkheidsgraad, onderwerpen, vereisten

#### UserProgress
- **Algemeen**: Totale voortgang, voltooide modules, overall score
- **Module Specifiek**: Voortgang per module, quiz scores, foute vragen
- **Tijd**: Bestede tijd per module en totaal

#### QuizQuestion
- **Vraag**: Tekst, type, moeilijkheidsgraad
- **Antwoorden**: Multiple choice opties met correctheid
- **Educatie**: Uitgebreide uitleg en scenario context

## API Endpoints

### Modules
```http
GET /api/v1/course/modules
GET /api/v1/course/modules/{module_id}
```

### Gebruiker Voortgang
```http
GET /api/v1/course/users/{user_id}/progress
POST /api/v1/course/users/{user_id}/modules/{module_id}/start
POST /api/v1/course/users/{user_id}/modules/{module_id}/complete-content
```

### Quiz Systeem
```http
GET /api/v1/course/users/{user_id}/modules/{module_id}/quiz
POST /api/v1/course/users/{user_id}/modules/{module_id}/quiz/submit
GET /api/v1/course/users/{user_id}/modules/{module_id}/review
```

### Statistieken
```http
GET /api/v1/course/statistics
```

## Cursus Modules

### 1. Phishing Herkennen en Voorkomen (Beginner - 15 min)
- **Onderwerpen**: Phishing, email security, social engineering
- **Content**: Herkenning van phishing, beschermingsmaatregelen, echte voorbeelden
- **Quiz**: 3 vragen over phishing herkenning en preventie

### 2. Wachtwoordbeveiliging en Authenticatie (Beginner - 12 min)
- **Onderwerpen**: Passwords, authentication, account security
- **Content**: Sterke wachtwoorden, password managers, 2FA
- **Quiz**: 2 vragen over wachtwoordbeveiliging

### 3. Malware Bescherming (Gemiddeld - 20 min)
- **Onderwerpen**: Malware, antivirus, ransomware
- **Content**: Types malware, beschermingsstrategieën, incident response
- **Quiz**: 2 vragen over malware herkenning en bescherming

### 4. Gegevensbescherming en Privacy (Gemiddeld - 18 min)
- **Onderwerpen**: Data protection, privacy, GDPR
- **Content**: GDPR compliance, datalek procedures, privacy rechten
- **Quiz**: 2 vragen over gegevensbescherming

### 5. Social Engineering Aanvallen (Gevorderd - 25 min)
- **Onderwerpen**: Social engineering, manipulation, human factors
- **Content**: Psychologische technieken, herkenning, verdediging
- **Quiz**: 2 vragen over social engineering

## Gebruik

### Voor Eindgebruikers

1. **Toegang**: Ga naar `/static/course.html`
2. **Module Selectie**: Klik op een module in de sidebar
3. **Content Lezen**: Bestudeer de module content
4. **Quiz Maken**: Klik "Start Quiz" en beantwoord vragen
5. **Review**: Bekijk foute antwoorden en herhaal indien nodig
6. **Voortgang**: Monitor uw voortgang in de sidebar

### Voor Ontwikkelaars

#### Nieuwe Module Toevoegen
```python
# In service.py
async def _create_new_module(self) -> CourseModule:
    content = """
    # Module Titel
    
    ## Sectie 1
    Content hier...
    """
    
    questions = [
        QuizQuestion(
            id="new_q1",
            question="Vraag tekst?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.BEGINNER,
            cybersecurity_topic="topic",
            explanation="Uitgebreide uitleg",
            answers=[
                QuizAnswer("a1", "Optie 1", False, "Uitleg optie 1"),
                QuizAnswer("a2", "Optie 2", True, "Uitleg optie 2"),
            ]
        )
    ]
    
    return CourseModule(
        id="new-module",
        title="Nieuwe Module",
        description="Beschrijving",
        content=content,
        cybersecurity_topics=["topic"],
        difficulty=DifficultyLevel.BEGINNER,
        estimated_time_minutes=15,
        quiz_questions=questions
    )
```

#### API Integratie
```javascript
// Frontend JavaScript
const modules = await fetch('/api/v1/course/modules').then(r => r.json());
const progress = await fetch(`/api/v1/course/users/${userId}/progress`).then(r => r.json());
```

## Testing

### Unit Tests
```bash
# Alle course tests
python -m pytest tests/test_course_system.py -v

# Specifieke test
python -m pytest tests/test_course_system.py::TestCourseService::test_quiz_questions -v
```

### Test Coverage
- **Service Layer**: Volledige dekking van CourseService
- **Models**: Validatie van data structuren
- **API Endpoints**: Integratie tests via FastAPI
- **Quiz Logic**: Slimme vraagstelling en score berekening

## Beveiliging

### Data Beveiliging
- **Input Validatie**: Alle API inputs worden gevalideerd
- **SQL Injection**: Voorkomen via ORM patterns
- **XSS Protection**: HTML sanitization in frontend

### Toegangscontrole
- **User Isolation**: Gebruikers kunnen alleen eigen voortgang zien
- **API Security**: Endpoints vereisen geldige gebruiker ID
- **Content Protection**: Quiz antwoorden niet blootgesteld in frontend

## Performance

### Optimalisaties
- **Lazy Loading**: Modules worden on-demand geladen
- **Caching**: Statische content wordt gecached
- **Minimal API Calls**: Efficiënte data overdracht
- **Progressive Enhancement**: Basis functionaliteit zonder JavaScript

### Schaalbaarheid
- **Stateless Design**: Geen server-side sessions
- **Database Optimized**: Efficiënte queries en indexing
- **CDN Ready**: Statische assets kunnen via CDN worden geleverd

## Deployment

### Productie Setup
```bash
# Dependencies installeren
pip install -r requirements.txt

# Server starten (for local development)
uvicorn euramax.main:app --host 0.0.0.0 --port 8000

# Health check (when backend is running)
curl http://localhost:8000/health
```

### Environment Variables
```bash
# Course specifieke configuratie
COURSE_COMPLETION_THRESHOLD=0.8  # 80% voor module voltooiing
COURSE_DEMO_USER=demo_user
COURSE_MAX_ATTEMPTS=3           # Max quiz pogingen
```

## Monitoring

### Metrics
- **Module Completion Rate**: Percentage gebruikers dat modules voltooit
- **Quiz Performance**: Gemiddelde scores per module
- **Time on Content**: Tijd besteed aan lezen vs. quiz
- **Error Patterns**: Meest voorkomende foute antwoorden

### Logging
```python
# Voorbeeld log output
2025-09-11 16:04:16 [info] Module gestart user_id=demo_user module_id=phishing-basics
2025-09-11 16:04:20 [info] Quiz vraag beantwoord correct=True question_id=phish_q1
2025-09-11 16:04:25 [info] Module voltooid score=0.85 time_spent=15
```

## Roadmap

### Geplande Features
- **Certificate Generation**: PDF certificaten voor voltooide cursussen
- **Advanced Analytics**: Gedetailleerde leerpatroon analyse
- **Content Management**: Admin interface voor content beheer
- **Multi-language**: Ondersteuning voor andere talen naast Nederlands
- **Offline Mode**: Progressive Web App voor offline gebruik
- **Gamification**: Badges, leaderboards, achievements

### Technische Verbeteringen
- **Database Migration**: Van in-memory naar persistente opslag
- **Real-time Updates**: WebSocket ondersteuning voor live updates
- **API Versioning**: Backward-compatible API versioning
- **Advanced Testing**: End-to-end browser tests
- **Performance Monitoring**: APM integratie

## Ondersteuning

Voor vragen over de cursus applicatie:
- **GitHub Issues**: Create an issue for support
- **Documentation**: Deze file
- **Technical Support**: GitHub Issues or Pull Requests