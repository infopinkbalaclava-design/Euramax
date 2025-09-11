/**
 * Euramax Cybersecurity Course Application
 * JavaScript functionality for course navigation and quiz system
 */

// Course state management
let currentSection = 'intro';
let completedSections = [];
let quizAttempts = 0;
let wrongAnswers = [];
let usedQuestions = [];

// Course sections in order
const sections = ['intro', 'phishing', 'passwords', 'malware', 'social', 'data', 'quiz'];

// Quiz questions database with detailed, challenging questions
const quizQuestions = [
    // Phishing Questions (5)
    {
        id: 1,
        category: 'phishing',
        question: 'Een email van "security@euramax.eu" vraagt u om uw wachtwoord te verifiëren via een bijgevoegde link. De link leidt naar "https://euramax-security.eu/verify". Wat is de beste actie?',
        options: [
            'Direct op de link klikken om te verifiëren',
            'De link kopiëren en in een nieuwe browser tab openen',
            'De email doorsturen naar IT voor verificatie',
            'Handmatig naar euramax.eu navigeren en inloggen om te controleren'
        ],
        correct: 3,
        explanation: 'Hoewel de email en link er legitiem uitzien, moet je altijd handmatig naar de officiële website navigeren. Cybercriminelen kunnen subtiele domain verschillen gebruiken (euramax-security.eu vs euramax.eu).'
    },
    {
        id: 2,
        category: 'phishing',
        question: 'U ontvangt een urgent email van uw CEO om onmiddellijk €50.000 over te maken naar een leverancier. De email komt van het correcte email adres en bevat de juiste handtekening. Wat doet u?',
        options: [
            'Onmiddellijk de betaling autoriseren vanwege de urgentie',
            'Bellen naar het bekende nummer van de CEO voor verificatie',
            'Vragen om schriftelijke autorisatie via een apart email',
            'De CFO vragen om bevestiging via email'
        ],
        correct: 1,
        explanation: 'Business Email Compromise aanvallen kunnen zeer geavanceerd zijn. Altijd telefonische verificatie doen via een bekend nummer bij grote financiële verzoeken, ongeacht hoe authentiek het email lijkt.'
    },
    {
        id: 3,
        category: 'phishing',
        question: 'Welke van deze URL\'s is het meest waarschijnlijk een phishing website die probeert de Nederlandse Belastingdienst na te bootsen?',
        options: [
            'https://www.belastingdienst.nl/login',
            'https://belastingdienst-nl.secure-login.eu',
            'https://secure.belastingdienst.nl/inloggen',
            'https://login.belastingdienst.nl/authenticate'
        ],
        correct: 1,
        explanation: 'Optie B gebruikt een ander domein (.eu) en bevat verdachte subdomains. Legitieme websites van de Belastingdienst gebruiken altijd het officiële .nl domein.'
    },
    {
        id: 4,
        category: 'phishing',
        question: 'U ontvangt een email met de onderwerpsregel "RE: Factuur #1234" van een bekende leverancier, maar u herinnert zich geen eerdere correspondentie. De bijlage is een .zip bestand. Wat is het grootste risico?',
        options: [
            'De factuur is mogelijk onjuist en veroorzaakt boekhoudkundige problemen',
            'Het .zip bestand kan malware bevatten en uw systeem infecteren',
            'De leverancier heeft mogelijk het verkeerde email adres gebruikt',
            'Het email kan spam zijn en uw inbox vervuilen'
        ],
        correct: 1,
        explanation: 'Het "RE:" in de onderwerpsregel suggereert een voortgezet gesprek dat er niet was. .zip bestanden zijn een veelgebruikte methode om malware te verspreiden via email bijlagen.'
    },
    {
        id: 5,
        category: 'phishing',
        question: 'Tijdens een telefoongesprek beweert iemand van "Microsoft Support" dat uw computer is gecompromitteerd en vraagt toegang via TeamViewer. Welke indicator wijst er NIET op dat dit een scam is?',
        options: [
            'Microsoft belt nooit ongevraagd naar klanten',
            'Legitieme support vraagt nooit om remote access software te installeren',
            'De beller heeft een buitenlands accent',
            'De beller vraagt om wachtwoorden of persoonlijke informatie'
        ],
        correct: 2,
        explanation: 'Een buitenlands accent is op zich niet verdacht, aangezien veel legitieme callcenters wereldwijd opereren. De andere opties zijn echter duidelijke waarschuwingssignalen van een scam.'
    },

    // Password Security Questions (3)
    {
        id: 6,
        category: 'passwords',
        question: 'Welk wachtwoord biedt de beste beveiliging voor een bedrijfsaccount met toegang tot gevoelige klantdata?',
        options: [
            'Euramax2024!',
            'MijnGeb00rteD@tum1985',
            'P@ssw0rd123456789',
            'K7#mL9$nX2&vQ5!rE8'
        ],
        correct: 3,
        explanation: 'Optie D is volledig willekeurig, lang genoeg (16+ karakters) en bevat geen persoonlijke informatie. De andere opties bevatten voorspelbare elementen zoals bedrijfsnamen of persoonlijke data.'
    },
    {
        id: 7,
        category: 'passwords',
        question: 'Uw collega deelt zijn wachtwoord met u zodat u toegang hebt tot een gedeeld systeem tijdens zijn vakantie. Wat is de beste praktijk?',
        options: [
            'Het wachtwoord gebruiken en na zijn terugkeer vergeten',
            'Het wachtwoord noteren voor toekomstig gebruik',
            'Een tijdelijk account aanvragen via IT-procedures',
            'Het wachtwoord alleen gebruiken in noodgevallen'
        ],
        correct: 2,
        explanation: 'Wachtwoorden mogen nooit worden gedeeld. IT-afdelingen kunnen tijdelijke accounts aanmaken met beperkte rechten voor specifieke tijdsperioden, wat een veiligere oplossing is.'
    },
    {
        id: 8,
        category: 'passwords',
        question: 'U ontdekt dat uw wachtwoord voorkomt in een publieke database van gelekte wachtwoorden. Het wachtwoord is 14 karakters lang en bevat speciale tekens. Wat is uw prioriteit?',
        options: [
            'Het wachtwoord behouden omdat het sterk genoeg is',
            'Alleen het wachtwoord wijzigen voor kritieke accounts',
            'Onmiddellijk alle accounts met dit wachtwoord wijzigen',
            'Wachten tot het volgende reguliere wijzigingsmoment'
        ],
        correct: 2,
        explanation: 'Zodra een wachtwoord in een datalek voorkomt, moet het onmiddellijk worden gewijzigd op alle accounts, ongeacht de sterkte. Criminelen gebruiken deze databases voor automatische aanvallen.'
    },

    // Malware Questions (3)
    {
        id: 9,
        category: 'malware',
        question: 'Uw computer wordt plotseling zeer traag en u ziet onbekende processen in Task Manager. Wat is uw eerste actie?',
        options: [
            'De computer opnieuw opstarten om de processen te stoppen',
            'Onmiddellijk de computer loskoppelen van het netwerk',
            'Een volledige antivirus scan uitvoeren',
            'De onbekende processen handmatig beëindigen'
        ],
        correct: 1,
        explanation: 'Bij vermoeden van malware moet u eerst de computer isoleren om verspreiding naar andere systemen te voorkomen. Pas daarna kunt u verdere analyses en cleaning procedures uitvoeren.'
    },
    {
        id: 10,
        category: 'malware',
        question: 'Een ransomware aanval heeft uw bestanden versleuteld en eist €5000 losgeld. U heeft backups van vorige week. Wat is de beste strategie?',
        options: [
            'Het losgeld betalen om tijd te besparen',
            'Onderhandelen over een lager bedrag',
            'Systeem vanaf backups herstellen en recent werk opnieuw doen',
            'Wachten om te zien of de criminelen hun eisen verlagen'
        ],
        correct: 2,
        explanation: 'Betaal nooit losgeld - dit garandeert niet dat data wordt teruggekregen en financiert criminele activiteiten. Systemen herstellen vanaf backups is de veiligste en meest effectieve aanpak.'
    },
    {
        id: 11,
        category: 'malware',
        question: 'Welke bestandsextensie vormt het HOOGSTE risico wanneer ontvangen als email bijlage van een onbekende afzender?',
        options: [
            '.pdf',
            '.docx',
            '.jpg',
            '.scr'
        ],
        correct: 3,
        explanation: '.scr bestanden zijn screensaver bestanden die uitvoerbare code bevatten en vaak worden gebruikt om malware te verspreiden. PDF, DOCX en JPG kunnen ook gevaarlijk zijn, maar .scr is direct uitvoerbaar.'
    },

    // Social Engineering Questions (2)
    {
        id: 12,
        category: 'social',
        question: 'Iemand belt zich voor als nieuwe HR medewerker en vraagt om verificatie van personeelsgegevens "voor de nieuwe database". Welke verificatie methode is het meest betrouwbaar?',
        options: [
            'Vragen naar hun werknemernummer',
            'Terugbellen naar het hoofdnummer en doorverbinding vragen',
            'Vragen naar informatie die alleen HR zou weten',
            'Verificatie via email van hun bedrijfsaccount'
        ],
        correct: 1,
        explanation: 'Terugbellen naar het officiële hoofdnummer en vragen om doorverbinding is de meest betrouwbare methode, omdat u zo controleert of de persoon echt bij het bedrijf werkt.'
    },
    {
        id: 13,
        category: 'social',
        question: 'Een "technicus" verschijnt aan de deur en beweert dat hij de netwerkapparatuur moet controleren wegens "gemelde problemen". Hij heeft geen afspraak maar lijkt legitiem. Wat doet u?',
        options: [
            'Hem begeleiden naar de apparatuur omdat het dringend lijkt',
            'Zijn ID controleren en hem dan toegang verlenen',
            'Contact opnemen met IT/facilities voor verificatie voordat u toegang verleent',
            'Vragen om zijn visitekaartje en hem later terugbellen'
        ],
        correct: 2,
        explanation: 'Ongeautoriseerde fysieke toegang is een ernstig beveiligingsrisico. Verifieer altijd via interne kanalen voordat u onbekende personen toegang verleent tot gevoelige locaties.'
    },

    // Data Protection Questions (2)
    {
        id: 14,
        category: 'data',
        question: 'U moet gevoelige klantgegevens delen met een externe consultant. Welke methode voldoet het best aan AVG/GDPR vereisten?',
        options: [
            'Email met wachtwoord beveiliging',
            'Upload naar Google Drive met gedeelde link',
            'Verzending via gecertificeerd veilig portaal met toegangslogging',
            'USB stick met versleuteling persoonlijk overhandigen'
        ],
        correct: 2,
        explanation: 'Gecertificeerde veilige portalen bieden end-to-end versleuteling, toegangscontrole, audit trails en voldoen aan GDPR eisen voor gegevensverwerking en -overdracht.'
    },
    {
        id: 15,
        category: 'data',
        question: 'U ontdekt dat een collega gevoelige klantgegevens heeft geprint en op zijn bureau heeft laten liggen tijdens de lunch. Wat is uw verantwoordelijkheid?',
        options: [
            'De documenten op een veilige plaats leggen en de collega later waarschuwen',
            'De documenten onmiddellijk beveiligen en het incident melden aan de supervisor',
            'Niets doen omdat het niet uw verantwoordelijkheid is',
            'Een foto maken als bewijs voordat u actie onderneemt'
        ],
        correct: 1,
        explanation: 'U heeft de verantwoordelijkheid om data onmiddellijk te beveiligen en het incident te melden. Dit is een clear desk policy overtreding die beveiligingsrisico\'s met zich meebrengt.'
    },

    // Advanced/Mixed Questions (5)
    {
        id: 16,
        category: 'advanced',
        question: 'U merkt dat uw computer automatisch verbinding maakt met onbekende WiFi netwerken. Welk beveiligingsrisico is het meest zorgwekkend?',
        options: [
            'Hogere data kosten door ongecontroleerd gebruik',
            'Tragere internet verbinding door zwakke signalen',
            'Man-in-the-middle aanvallen door kwaadaardige access points',
            'Batterij verbruik door constante WiFi scanning'
        ],
        correct: 2,
        explanation: 'Kwaadaardige WiFi access points kunnen al uw internetverkeer onderscheppen, inclusief gevoelige bedrijfsdata. Auto-connect naar onbekende netwerken vormt een ernstig beveiligingsrisico.'
    },
    {
        id: 17,
        category: 'advanced',
        question: 'Welke combinatie van factoren maakt een succesvolle cyberaanval het meest waarschijnlijk?',
        options: [
            'Zwakke wachtwoorden + geen antivirus software',
            'Ongepatcht systeem + social engineering + tijdsdruk',
            'Oude hardware + gebrek aan training',
            'Geen firewall + veel email bijlagen'
        ],
        correct: 1,
        explanation: 'De combinatie van technische kwetsbaarheden (ongepatcht systeem), menselijke factoren (social engineering) en psychologische druk (tijdsdruk) creëert de perfecte storm voor succesvolle aanvallen.'
    },
    {
        id: 18,
        category: 'advanced',
        question: 'Een externe auditor vraagt om toegang tot het klantendatabase "om compliance te verifiëren". Hij heeft legitieme credentials van een bekende auditfirma. Wat is de juiste procedure?',
        options: [
            'Toegang verlenen omdat hij van een bekende firma komt',
            'Beperkte toegang geven met supervisie',
            'Verificatie via contractbeheer en autorisatie van management vereisen',
            'Hem vragen om een schriftelijk verzoek in te dienen'
        ],
        correct: 2,
        explanation: 'Externe toegang tot gevoelige databases vereist altijd formele autorisatie via contractbeheer en management, ongeacht de legitimiteit van de credentials. Dit is een critical control voor data beveiliging.'
    },
    {
        id: 19,
        category: 'advanced',
        question: 'Tijdens een beveiligingsincident ontdekt u dat gevoelige data mogelijk is gecompromitteerd. Wat is uw eerste prioriteit volgens AVG/GDPR?',
        options: [
            'Het incident onderzoeken om de oorzaak te vinden',
            'Alle gecompromitteerde systemen offline halen',
            'Het incident documenteren en binnen 72 uur melden aan de toezichthouder',
            'Betrokkenen onmiddellijk informeren over het mogelijke lek'
        ],
        correct: 1,
        explanation: 'Hoewel melding binnen 72 uur verplicht is, heeft containment (stoppen van verdere schade) absolute prioriteit om de impact te minimaliseren. Parallel moet documentatie en melding worden voorbereid.'
    },
    {
        id: 20,
        category: 'advanced',
        question: 'Welke indicator suggereert het sterkst dat uw organisatie doelwit is van een geavanceerde persistente bedreiging (APT)?',
        options: [
            'Veel spam emails in korte tijd',
            'Langzame computer prestaties',
            'Kleine, maar consistente data exfiltratie over lange periode',
            'Regelmatige pop-up advertenties'
        ],
        correct: 2,
        explanation: 'APT aanvallen zijn gekarakteriseerd door subtiele, langdurige infiltratie met geleidelijke data exfiltratie om detectie te vermijden. Dit in tegenstelling tot "smash and grab" aanvallen.'
    }
];

// Initialize the course
document.addEventListener('DOMContentLoaded', function() {
    updateProgress();
    updateNavigation();
    console.log('Euramax Cybersecurity Course initialized');
});

// Navigation functions
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.course-content, .quiz-section, .quiz-results').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Update menu items
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Find and activate the corresponding menu item
    const menuItems = document.querySelectorAll('.menu-item');
    const sectionIndex = sections.indexOf(sectionId);
    if (sectionIndex !== -1 && menuItems[sectionIndex]) {
        menuItems[sectionIndex].classList.add('active');
    }
    
    currentSection = sectionId;
    
    // Special handling for quiz section
    if (sectionId === 'quiz') {
        initializeQuiz();
    }
    
    updateProgress();
    updateNavigation();
}

function nextSection() {
    const currentIndex = sections.indexOf(currentSection);
    if (currentIndex < sections.length - 1) {
        // Mark current section as completed
        if (!completedSections.includes(currentSection)) {
            completedSections.push(currentSection);
            markSectionCompleted(currentSection);
        }
        
        const nextSectionId = sections[currentIndex + 1];
        showSection(nextSectionId);
    }
}

function previousSection() {
    const currentIndex = sections.indexOf(currentSection);
    if (currentIndex > 0) {
        const prevSectionId = sections[currentIndex - 1];
        showSection(prevSectionId);
    }
}

function updateNavigation() {
    const currentIndex = sections.indexOf(currentSection);
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    // Update previous button
    if (prevBtn) {
        prevBtn.disabled = currentIndex === 0;
    }
    
    // Update next button
    if (nextBtn) {
        if (currentIndex === sections.length - 1) {
            nextBtn.style.display = 'none';
        } else {
            nextBtn.style.display = 'inline-block';
            nextBtn.disabled = false;
        }
    }
}

function updateProgress() {
    const progressBar = document.getElementById('progressBar');
    const currentIndex = sections.indexOf(currentSection);
    const progress = ((currentIndex + 1) / sections.length) * 100;
    
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
    }
}

function markSectionCompleted(sectionId) {
    const menuItems = document.querySelectorAll('.menu-item');
    const sectionIndex = sections.indexOf(sectionId);
    
    if (sectionIndex !== -1 && menuItems[sectionIndex]) {
        menuItems[sectionIndex].classList.add('completed');
    }
}

// Quiz functionality
function initializeQuiz() {
    const quizContainer = document.getElementById('quiz-section');
    if (!quizContainer) {
        createQuizSection();
    }
    
    document.getElementById('quiz-section').classList.add('active');
    displayQuiz();
}

function createQuizSection() {
    const quizHTML = `
        <div class="quiz-section" id="quiz-section">
            <h2>📝 Cybersecurity Kennistoets</h2>
            <p>Test uw kennis met deze uitdagende vragen over cybersecurity. Let goed op - de vragen zijn ontworpen om uw werkelijke begrip te testen!</p>
            
            <div class="critical-box">
                <strong>⚠️ Instructies:</strong>
                <ul>
                    <li>Lees elke vraag zorgvuldig door</li>
                    <li>U heeft 15 vragen om te beantwoorden</li>
                    <li>Bij foute antwoorden krijgt u uitleg en een nieuwe kans</li>
                    <li>Verschillende vragen bij elke poging</li>
                </ul>
            </div>
            
            <div id="quiz-content"></div>
            <div class="navigation">
                <button class="btn" id="submitQuiz" onclick="submitQuiz()" style="display: none;">Toets Indienen</button>
            </div>
        </div>
        
        <div class="quiz-results" id="quiz-results">
            <h2>📊 Toets Resultaten</h2>
            <div class="score-display">
                <div class="score-circle" id="scoreCircle">
                    <div class="score-text" id="scoreText">0%</div>
                </div>
                <h3 id="scoreMessage">Resultaat wordt berekend...</h3>
            </div>
            
            <div class="wrong-answers" id="wrongAnswersSection" style="display: none;">
                <h3>❌ Foute Antwoorden - Leer van je Fouten</h3>
                <div id="wrongAnswersList"></div>
                
                <div class="retry-section">
                    <p>Wilt u de foute vragen opnieuw proberen met andere vragen?</p>
                    <button class="btn" onclick="retryQuiz()">🔄 Opnieuw Proberen</button>
                    <button class="btn" onclick="restartCourse()">🏁 Cursus Opnieuw Starten</button>
                </div>
            </div>
        </div>
    `;
    
    const navigation = document.querySelector('.navigation');
    navigation.insertAdjacentHTML('beforebegin', quizHTML);
}

function displayQuiz() {
    const quizContent = document.getElementById('quiz-content');
    const selectedQuestions = selectQuizQuestions();
    
    let quizHTML = '';
    selectedQuestions.forEach((question, index) => {
        quizHTML += `
            <div class="question" data-question-id="${question.id}">
                <h4>Vraag ${index + 1}: ${question.question}</h4>
                ${question.options.map((option, optIndex) => `
                    <label class="answer-option">
                        <input type="radio" name="question-${question.id}" value="${optIndex}">
                        ${option}
                    </label>
                `).join('')}
            </div>
        `;
    });
    
    quizContent.innerHTML = quizHTML;
    document.getElementById('submitQuiz').style.display = 'block';
}

function selectQuizQuestions() {
    // For retries, avoid previously used questions
    let availableQuestions = quizQuestions.filter(q => !usedQuestions.includes(q.id));
    
    // If we don't have enough unused questions, reset and use all
    if (availableQuestions.length < 15) {
        availableQuestions = [...quizQuestions];
        usedQuestions = [];
    }
    
    // Randomly select 15 questions
    const selected = [];
    const shuffled = [...availableQuestions].sort(() => 0.5 - Math.random());
    
    for (let i = 0; i < Math.min(15, shuffled.length); i++) {
        selected.push(shuffled[i]);
        usedQuestions.push(shuffled[i].id);
    }
    
    return selected;
}

function submitQuiz() {
    const questions = document.querySelectorAll('.question');
    let totalQuestions = questions.length;
    let correctAnswers = 0;
    wrongAnswers = [];
    
    questions.forEach(questionDiv => {
        const questionId = parseInt(questionDiv.dataset.questionId);
        const question = quizQuestions.find(q => q.id === questionId);
        const selectedOption = questionDiv.querySelector('input[type="radio"]:checked');
        
        if (selectedOption) {
            const selectedValue = parseInt(selectedOption.value);
            if (selectedValue === question.correct) {
                correctAnswers++;
                // Mark as correct visually
                selectedOption.closest('.answer-option').classList.add('correct');
            } else {
                // Mark as incorrect and store for review
                selectedOption.closest('.answer-option').classList.add('incorrect');
                // Show correct answer
                const correctOption = questionDiv.querySelectorAll('.answer-option')[question.correct];
                correctOption.classList.add('correct');
                
                wrongAnswers.push({
                    question: question.question,
                    selectedAnswer: question.options[selectedValue],
                    correctAnswer: question.options[question.correct],
                    explanation: question.explanation
                });
            }
        } else {
            // No answer selected - count as wrong
            const correctOption = questionDiv.querySelectorAll('.answer-option')[question.correct];
            correctOption.classList.add('correct');
            
            wrongAnswers.push({
                question: question.question,
                selectedAnswer: 'Geen antwoord gegeven',
                correctAnswer: question.options[question.correct],
                explanation: question.explanation
            });
        }
    });
    
    const score = Math.round((correctAnswers / totalQuestions) * 100);
    quizAttempts++;
    
    setTimeout(() => {
        showQuizResults(score, correctAnswers, totalQuestions);
    }, 2000);
}

function showQuizResults(score, correct, total) {
    document.getElementById('quiz-section').classList.remove('active');
    document.getElementById('quiz-results').classList.add('active');
    
    // Update score display
    const scoreCircle = document.getElementById('scoreCircle');
    const scoreText = document.getElementById('scoreText');
    const scoreMessage = document.getElementById('scoreMessage');
    
    scoreText.textContent = `${score}%`;
    scoreCircle.style.setProperty('--score-deg', `${(score / 100) * 360}deg`);
    
    // Determine message based on score
    let message, color;
    if (score >= 90) {
        message = '🎉 Uitstekend! Je bent goed voorbereid op cybersecurity uitdagingen.';
        color = '#2ecc71';
    } else if (score >= 80) {
        message = '👍 Goed werk! Je hebt een solide basis, maar er is ruimte voor verbetering.';
        color = '#f39c12';
    } else if (score >= 70) {
        message = '📚 Redelijk resultaat. Bestudeer het materiaal nogmaals voor betere kennis.';
        color = '#e67e22';
    } else {
        message = '⚠️ Je score suggereert dat meer studie nodig is. Cybersecurity is cruciaal!';
        color = '#e74c3c';
    }
    
    scoreMessage.textContent = message;
    scoreMessage.style.color = color;
    
    // Show wrong answers if any
    if (wrongAnswers.length > 0) {
        showWrongAnswers();
    }
    
    // Mark quiz as completed
    if (!completedSections.includes('quiz')) {
        completedSections.push('quiz');
        markSectionCompleted('quiz');
    }
}

function showWrongAnswers() {
    const wrongAnswersSection = document.getElementById('wrongAnswersSection');
    const wrongAnswersList = document.getElementById('wrongAnswersList');
    
    let wrongAnswersHTML = '';
    wrongAnswers.forEach((item, index) => {
        wrongAnswersHTML += `
            <div class="wrong-answer-item">
                <h4>❌ Vraag ${index + 1}</h4>
                <p><strong>Vraag:</strong> ${item.question}</p>
                <p><strong>Jouw antwoord:</strong> <span style="color: #e74c3c;">${item.selectedAnswer}</span></p>
                <p><strong>Correct antwoord:</strong> <span style="color: #2ecc71;">${item.correctAnswer}</span></p>
                <div class="info-box">
                    <strong>💡 Uitleg:</strong> ${item.explanation}
                </div>
            </div>
        `;
    });
    
    wrongAnswersList.innerHTML = wrongAnswersHTML;
    wrongAnswersSection.style.display = 'block';
}

function retryQuiz() {
    // Reset quiz state
    wrongAnswers = [];
    
    // Show quiz section again
    document.getElementById('quiz-results').classList.remove('active');
    document.getElementById('quiz-section').classList.add('active');
    
    // Generate new quiz with different questions
    displayQuiz();
}

function restartCourse() {
    // Reset all progress
    currentSection = 'intro';
    completedSections = [];
    quizAttempts = 0;
    wrongAnswers = [];
    usedQuestions = [];
    
    // Reset UI
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('completed', 'active');
    });
    
    document.querySelectorAll('.course-content, .quiz-section, .quiz-results').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show intro
    showSection('intro');
    
    alert('🔄 Cursus is opnieuw gestart. Veel succes met je nieuwe poging!');
}

// Utility functions for enhanced user experience
function checkCompletion() {
    // Check if user has completed all sections
    const requiredSections = sections.slice(0, -1); // All except quiz
    const allCompleted = requiredSections.every(section => completedSections.includes(section));
    
    if (allCompleted && currentSection !== 'quiz') {
        showCompletionPrompt();
    }
}

function showCompletionPrompt() {
    if (confirm('🎓 Je hebt alle modules voltooid! Wil je nu de toets maken?')) {
        showSection('quiz');
    }
}

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) return; // Ignore shortcuts
    
    switch(e.key) {
        case 'ArrowLeft':
            if (currentSection !== 'intro') {
                previousSection();
            }
            break;
        case 'ArrowRight':
            if (currentSection !== 'quiz') {
                nextSection();
            }
            break;
    }
});

// Auto-save progress to localStorage
function saveProgress() {
    const progress = {
        currentSection,
        completedSections,
        quizAttempts,
        usedQuestions
    };
    localStorage.setItem('euramax-course-progress', JSON.stringify(progress));
}

function loadProgress() {
    const saved = localStorage.getItem('euramax-course-progress');
    if (saved) {
        const progress = JSON.parse(saved);
        currentSection = progress.currentSection || 'intro';
        completedSections = progress.completedSections || [];
        quizAttempts = progress.quizAttempts || 0;
        usedQuestions = progress.usedQuestions || [];
        
        // Restore UI state
        completedSections.forEach(section => markSectionCompleted(section));
        showSection(currentSection);
    }
}

// Save progress periodically
setInterval(saveProgress, 30000); // Every 30 seconds

// Load progress on page load
document.addEventListener('DOMContentLoaded', loadProgress);

console.log('Euramax Cybersecurity Course JavaScript loaded successfully');