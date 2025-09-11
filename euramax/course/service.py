"""
Euramax Course Service
Service voor het beheren van Nederlandse cybersecurity cursus content en gebruikersvoortgang
"""

import asyncio
import json
import structlog
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
import uuid
import random

from euramax.course.models import (
    CourseModule, QuizQuestion, QuizAnswer, UserProgress, ModuleProgress, 
    UserQuizAttempt, User, QuestionType, DifficultyLevel,
    DUTCH_CYBERSECURITY_MODULES
)


logger = structlog.get_logger()


class CourseService:
    """Service voor cursus en quiz functionaliteit"""
    
    def __init__(self):
        self.modules: Dict[str, CourseModule] = {}
        self.users: Dict[str, User] = {}
        self.user_progress: Dict[str, UserProgress] = {}
        self.is_initialized = False
        
    async def initialize(self):
        """Initialiseer course service met Nederlandse content"""
        logger.info("Initialiseren van Course Service")
        
        # Laad cursus modules met Nederlandse content
        await self._load_course_modules()
        
        # Maak test gebruiker aan voor demo
        await self._create_demo_user()
        
        self.is_initialized = True
        logger.info("Course Service operationeel", modules_loaded=len(self.modules))
        
    async def _load_course_modules(self):
        """Laad alle cursus modules met Nederlandse cybersecurity content"""
        
        # Module 1: Phishing Herkenning
        phishing_module = await self._create_phishing_module()
        self.modules[phishing_module.id] = phishing_module
        
        # Module 2: Wachtwoordbeveiliging
        password_module = await self._create_password_module()
        self.modules[password_module.id] = password_module
        
        # Module 3: Malware Bescherming
        malware_module = await self._create_malware_module()
        self.modules[malware_module.id] = malware_module
        
        # Module 4: Gegevensbescherming
        data_protection_module = await self._create_data_protection_module()
        self.modules[data_protection_module.id] = data_protection_module
        
        # Module 5: Social Engineering
        social_engineering_module = await self._create_social_engineering_module()
        self.modules[social_engineering_module.id] = social_engineering_module
        
    async def _create_phishing_module(self) -> CourseModule:
        """Maak phishing herkenning module"""
        content = """
# Phishing Herkennen en Voorkomen

## Wat is Phishing?

Phishing is een vorm van cybercriminaliteit waarbij aanvallers zich voordoen als betrouwbare entiteiten om gevoelige informatie te stelen, zoals:
- Wachtwoorden
- Creditcardgegevens  
- Persoonlijke informatie
- Bedrijfsgegevens

## Veelvoorkomende Phishing Technieken

### 1. Email Phishing
- **Spoofed afzenders**: Emails die lijken van bekende bedrijven te komen
- **Urgente taal**: "Uw account wordt opgeschort binnen 24 uur"
- **Verdachte links**: URLs die niet matchen met de beweerde afzender

### 2. Spear Phishing
- **Gerichte aanvallen**: Specifiek gericht op individuen of organisaties
- **Gepersonaliseerde berichten**: Gebruikmakend van publieke informatie
- **Hogere successkans**: Omdat ze geloofwaardiger lijken

## Herkenningssignalen

🚩 **Verdachte indicatoren:**
- Spelfouten en grammaticafouten
- Generieke begroetingen ("Beste klant")
- Dringende actie-oproepen
- Onverwachte attachments
- Links die niet overeenkomen met de tekst

## Beschermingsmaatregelen

### Voor Werknemers:
1. **Verifieer altijd** de afzender via een ander kanaal
2. **Hover over links** om de echte bestemming te zien
3. **Download geen** onverwachte attachments
4. **Rapporteer verdachte emails** aan IT-beveiliging

### Technische Bescherming:
- Email filters en spam detectie
- Anti-phishing software
- Twee-factor authenticatie
- Regelmatige beveiligingsupdates

## Wat te Doen bij Vermoeden van Phishing?

1. **Stop** - Open geen links of attachments
2. **Rapporteer** - Meld het aan security@euramax.eu
3. **Verwijder** - Delete de verdachte email
4. **Controleer** - Check of anderen ook deze email hebben ontvangen

## Echte Voorbeelden

### Voorbeeld 1: Phishing Email
```
Van: security@banke-nl.com
Onderwerp: URGENT: Verificatie Vereist

Beste klant,

Uw account is verdachte activiteit gedetecteerd. Klik hier om 
uw identiteit te verifiëren: http://bank-verificatie.ru

Met vriendelijke groet,
Het Beveiligingsteam
```

**Waarom dit phishing is:**
- Domein komt niet overeen (banke-nl.com vs echte bank)
- Urgente taal zonder specifieke details
- Link naar .ru domein (niet Nederlands)
- Generieke aanhef

## Oefening: Test Uw Kennis

Na het bestuderen van deze module, test uw kennis met de interactieve quiz om te controleren of u phishing-aanvallen kunt herkennen.
"""
        
        questions = [
            QuizQuestion(
                id="phish_q1",
                question="Welke van de volgende is GEEN typisch kenmerk van een phishing-email?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.BEGINNER,
                cybersecurity_topic="phishing",
                explanation="Persoonlijke begroetingen met uw echte naam zijn juist een teken van legitimiteit. Phishing-emails gebruiken vaak generieke begroetingen.",
                answers=[
                    QuizAnswer("a1", "Urgente taal en dreigingen", False, "Dit is wel een typisch kenmerk van phishing"),
                    QuizAnswer("a2", "Spelfouten in de tekst", False, "Phishing-emails bevatten vaak spelfouten"),
                    QuizAnswer("a3", "Persoonlijke begroeting met uw naam", True, "Correct! Legitieme emails gebruiken vaak uw echte naam"),
                    QuizAnswer("a4", "Verdachte links of attachments", False, "Dit is een duidelijk phishing-kenmerk")
                ]
            ),
            QuizQuestion(
                id="phish_q2", 
                question="U ontvangt een email van 'security@euramax.eu' die vraagt om uw wachtwoord. Wat doet u?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.INTERMEDIATE,
                cybersecurity_topic="phishing",
                explanation="Legitieme bedrijven vragen nooit om wachtwoorden via email. Verifieer altijd via een ander kanaal.",
                answers=[
                    QuizAnswer("b1", "Het wachtwoord direct invullen", False, "Nooit doen! Bedrijven vragen nooit om wachtwoorden"),
                    QuizAnswer("b2", "De email negeren", False, "Beter om te rapporteren voor anderen"),
                    QuizAnswer("b3", "Contact opnemen via telefoon om te verifiëren", True, "Correct! Altijd via een ander kanaal verifiëren"),
                    QuizAnswer("b4", "De email doorsturen naar collega's", False, "Dit kan de phishing verspreiden")
                ]
            ),
            QuizQuestion(
                id="phish_q3",
                question="Een email beweert van uw bank te komen, maar de link verwijst naar 'bank-verificatie.tk'. Is dit verdacht?",
                question_type=QuestionType.TRUE_FALSE,
                difficulty=DifficultyLevel.BEGINNER,
                cybersecurity_topic="phishing",
                explanation="Ja, dit is zeer verdacht. Banken gebruiken hun eigen domeinen (.nl, .com) en geen .tk-domeinen.",
                answers=[
                    QuizAnswer("t1", "Ja, dit is verdacht", True, "Correct! .tk-domeinen zijn vaak gebruikt voor phishing"),
                    QuizAnswer("t2", "Nee, dit is normaal", False, "Banken gebruiken nooit .tk-domeinen")
                ]
            )
        ]
        
        return CourseModule(
            id="phishing-basics",
            title="Phishing Herkennen en Voorkomen", 
            description="Leer hoe je phishing-aanvallen kunt herkennen en jezelf kunt beschermen",
            content=content,
            cybersecurity_topics=["phishing", "email_security", "social_engineering"],
            difficulty=DifficultyLevel.BEGINNER,
            estimated_time_minutes=15,
            quiz_questions=questions
        )
        
    async def _create_password_module(self) -> CourseModule:
        """Maak wachtwoordbeveiliging module"""
        content = """
# Wachtwoordbeveiliging en Authenticatie

## Het Belang van Sterke Wachtwoorden

Wachtwoorden zijn de eerste verdedigingslinie tegen cyberaanvallen. Zwakke wachtwoorden maken 81% van de databreeches mogelijk.

## Kenmerken van Sterke Wachtwoorden

### ✅ Goede Wachtwoorden:
- **Minimaal 12 karakters** lang
- **Combinatie** van hoofdletters, kleine letters, cijfers en symbolen  
- **Uniek** voor elke account
- **Geen persoonlijke informatie** (naam, geboortedatum)
- **Geen veelgebruikte woorden** of patronen

### ❌ Zwakke Wachtwoorden:
- "password123"
- "admin" 
- Uw naam + geboortejaar
- Toetsenbord patronen (qwerty, 123456)

## Wachtwoord Strategieën

### 1. Passphrase Methode
Gebruik een zin die gemakkelijk te onthouden is:
- "MijnKat3etGraag4Vissen!" 
- "IkWerk2024BijEuramax!"

### 2. Wachtwoord Managers
**Voordelen:**
- Genereert sterke, unieke wachtwoorden
- Onthoudt alle wachtwoorden voor u
- Synchroniseert tussen apparaten
- Waarschuwt voor hergebruik

**Aanbevolen tools:**
- 1Password
- Bitwarden  
- LastPass

## Twee-Factor Authenticatie (2FA)

### Wat is 2FA?
Een extra beveiligingslaag naast uw wachtwoord:
1. **Iets wat u weet** (wachtwoord)
2. **Iets wat u heeft** (telefoon, token)

### Soorten 2FA:
- **SMS codes** (minder veilig)
- **Authenticator apps** (Google Authenticator, Authy)
- **Hardware tokens** (YubiKey)
- **Biometrische data** (vingerafdruk, gezichtsherkenning)

## Account Beveiliging Best Practices

### 1. Regelmatige Updates
- Verander wachtwoorden na databreaches
- Update belangrijke accounts elke 3-6 maanden
- Gebruik nooit hetzelfde wachtwoord voor meerdere accounts

### 2. Monitoring
- Controleer account activiteit regelmatig
- Stel meldingen in voor inlogpogingen
- Meld verdachte activiteit direct

### 3. Recovery Opties
- Houd recovery emails bij
- Noteer backup codes op een veilige plaats
- Test recovery processen regelmatig

## Veelgemaakte Fouten

❌ **Vermijd deze fouten:**
- Wachtwoorden delen met collega's
- Wachtwoorden opschrijven op post-its
- Hetzelfde wachtwoord voor werk en privé
- Automatisch inloggen op gedeelde computers
- Wachtwoorden opslaan in browsers op gedeelde pc's

## Bedrijfsbeleid

Bij Euramax hanteren wij:
- **Minimaal 12 karakters** voor alle accounts
- **Verplichte 2FA** voor alle systemen
- **Wachtwoord rotatie** elke 90 dagen voor kritieke systemen
- **Account lockout** na 5 mislukte pogingen

## Wat te Doen bij Compromis?

1. **Direct handelen** - Verander het wachtwoord onmiddellijk
2. **Andere accounts** - Update alle accounts met hetzelfde wachtwoord  
3. **Rapporteren** - Meld het incident aan IT-beveiliging
4. **Monitoren** - Houd accounts extra goed in de gaten
"""

        questions = [
            QuizQuestion(
                id="pass_q1",
                question="Wat is de aanbevolen minimale lengte voor een veilig wachtwoord?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.BEGINNER,
                cybersecurity_topic="passwords",
                explanation="12 karakters is het huidige minimum voor goede beveiliging tegen moderne aanvallen.",
                answers=[
                    QuizAnswer("p1", "6 karakters", False, "Te kort voor moderne beveiligingseisen"),
                    QuizAnswer("p2", "8 karakters", False, "Niet meer voldoende tegen huidige aanvallen"),
                    QuizAnswer("p3", "12 karakters", True, "Correct! Dit is het aanbevolen minimum"),
                    QuizAnswer("p4", "16 karakters", False, "Dit is goed maar niet het minimum")
                ]
            ),
            QuizQuestion(
                id="pass_q2",
                question="Welke van deze is het veiligste type twee-factor authenticatie?",
                question_type=QuestionType.MULTIPLE_CHOICE, 
                difficulty=DifficultyLevel.INTERMEDIATE,
                cybersecurity_topic="authentication",
                explanation="Hardware tokens zoals YubiKey zijn het veiligst omdat ze niet gekaapt kunnen worden zoals SMS.",
                answers=[
                    QuizAnswer("p5", "SMS berichten", False, "SMS kan onderschept worden"),
                    QuizAnswer("p6", "Email codes", False, "Email accounts kunnen gehackt worden"),
                    QuizAnswer("p7", "Hardware tokens (YubiKey)", True, "Correct! Meest veilige optie"),
                    QuizAnswer("p8", "Beveiligingsvragen", False, "Beveiligingsvragen zijn niet 2FA")
                ]
            )
        ]
        
        return CourseModule(
            id="password-security",
            title="Wachtwoordbeveiliging en Authenticatie",
            description="Ontdek beste praktijken voor sterke wachtwoorden en twee-factor authenticatie",
            content=content,
            cybersecurity_topics=["passwords", "authentication", "account_security"],
            difficulty=DifficultyLevel.BEGINNER,
            estimated_time_minutes=12,
            quiz_questions=questions
        )
        
    async def _create_malware_module(self) -> CourseModule:
        """Maak malware bescherming module"""
        content = """
# Malware Bescherming

## Wat is Malware?

Malware (kwaadaardige software) is elk programma dat ontworpen is om schade aan te richten aan computers, netwerken of gebruikers.

## Types Malware

### 1. Virussen
- **Kenmerken**: Vermenigvuldigen zich en verspreiden via bestanden
- **Schade**: Bestandsvernietiging, systeemcorruptie
- **Verspreiding**: Email attachments, geïnfecteerde bestanden

### 2. Trojaanse Paarden
- **Kenmerken**: Vermomd als legitieme software
- **Schade**: Gegevensroof, backdoor toegang
- **Verspreiding**: Downloads, email attachments

### 3. Ransomware
- **Kenmerken**: Versleutelt bestanden en eist losgeld
- **Schade**: Bedrijfsstilstand, gegevensverlies
- **Verspreiding**: Phishing emails, exploit kits

### 4. Spyware
- **Kenmerken**: Verzamelt informatie zonder toestemming
- **Schade**: Privacy inbreuk, identiteitsdiefstal
- **Verspreiding**: Gratis software, websites

### 5. Adware
- **Kenmerken**: Toont ongewenste advertenties
- **Schade**: Prestatie verlies, privacy problemen
- **Verspreiding**: Software bundels, misleidende downloads

## Beschermingsstrategieën

### 1. Antivirussoftware
**Essentieel voor bescherming:**
- Real-time scanning
- Automatische updates
- Gedragsanalyse
- Web protection

**Aanbevolen oplossingen:**
- Windows Defender (ingebouwd)
- Bitdefender
- Kaspersky
- Norton

### 2. Besturingssysteem Updates
- **Automatische updates** inschakelen
- **Security patches** direct installeren
- **Legacy systemen** vermijden
- **End-of-life software** vervangen

### 3. Veilig Browsen
**Vermijd risicovolle sites:**
- Illegale download sites
- Gratis streaming platforms
- Onbekende software repositories
- Verdachte advertenties

### 4. Email Beveiliging
- **Scan attachments** voor virussen
- **Verifieer afzenders** van onverwachte bestanden
- **Gebruik email filtering** voor spam
- **Trainingsmateriaal** voor werknemers

## Herkenning van Infecties

### Waarschuwingssignalen:
🚨 **Computer gedrag:**
- Langzame prestaties
- Onverwachte pop-ups
- Programma's die crashen
- Onbekende software
- Hoge netwerk activiteit

🚨 **Browser problemen:**
- Gewijzigde startpagina
- Nieuwe toolbars
- Omgeleide zoekopdrachten
- Excessive advertenties

### Directe Actie:
1. **Disconnect** van internet
2. **Scan** met antivirus
3. **Rapporteer** aan IT-support
4. **Backup check** - zijn backups veilig?

## Bedrijfsbeleid bij Euramax

### Verplichte Maatregelen:
- **Managed antivirus** op alle werkstations
- **Automatische updates** voor OS en software
- **Email filtering** en attachment scanning
- **USB restricties** op kritieke systemen
- **Regelmatige backups** met offline copies

### Gebruikersverantwoordelijkheden:
- **Geen admin rechten** gebruiken voor dagelijks werk
- **Downloads** alleen van vertrouwde bronnen
- **Rapportage** van verdachte activiteit
- **Training** bijwonen en up-to-date blijven

## Incident Response

### Bij Vermoeden van Malware:
1. **Isoleer** het systeem (disconnect netwerk)
2. **Rapporteer** onmiddellijk aan security@euramax.eu
3. **Scan** met bijgewerkte antivirus
4. **Document** wat er gebeurde
5. **Volg** instructies van IT-security team

### Recovery Process:
- **Malware removal** door experts
- **System hardening** tegen herhaling
- **Data recovery** van schone backups
- **Monitoring** voor resterende infecties
- **Lesson learned** analyse

## Preventie Tips

✅ **Dagelijkse praktijken:**
- Houd software up-to-date
- Gebruik standaard user accounts
- Wees voorzichtig met downloads
- Maak regelmatig backups
- Train uw cybersecurity awareness

❌ **Vermijd deze risico's:**
- Onbekende email attachments openen
- Software van dubieuze websites downloaden
- Admin rechten voor dagelijks gebruik
- USB sticks van onbekende herkomst
- Beveiligingswaarschuwingen negeren
"""

        questions = [
            QuizQuestion(
                id="mal_q1",
                question="Welke type malware versleutelt uw bestanden en vraagt losgeld?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.INTERMEDIATE,
                cybersecurity_topic="malware",
                explanation="Ransomware versleutelt bestanden en eist betaling voor de ontsleuteling.",
                answers=[
                    QuizAnswer("m1", "Virus", False, "Virussen vermenigvuldigen zich maar eisen geen losgeld"),
                    QuizAnswer("m2", "Spyware", False, "Spyware verzamelt informatie heimelijk"),
                    QuizAnswer("m3", "Ransomware", True, "Correct! Ransomware eist losgeld voor ontsleuteling"),
                    QuizAnswer("m4", "Adware", False, "Adware toont ongewenste advertenties")
                ]
            ),
            QuizQuestion(
                id="mal_q2",
                question="Uw computer wordt plotseling zeer langzaam en toont onbekende pop-ups. Wat is de eerste actie?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.INTERMEDIATE,
                cybersecurity_topic="malware",
                explanation="Bij vermoeden van malware moet u eerst het systeem isoleren door de netwerkverbinding te verbreken.",
                answers=[
                    QuizAnswer("m5", "Opnieuw opstarten", False, "Dit lost het probleem niet op"),
                    QuizAnswer("m6", "Antivirus scan uitvoeren", False, "Eerst isoleren van netwerk"),
                    QuizAnswer("m7", "Disconnect van internet", True, "Correct! Isoleer eerst het systeem"),
                    QuizAnswer("m8", "Alle bestanden verwijderen", False, "Te drastisch en niet nodig")
                ]
            )
        ]
        
        return CourseModule(
            id="malware-protection",
            title="Malware Bescherming",
            description="Verstaan wat malware is en hoe je je systeem kunt beschermen",
            content=content,
            cybersecurity_topics=["malware", "antivirus", "ransomware"],
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_time_minutes=20,
            quiz_questions=questions
        )
        
    async def _create_data_protection_module(self) -> CourseModule:
        """Maak gegevensbescherming module"""
        content = """
# Gegevensbescherming en Privacy

## GDPR en Nederlandse Wetgeving

De Algemene Verordening Gegevensbescherming (GDPR) beschermt de privacy van EU-burgers en stelt strenge eisen aan organisaties.

### Kernprincipes GDPR:
1. **Rechtmatigheid** - Geldige reden voor verwerking
2. **Doelbinding** - Specifiek en legitiem doel
3. **Minimalisatie** - Niet meer dan nodig
4. **Juistheid** - Accurate en actuele gegevens
5. **Opslagbeperking** - Niet langer dan nodig
6. **Integriteit** - Veilige verwerking

## Soorten Persoonsgegevens

### Gewone Persoonsgegevens:
- Namen en adressen
- Telefoonnummers
- Email adressen  
- IP-adressen
- Cookie data

### Bijzondere Persoonsgegevens:
- Medische informatie
- Politieke overtuigingen
- Religieuze gegevens
- Biometrische gegevens
- Strafrechtelijke gegevens

## Rechten van Betrokkenen

### Belangrijke Rechten:
1. **Recht op informatie** - Transparante communicatie
2. **Recht op inzage** - Toegang tot eigen gegevens
3. **Recht op rectificatie** - Correctie van fouten
4. **Recht op vergetelheid** - Verwijdering van gegevens
5. **Recht op beperking** - Pauzeren van verwerking
6. **Recht op overdraagbaarheid** - Gegevens meenemen
7. **Recht van bezwaar** - Verzet tegen verwerking

## Veilige Gegevensverwerking

### Technische Maatregelen:
- **Versleuteling** van gevoelige data
- **Toegangscontrole** en authenticatie
- **Audit logs** voor traceerbaarheid  
- **Backup procedures** voor herstel
- **Netwerk beveiliging** tegen intrusions

### Organisatorische Maatregelen:
- **Privacy by Design** - Privacy vanaf ontwerp
- **Data Protection Impact Assessment** (DPIA)
- **Medewerkerstraining** over privacy
- **Incident response procedures**
- **Contractuele afspraken** met verwerkers

## Gegevenslek Procedures

### Herkenning van Datalekken:
🚨 **Signalen:**
- Ongeautoriseerde toegang tot systemen
- Verlies van apparaten met gegevens
- Mislukking van backup systemen
- Phishing aanvallen op medewerkers
- Malware infecties

### Incident Response (72 uur regel):
1. **Containment** - Stop verdere schade
2. **Assessment** - Bepaal omvang en impact
3. **Notification** - Meld binnen 72 uur aan AP
4. **Communication** - Informeer betrokkenen indien nodig
5. **Documentation** - Documenteer alle acties
6. **Review** - Leer van het incident

## Werknemersrichtlijnen

### ✅ Doe's:
- **Minimale toegang** - Alleen benodigde gegevens
- **Veilige opslag** - Gebruik bedrijfssystemen
- **Screen locks** - Vergrendel bij verlaten werkplek
- **Clean desk** - Geen gevoelige documenten zichtbaar
- **Rapporteer incidents** - Bij twijfel altijd melden

### ❌ Don'ts:
- **Geen privé-email** voor bedrijfsgegevens
- **Geen USB-sticks** voor gevoelige data
- **Geen gedeelde accounts** tussen medewerkers
- **Geen onbeveiligde cloud** services
- **Geen screenshots** van vertrouwelijke informatie

## Internationale Gegevensoverdracht

### Europese Economische Ruimte (EER):
- **Vrije overdracht** binnen EER landen
- **Gelijk beschermingsniveau** verondersteld

### Landen Buiten EER:
- **Adequaatheid beslissing** van Europese Commissie
- **Passende waarborgen** zoals Standard Contractual Clauses
- **Binding Corporate Rules** voor multinationals
- **Toestemming** van betrokkene in specifieke gevallen

## Privacy Impact Assessment

### Wanneer Verplicht:
- Systematische monitoring van publieke ruimtes
- Grootschalige verwerking van bijzondere categorieën
- Automated decision making met rechtsgevolgen

### DPIA Process:
1. **Beschrijving** van verwerkingsactiviteit
2. **Noodzaak** en evenredigheid beoordelen
3. **Risico's** voor betrokkenen identificeren
4. **Maatregelen** om risico's te mitigeren
5. **Consultatie** stakeholders en AP indien nodig

## Euramax Gegevensbeleid

### Onze Toewijding:
- **Privacy by Design** in alle systemen
- **Minimale gegevensverzameling**
- **Versleuteling** van alle gevoelige data
- **Regelmatige audits** en assessments
- **24/7 monitoring** voor veiligheidsincidenten

### Contactgegevens:
- **Data Protection Officer**: privacy@euramax.eu
- **Security Incidents**: security@euramax.eu
- **Algemene vragen**: info@euramax.eu
"""

        questions = [
            QuizQuestion(
                id="data_q1",
                question="Binnen hoeveel uur moet een datalek gemeld worden aan de Autoriteit Persoonsgegevens?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.INTERMEDIATE,
                cybersecurity_topic="data_protection",
                explanation="GDPR vereist melding binnen 72 uur na vaststelling van het datalek.",
                answers=[
                    QuizAnswer("d1", "24 uur", False, "Te kort volgens GDPR regelgeving"),
                    QuizAnswer("d2", "48 uur", False, "Nog steeds te kort"),
                    QuizAnswer("d3", "72 uur", True, "Correct! GDPR vereist melding binnen 72 uur"),
                    QuizAnswer("d4", "1 week", False, "Te lang, kan tot boetes leiden")
                ]
            ),
            QuizQuestion(
                id="data_q2",
                question="Welke gegevens vallen onder bijzondere categorieën volgens GDPR?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.ADVANCED,
                cybersecurity_topic="privacy",
                explanation="Medische gegevens zijn bijzondere persoonsgegevens met extra bescherming onder GDPR.",
                answers=[
                    QuizAnswer("d5", "Email adressen", False, "Dit zijn gewone persoonsgegevens"),
                    QuizAnswer("d6", "Telefoonnummers", False, "Dit zijn gewone persoonsgegevens"),
                    QuizAnswer("d7", "Medische informatie", True, "Correct! Valt onder bijzondere categorieën"),
                    QuizAnswer("d8", "Bedrijfsnamen", False, "Dit zijn geen persoonsgegevens")
                ]
            )
        ]
        
        return CourseModule(
            id="data-protection",
            title="Gegevensbescherming en Privacy",
            description="Leer over GDPR-compliance en veilige gegevensbehandeling",
            content=content,
            cybersecurity_topics=["data_protection", "privacy", "gdpr"],
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_time_minutes=18,
            quiz_questions=questions
        )
        
    async def _create_social_engineering_module(self) -> CourseModule:
        """Maak social engineering module"""
        content = """
# Social Engineering Aanvallen

## Wat is Social Engineering?

Social engineering is de kunst van het manipuleren van mensen om vertrouwelijke informatie prijs te geven of beveiligingsmaatregelen te omzeilen. Aanvallers maken gebruik van menselijke psychologie in plaats van technische hacks.

## Psychologische Technieken

### 1. Autoriteit
- **Voordoen als manager** of CEO
- **Uniform** of officiële titels gebruiken
- **Druk uitoefenen** via hiërarchie

### 2. Urgentie en Schaarste
- **"Dit aanbod geldt alleen vandaag"**
- **"Uw account wordt binnen uren gesloten"**
- **Tijdsdruk** creëren voor snelle beslissingen

### 3. Vertrouwen en Sympathie
- **Gemeenschappelijke interesses** vinden
- **Complimenten** geven
- **Persoonlijke verhalen** delen

### 4. Angst
- **Dreigen met consequenties**
- **"Uw computer is geïnfecteerd"**
- **Juridische gevolgen** suggereren

## Veelvoorkomende Aanvallen

### 1. Pretexting
**Definitie**: Een verzonnen scenario creëren om informatie te verkrijgen

**Voorbeeld**:
> "Hallo, ik ben van de IT-afdeling. We hebben een beveiligingsincident en moeten uw wachtwoord controleren voor uw veiligheid."

**Bescherming**:
- Verifieer identiteit via officiële kanalen
- IT vraagt nooit om wachtwoorden
- Bij twijfel, hang op en bel terug

### 2. Baiting
**Definitie**: Lokken met gratis items of interessante content

**Voorbeelden**:
- USB-sticks in parkeerplaats
- "Gratis muziek downloads"
- "Exclusieve foto's van celebrity"

**Bescherming**:
- Gebruik geen onbekende USB's
- Download alleen van vertrouwde bronnen
- Te mooi om waar te zijn = waarschijnlijk vals

### 3. Quid Pro Quo
**Definitie**: Dienst aanbieden in ruil voor informatie

**Voorbeeld**:
> "Ik kan uw computer versnellen, ik heb alleen uw inloggegevens nodig om de software te installeren."

**Bescherming**:
- Officiële IT-support volgt procedures
- Geen externe "hulp" accepteren
- Altijd verifiëren via bekende kanalen

### 4. Tailgating
**Definitie**: Meelopen achter geautoriseerde personen

**Scenario's**:
- "Mijn pasje werkt niet, mag ik meelopen?"
- Voordoen als leverancier
- Vriendelijk meelopen bij koffie halen

**Bescherming**:
- Elke persoon moet eigen toegang gebruiken
- Vriendelijk maar alert blijven
- Meld verdachte personen aan beveiliging

## Digitale Social Engineering

### 1. Spear Phishing
- **Gepersonaliseerde aanvallen** met echte informatie
- **LinkedIn profiles** voor research
- **Collega namen** en bedrijfsinformatie gebruiken

### 2. Watering Hole Attacks
- **Websites infecteren** die doelgroep bezoekt
- **Branche-specifieke sites** compromitteren
- **Malware** via legitieme websites

### 3. Social Media Exploitatie
- **Fake accounts** om vertrouwen te winnen
- **Informatie verzameling** via posts
- **Phishing links** delen in berichten

## Bescherming Strategieën

### Persoonlijke Beveiliging:
1. **Verificatie Protocol**
   - Altijd identiteit bevestigen
   - Gebruik officiële contactgegevens
   - Bij twijfel: hang op en bel terug

2. **Informatie Bewustzijn**
   - Beperkt delen op social media
   - Privacy instellingen controleren
   - Geen bedrijfsinfo in persoonlijke posts

3. **Skeptisch Blijven**
   - Te mooi om waar te zijn
   - Urgente verzoeken wantrouwen
   - Autoriteit niet blind accepteren

### Organisatie Niveau:
1. **Training en Bewustzijn**
   - Regelmatige awareness sessies
   - Phishing simulaties
   - Incident rapportage procedures

2. **Technische Maatregelen**
   - Email filtering
   - Web filtering
   - Endpoint protection

3. **Beleidsmaatregelen**
   - Clear desk policy
   - Bezoekersregistratie
   - Verificatie procedures

## Herkenning van Aanvallen

### 🚩 Waarschuwingssignalen:

**Telefoongevaar:**
- Onverwachte oproepen om informatie
- Druk om snel te handelen
- Vragen naar vertrouwelijke data
- Emotionele manipulatie

**Email/Bericht Signalen:**
- Urgente taal
- Spelfouten in professionele context
- Onverwachte links of attachments
- Verzoeken om gevoelige informatie

**Fysieke Signalen:**
- Onbekende personen in beveiligde gebieden
- Mensen die vragen om mee te lopen
- Verdachte vragen over systemen
- Poging tot informatie verzameling

## Incident Response

### Bij Vermoeden van Social Engineering:
1. **Stop** de interactie onmiddellijk
2. **Documenteer** wat er gebeurde
3. **Rapporteer** aan security@euramax.eu
4. **Waarschuw** collega's indien nodig
5. **Verander** wachtwoorden bij compromis

### Na een Incident:
- **Analyse** van de aanval
- **Lessons learned** sessie
- **Update** security awareness training
- **Versterking** van procedures

## Test Uw Alertheid

### Scenario 1:
U krijgt een telefoontje: *"Dit is Microsoft Support. We zien verdachte activiteit op uw computer. Kunt u ons uw wachtwoord geven zodat we kunnen helpen?"*

**Reactie**: ❌ Hang op! Microsoft belt nooit ongevraagd.

### Scenario 2:
Een email van "HR": *"Bijgevoegd uw nieuwe arbeidscontract ter ondertekening. Klik hier om te downloaden."*

**Reactie**: 🔍 Verifieer bij HR voor opening attachment.

### Scenario 3:
Bij de koffieautomaat: *"Hoi, ik ben nieuw op IT. Welk systeem gebruiken jullie voor email?"*

**Reactie**: 🚨 Rapporteer aan beveiliging - geen bedrijfsinformatie delen.
"""

        questions = [
            QuizQuestion(
                id="social_q1",
                question="Iemand belt zich voor als Microsoft Support en vraagt om toegang tot uw computer. Wat doet u?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.ADVANCED,
                cybersecurity_topic="social_engineering",
                explanation="Microsoft belt nooit ongevraagd. Dit is een klassieke social engineering techniek.",
                answers=[
                    QuizAnswer("s1", "Toegang verlenen omdat het Microsoft is", False, "Microsoft belt nooit ongevraagd"),
                    QuizAnswer("s2", "Ophangen en rapporteren", True, "Correct! Dit is een oplichting"),
                    QuizAnswer("s3", "Eerst om legitimatie vragen", False, "Hang direct op, geen discussie"),
                    QuizAnswer("s4", "Doorverbinden naar IT", False, "Hang direct op om IT te beschermen")
                ]
            ),
            QuizQuestion(
                id="social_q2",
                question="Wat is de belangrijkste verdediging tegen social engineering?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.ADVANCED,
                cybersecurity_topic="human_factors",
                explanation="Bewustzijn en training van medewerkers is de beste verdediging tegen social engineering.",
                answers=[
                    QuizAnswer("s5", "Firewall software", False, "Technologie helpt niet tegen social engineering"),
                    QuizAnswer("s6", "Antivirus programma's", False, "Dit beschermt niet tegen manipulatie"),
                    QuizAnswer("s7", "Medewerker bewustzijn en training", True, "Correct! Mensen zijn de eerste verdedigingslinie"),
                    QuizAnswer("s8", "Sterke wachtwoorden", False, "Helpt niet als je gemanipuleerd wordt om ze te delen")
                ]
            )
        ]
        
        return CourseModule(
            id="social-engineering",
            title="Social Engineering Aanvallen",
            description="Herken en voorkom manipulatietechnieken van cybercriminelen",
            content=content,
            cybersecurity_topics=["social_engineering", "manipulation", "human_factors"],
            difficulty=DifficultyLevel.ADVANCED,
            estimated_time_minutes=25,
            quiz_questions=questions
        )
    
    async def _create_demo_user(self):
        """Maak demo gebruiker voor testing"""
        demo_user = User(
            id="demo_user",
            email="demo@euramax.eu",
            full_name="Demo Gebruiker",
            department="IT",
            role="Employee"
        )
        self.users[demo_user.id] = demo_user
        
        # Initialiseer lege progress
        self.user_progress[demo_user.id] = UserProgress(
            user_id=demo_user.id,
            total_modules=len(self.modules),
            completed_modules=0,
            overall_score=0.0,
            total_time_spent_minutes=0,
            module_progress={}
        )

    # Public API Methods
    
    async def get_all_modules(self) -> List[CourseModule]:
        """Krijg alle beschikbare cursus modules"""
        return list(self.modules.values())
    
    async def get_module(self, module_id: str) -> Optional[CourseModule]:
        """Krijg een specifieke module"""
        return self.modules.get(module_id)
    
    async def get_user_progress(self, user_id: str) -> Optional[UserProgress]:
        """Krijg gebruikersvoortgang"""
        return self.user_progress.get(user_id)
    
    async def start_module(self, user_id: str, module_id: str) -> bool:
        """Start een module voor een gebruiker"""
        if module_id not in self.modules:
            return False
            
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(
                user_id=user_id,
                total_modules=len(self.modules),
                completed_modules=0,
                overall_score=0.0,
                total_time_spent_minutes=0,
                module_progress={}
            )
        
        # Initialiseer module progress
        self.user_progress[user_id].module_progress[module_id] = ModuleProgress(
            user_id=user_id,
            module_id=module_id,
            is_completed=False,
            content_viewed=False,
            quiz_score=0.0,
            quiz_attempts=[],
            incorrect_questions=set(),
            time_spent_minutes=0,
            started_at=datetime.now()
        )
        
        logger.info("Module gestart", user_id=user_id, module_id=module_id)
        return True
    
    async def complete_module_content(self, user_id: str, module_id: str, time_spent: int) -> bool:
        """Markeer module content als bekeken"""
        if user_id not in self.user_progress or module_id not in self.user_progress[user_id].module_progress:
            return False
            
        progress = self.user_progress[user_id].module_progress[module_id]
        progress.content_viewed = True
        progress.time_spent_minutes += time_spent
        progress.last_accessed = datetime.now()
        
        self.user_progress[user_id].total_time_spent_minutes += time_spent
        
        return True
    
    async def submit_quiz_answer(self, user_id: str, module_id: str, question_id: str, 
                               selected_answer_id: str, time_spent: int) -> Dict[str, any]:
        """Submit een quiz antwoord en return feedback"""
        if (user_id not in self.user_progress or 
            module_id not in self.user_progress[user_id].module_progress or
            module_id not in self.modules):
            return {"error": "Invalid user, module, or question"}
        
        module = self.modules[module_id]
        question = next((q for q in module.quiz_questions if q.id == question_id), None)
        
        if not question:
            return {"error": "Question not found"}
        
        # Check correct answer
        correct_answer = next((a for a in question.answers if a.is_correct), None)
        selected_answer = next((a for a in question.answers if a.id == selected_answer_id), None)
        
        if not selected_answer:
            return {"error": "Invalid answer selection"}
        
        is_correct = selected_answer.is_correct
        
        # Create attempt record
        attempt = UserQuizAttempt(
            id=str(uuid.uuid4()),
            user_id=user_id,
            module_id=module_id,
            question_id=question_id,
            selected_answer_id=selected_answer_id,
            is_correct=is_correct,
            timestamp=datetime.now(),
            time_spent_seconds=time_spent
        )
        
        # Update progress
        module_progress = self.user_progress[user_id].module_progress[module_id]
        module_progress.quiz_attempts.append(attempt)
        
        if not is_correct:
            module_progress.incorrect_questions.add(question_id)
        elif question_id in module_progress.incorrect_questions:
            # Remove from incorrect if answered correctly
            module_progress.incorrect_questions.discard(question_id)
        
        # Calculate current quiz score
        await self._update_quiz_score(user_id, module_id)
        
        return {
            "is_correct": is_correct,
            "explanation": selected_answer.explanation,
            "correct_answer": correct_answer.text if not is_correct else None,
            "question_explanation": question.explanation
        }
    
    async def get_quiz_questions(self, user_id: str, module_id: str, exclude_correct: bool = True) -> List[QuizQuestion]:
        """Krijg quiz vragen, optioneel exclusief correct beantwoorde vragen"""
        if module_id not in self.modules:
            return []
            
        module = self.modules[module_id]
        questions = module.quiz_questions.copy()
        
        if exclude_correct and user_id in self.user_progress and module_id in self.user_progress[user_id].module_progress:
            # Exclude questions that were answered correctly
            module_progress = self.user_progress[user_id].module_progress[module_id]
            correctly_answered = set()
            
            for attempt in module_progress.quiz_attempts:
                if attempt.is_correct:
                    correctly_answered.add(attempt.question_id)
            
            questions = [q for q in questions if q.id not in correctly_answered or q.id in module_progress.incorrect_questions]
        
        # Shuffle questions for variety
        random.shuffle(questions)
        return questions
    
    async def get_incorrect_questions(self, user_id: str, module_id: str) -> List[QuizQuestion]:
        """Krijg alleen de incorrect beantwoorde vragen voor review"""
        if (user_id not in self.user_progress or 
            module_id not in self.user_progress[user_id].module_progress or
            module_id not in self.modules):
            return []
            
        module = self.modules[module_id]
        module_progress = self.user_progress[user_id].module_progress[module_id]
        
        incorrect_questions = [
            q for q in module.quiz_questions 
            if q.id in module_progress.incorrect_questions
        ]
        
        return incorrect_questions
    
    async def _update_quiz_score(self, user_id: str, module_id: str):
        """Update quiz score voor een module"""
        module_progress = self.user_progress[user_id].module_progress[module_id]
        module = self.modules[module_id]
        
        if not module.quiz_questions:
            return
            
        # Get latest attempt per question
        latest_attempts = {}
        for attempt in module_progress.quiz_attempts:
            if (attempt.question_id not in latest_attempts or 
                attempt.timestamp > latest_attempts[attempt.question_id].timestamp):
                latest_attempts[attempt.question_id] = attempt
        
        # Calculate score
        correct_count = sum(1 for attempt in latest_attempts.values() if attempt.is_correct)
        total_questions = len(module.quiz_questions)
        module_progress.quiz_score = correct_count / total_questions if total_questions > 0 else 0
        
        # Check if module is completed (80% score threshold)
        if module_progress.quiz_score >= 0.8 and module_progress.content_viewed:
            if not module_progress.is_completed:
                module_progress.is_completed = True
                module_progress.completed_at = datetime.now()
                self.user_progress[user_id].completed_modules += 1
                
                # Update overall score
                await self._update_overall_score(user_id)
    
    async def _update_overall_score(self, user_id: str):
        """Update overall gebruiker score"""
        user_progress = self.user_progress[user_id]
        
        if not user_progress.module_progress:
            return
            
        total_score = sum(mp.quiz_score for mp in user_progress.module_progress.values())
        user_progress.overall_score = total_score / len(user_progress.module_progress)
    
    async def health_check(self) -> str:
        """Health check voor course service"""
        if not self.is_initialized:
            return "not_initialized"
        return "operationeel"
    
    async def shutdown(self):
        """Shutdown course service"""
        logger.info("Course Service wordt afgesloten")
        self.is_initialized = False