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
let timeSpent = 0; // in minutes
let sessionStartTime = Date.now();
let sectionStartTime = Date.now();
let bookmarks = [];

// Course sections in order
const sections = ['intro', 'phishing', 'passwords', 'malware', 'social', 'data', 'quiz', 'phishing-demo'];

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

// Initialize the course with enhanced progress tracking
document.addEventListener('DOMContentLoaded', function() {
    loadProgress();
    updateProgress();
    updateProgressDashboard();
    updateNavigation();
    updateTimeSpent();
    initializeLearningPath();
    initializeAchievements();
    console.log('Euramax Cybersecurity Course initialized with enhanced tracking');
});

// Learning Path Indicator
function initializeLearningPath() {
    const pathIndicator = document.getElementById('pathIndicator');
    const sectionIcons = ['🏁', '📧', '🔐', '🦠', '👥', '💾', '📝'];
    const sectionNames = ['Intro', 'Phishing', 'Passwords', 'Malware', 'Social', 'Data', 'Quiz'];
    
    pathIndicator.innerHTML = sections.map((section, index) => {
        const isCompleted = completedSections.includes(section);
        const isCurrent = section === currentSection;
        const isAccessible = index === 0 || completedSections.includes(sections[index - 1]);
        
        return `
            <div class="path-step ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''} ${isAccessible ? 'accessible' : 'locked'}" 
                 data-section="${section}" style="cursor: pointer;">
                <div class="path-icon">${sectionIcons[index]}</div>
                <div class="path-name">${sectionNames[index]}</div>
                ${index < sections.length - 1 ? '<div class="path-connector"></div>' : ''}
            </div>
        `;
    }).join('');
    
    // Add click handlers for accessible steps
    pathIndicator.querySelectorAll('.path-step.accessible').forEach(step => {
        step.addEventListener('click', () => {
            const section = step.dataset.section;
            showSection(section);
        });
    });
}

function updateLearningPath() {
    const pathSteps = document.querySelectorAll('.path-step');
    
    pathSteps.forEach((step, index) => {
        const section = sections[index];
        const isCompleted = completedSections.includes(section);
        const isCurrent = section === currentSection;
        const isAccessible = index === 0 || completedSections.includes(sections[index - 1]);
        
        step.className = `path-step ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''} ${isAccessible ? 'accessible' : 'locked'}`;
        
        // Update click handler
        if (isAccessible) {
            step.style.cursor = 'pointer';
            step.onclick = () => showSection(section);
        } else {
            step.style.cursor = 'not-allowed';
            step.onclick = null;
        }
    });
}

// Achievement System
function initializeAchievements() {
    const achievements = [
        { id: 'first-step', name: 'Eerste Stap', icon: '🚀', description: 'Cursus gestart' },
        { id: 'halfway', name: 'Halverwege', icon: '⚡', description: '50% voltooid' },
        { id: 'speed-demon', name: 'Snelle Leerling', icon: '💨', description: 'Module in <5 min' },
        { id: 'perfect-score', name: 'Perfectionist', icon: '🏆', description: '100% op toets' },
        { id: 'completed', name: 'Afgerond', icon: '🎓', description: 'Cursus voltooid' }
    ];
    
    // Load existing achievements
    const earned = JSON.parse(localStorage.getItem('euramax-achievements') || '[]');
    earned.forEach(achievementId => {
        showAchievementBadge(achievements.find(a => a.id === achievementId));
    });
}

function earnAchievement(achievementId) {
    const earned = JSON.parse(localStorage.getItem('euramax-achievements') || '[]');
    if (earned.includes(achievementId)) return;
    
    earned.push(achievementId);
    localStorage.setItem('euramax-achievements', JSON.stringify(earned));
    
    const achievements = [
        { id: 'first-step', name: 'Eerste Stap', icon: '🚀', description: 'Cursus gestart' },
        { id: 'halfway', name: 'Halverwege', icon: '⚡', description: '50% voltooid' },
        { id: 'speed-demon', name: 'Snelle Leerling', icon: '💨', description: 'Module in <5 min' },
        { id: 'perfect-score', name: 'Perfectionist', icon: '🏆', description: '100% op toets' },
        { id: 'completed', name: 'Afgerond', icon: '🎓', description: 'Cursus voltooid' }
    ];
    
    const achievement = achievements.find(a => a.id === achievementId);
    if (achievement) {
        showAchievementBadge(achievement);
        showAchievementNotification(achievement);
    }
}

function showAchievementBadge(achievement) {
    const badgesContainer = document.getElementById('achievementBadges');
    const badge = document.createElement('div');
    badge.className = 'achievement-badge';
    badge.style.cssText = `
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
        animation: badgeEarn 0.5s ease-out;
    `;
    badge.innerHTML = `${achievement.icon} ${achievement.name}`;
    badge.title = achievement.description;
    badgesContainer.appendChild(badge);
}

function showAchievementNotification(achievement) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(243, 156, 18, 0.3);
        z-index: 10000;
        animation: achievementSlide 3s ease-out forwards;
    `;
    
    notification.innerHTML = `
        <div style="font-weight: bold; display: flex; align-items: center; gap: 0.5rem;">
            ${achievement.icon} Achievement Unlocked!
        </div>
        <div style="margin-top: 0.25rem; font-size: 0.9rem;">
            ${achievement.name} - ${achievement.description}
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Add animation styles if not exist
    if (!document.getElementById('achievement-styles')) {
        const style = document.createElement('style');
        style.id = 'achievement-styles';
        style.textContent = `
            @keyframes achievementSlide {
                0% { transform: translateX(100%); opacity: 0; }
                20% { transform: translateX(0); opacity: 1; }
                80% { transform: translateX(0); opacity: 1; }
                100% { transform: translateX(100%); opacity: 0; }
            }
            @keyframes badgeEarn {
                0% { transform: scale(0); opacity: 0; }
                50% { transform: scale(1.2); opacity: 1; }
                100% { transform: scale(1); opacity: 1; }
            }
            .path-step {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 0.5rem;
                border-radius: 8px;
                transition: all 0.3s ease;
                min-width: 60px;
                position: relative;
            }
            .path-step.completed {
                background: rgba(46, 204, 113, 0.1);
                color: #27ae60;
            }
            .path-step.current {
                background: rgba(102, 126, 234, 0.1);
                color: #667eea;
                transform: scale(1.1);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
            }
            .path-step.locked {
                opacity: 0.5;
                color: #7f8c8d;
            }
            .path-step.accessible:hover {
                background: rgba(0, 0, 0, 0.05);
                transform: scale(1.05);
            }
            .path-icon {
                font-size: 1.2rem;
                margin-bottom: 0.25rem;
            }
            .path-name {
                font-size: 0.7rem;
                text-align: center;
                font-weight: 500;
            }
            .path-connector {
                position: absolute;
                right: -0.75rem;
                top: 50%;
                transform: translateY(-50%);
                width: 1rem;
                height: 2px;
                background: #ddd;
            }
            .path-step.completed .path-connector {
                background: #27ae60;
            }
        `;
        document.head.appendChild(style);
    }
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Navigation functions with enhanced transitions
function showSection(sectionId, direction = 'forward') {
    const currentActiveSection = document.querySelector('.course-content.active, .quiz-section.active, .quiz-results.active');
    const targetSection = document.getElementById(sectionId);
    
    if (!targetSection) return;
    
    // Add slide-out animation to current section
    if (currentActiveSection && currentActiveSection !== targetSection) {
        currentActiveSection.classList.add(direction === 'forward' ? 'slide-out' : 'slide-in');
        
        setTimeout(() => {
            // Hide all sections
            document.querySelectorAll('.course-content, .quiz-section, .quiz-results').forEach(section => {
                section.classList.remove('active', 'slide-out', 'slide-in');
            });
            
            // Show target section with slide-in animation
            targetSection.classList.add('active');
            if (direction === 'forward') {
                targetSection.classList.add('slide-in');
            }
            
            // Remove animation classes after transition
            setTimeout(() => {
                targetSection.classList.remove('slide-in', 'slide-out');
            }, 400);
        }, 200);
    } else {
        // First time or same section - no animation needed
        document.querySelectorAll('.course-content, .quiz-section, .quiz-results').forEach(section => {
            section.classList.remove('active');
        });
        targetSection.classList.add('active');
    }
    
    // Update menu items with enhanced animations
    updateMenuItems(sectionId);
    
    currentSection = sectionId;
    
    // Track section changes for time measurement
    sectionStartTime = Date.now();
    
    // Special handling for quiz section
    if (sectionId === 'quiz') {
        initializeQuiz();
    }
    
    updateProgress();
    updateProgressDashboard();
    updateNavigation();
    saveProgress();
    
    // Add scroll to top with smooth behavior
    setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 300);
}

function updateMenuItems(activeSectionId) {
    document.querySelectorAll('.menu-item').forEach((item, index) => {
        item.classList.remove('active');
        
        // Add stagger animation effect
        setTimeout(() => {
            if (sections[index] === activeSectionId) {
                item.classList.add('active');
            }
        }, index * 50);
    });
}

function nextSection() {
    const currentIndex = sections.indexOf(currentSection);
    if (currentIndex < sections.length - 1) {
        // Mark current section as completed with celebration
        if (!completedSections.includes(currentSection)) {
            completedSections.push(currentSection);
            markSectionCompleted(currentSection);
            showCompletionCelebration(currentSection);
        }
        
        const nextSectionId = sections[currentIndex + 1];
        showSection(nextSectionId, 'forward');
        
        // Update progress dashboard
        updateProgressDashboard();
        saveProgress();
    }
}

function previousSection() {
    const currentIndex = sections.indexOf(currentSection);
    if (currentIndex > 0) {
        const prevSectionId = sections[currentIndex - 1];
        showSection(prevSectionId, 'backward');
    }
}

function showCompletionCelebration(sectionId) {
    // Create a temporary celebration element
    const celebration = document.createElement('div');
    celebration.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(46, 204, 113, 0.3);
        z-index: 10000;
        font-size: 1.1rem;
        font-weight: bold;
        opacity: 0;
        animation: celebrationPop 2s ease-out forwards;
        pointer-events: none;
    `;
    
    const sectionName = getSectionName(sectionId);
    celebration.innerHTML = `
        🎉 ${sectionName} voltooid!
        <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
            Goed gedaan! Ga door naar de volgende module.
        </div>
    `;
    
    document.body.appendChild(celebration);
    
    // Add celebration animation styles if not exist
    if (!document.getElementById('celebration-styles')) {
        const style = document.createElement('style');
        style.id = 'celebration-styles';
        style.textContent = `
            @keyframes celebrationPop {
                0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
                20% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
                30% { transform: translate(-50%, -50%) scale(1); }
                100% { opacity: 0; transform: translate(-50%, -50%) scale(1); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Remove after animation
    setTimeout(() => {
        if (celebration.parentNode) {
            celebration.parentNode.removeChild(celebration);
        }
    }, 2000);
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
        // Animate progress bar with easing
        setTimeout(() => {
            progressBar.style.width = `${progress}%`;
        }, 100);
    }
}

function markSectionCompleted(sectionId) {
    const menuItems = document.querySelectorAll('.menu-item');
    const sectionIndex = sections.indexOf(sectionId);
    
    if (sectionIndex !== -1 && menuItems[sectionIndex]) {
        // Add completion animation
        const menuItem = menuItems[sectionIndex];
        menuItem.style.transform = 'scale(1.1)';
        
        setTimeout(() => {
            menuItem.classList.add('completed');
            menuItem.style.transform = '';
        }, 200);
    }
    
    // Update status indicator with animation
    const statusElement = document.getElementById(`status-${sectionId}`);
    if (statusElement) {
        statusElement.style.transform = 'scale(1.3)';
        setTimeout(() => {
            statusElement.textContent = '✅';
            statusElement.className = 'module-status completed';
            statusElement.style.transform = '';
        }, 150);
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
    
    // Save quiz score for progress tracking
    localStorage.setItem('last-quiz-score', score);
    
    // Update score display
    const scoreCircle = document.getElementById('scoreCircle');
    const scoreText = document.getElementById('scoreText');
    const scoreMessage = document.getElementById('scoreMessage');
    
    scoreText.textContent = `${score}%`;
    scoreCircle.style.setProperty('--score-deg', `${(score / 100) * 360}deg`);
    
    // Generate AI-style personalized feedback based on performance
    const feedback = generateAIFeedback(score, correct, total, wrongAnswers);
    
    scoreMessage.innerHTML = feedback.message;
    scoreMessage.style.color = feedback.color;
    
    // Show personalized learning recommendations
    showPersonalizedRecommendations(score, wrongAnswers);
    
    // Show wrong answers with enhanced AI feedback if any
    if (wrongAnswers.length > 0) {
        showWrongAnswersWithAI();
    }
    
    // Mark quiz as completed and update progress
    if (!completedSections.includes('quiz')) {
        completedSections.push('quiz');
        markSectionCompleted('quiz');
    }
    
    updateProgressDashboard();
    saveProgress();
}

// AI-Generated Feedback System (Killer Feature)
function generateAIFeedback(score, correct, total, wrongAnswers) {
    const weakAreas = analyzeWeakAreas(wrongAnswers);
    const timeEfficiency = analyzeTimeEfficiency();
    
    let message, color;
    
    if (score >= 90) {
        message = `🎉 <strong>Uitstekend presteren!</strong><br>
                   Je toont een diep begrip van cybersecurity principes. Je hebt ${correct}/${total} vragen correct beantwoord.<br>
                   <em>AI-analyse: Je reactiesnelheid en nauwkeurigheid duiden op sterke risicoherkenning.</em>`;
        color = '#2ecc71';
    } else if (score >= 80) {
        message = `👍 <strong>Goed gefundeerde kennis!</strong><br>
                   Je beheerst de basis goed met ${correct}/${total} correcte antwoorden.<br>
                   <em>AI-suggestie: ${generateSpecificAdvice(weakAreas)}</em>`;
        color = '#f39c12';
    } else if (score >= 70) {
        message = `📚 <strong>Basis aanwezig, verdieping nodig</strong><br>
                   ${correct}/${total} correct. ${generateLearningPath(weakAreas)}<br>
                   <em>AI-focus: Concentreer je op praktische herkenning van bedreigingen.</em>`;
        color = '#e67e22';
    } else {
        message = `⚠️ <strong>Verhoogde aandacht vereist</strong><br>
                   Met ${correct}/${total} correcte antwoorden is extra training essentieel.<br>
                   <em>AI-prioriteit: ${generateUrgentRecommendations(weakAreas)}</em>`;
        color = '#e74c3c';
    }
    
    return { message, color };
}

function analyzeWeakAreas(wrongAnswers) {
    const categories = {
        phishing: 0,
        passwords: 0,
        malware: 0,
        social: 0,
        data: 0,
        advanced: 0
    };
    
    wrongAnswers.forEach(answer => {
        if (categories.hasOwnProperty(answer.category)) {
            categories[answer.category]++;
        }
    });
    
    return Object.entries(categories)
        .filter(([category, count]) => count > 0)
        .sort((a, b) => b[1] - a[1])
        .map(([category, count]) => ({ category, count }));
}

function analyzeTimeEfficiency() {
    // Simple time analysis based on total time spent
    return timeSpent < 30 ? 'snel' : timeSpent > 60 ? 'grondig' : 'gemiddeld';
}

function generateSpecificAdvice(weakAreas) {
    if (weakAreas.length === 0) return "Behoud je uitstekende vorm door regelmatig te oefenen.";
    
    const primaryWeak = weakAreas[0];
    const adviceMap = {
        phishing: "Focus op het herkennen van subtiele phishing-technieken en URL-verificatie.",
        passwords: "Bestudeer geavanceerde wachtwoordstrategieën en multi-factor authenticatie.",
        malware: "Verdiep je kennis over malware-detectie en incident response procedures.",
        social: "Oefen met het herkennen van sociale manipulatietechnieken.",
        data: "Bestudeer GDPR-compliance en data-classificatiesystemen.",
        advanced: "Focus op geavanceerde bedreigingen zoals APT-aanvallen."
    };
    
    return adviceMap[primaryWeak.category] || "Herhaal de basisprincipes van cybersecurity.";
}

function generateLearningPath(weakAreas) {
    if (weakAreas.length === 0) return "Herhaal alle modules voor een sterke basis.";
    
    const paths = weakAreas.slice(0, 2).map(area => {
        const sectionMap = {
            phishing: "📧 Phishing module",
            passwords: "🔐 Wachtwoord module", 
            malware: "🦠 Malware module",
            social: "👥 Social Engineering module",
            data: "💾 Data Bescherming module",
            advanced: "🎯 Geavanceerde bedreigingen"
        };
        return sectionMap[area.category];
    });
    
    return `Bestudeer vooral: ${paths.join(" en ")}.`;
}

function generateUrgentRecommendations(weakAreas) {
    const categories = weakAreas.map(area => area.category);
    
    if (categories.includes('phishing')) {
        return "Begin met phishing-herkenning - dit is de meest voorkomende bedreiging.";
    } else if (categories.includes('passwords')) {
        return "Start met wachtwoordbeveiliging - de basis van digitale veiligheid.";
    } else {
        return "Neem alle modules systematisch door, beginnend bij de basis.";
    }
}

function showPersonalizedRecommendations(score, wrongAnswers) {
    const weakAreas = analyzeWeakAreas(wrongAnswers);
    let recommendationsHTML = `
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">🤖 AI-Gepersonaliseerde Aanbevelingen</h4>
    `;
    
    if (score >= 80) {
        recommendationsHTML += `
            <div style="margin-bottom: 1rem;">
                <strong>🎯 Vervolgstappen voor experts:</strong>
                <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                    <li>Deel je kennis met collega's door een mini-presentatie te geven</li>
                    <li>Meld je aan voor geavanceerde cybersecurity certificeringen</li>
                    <li>Word cybersecurity champion in je team</li>
                </ul>
            </div>
        `;
    } else {
        recommendationsHTML += `
            <div style="margin-bottom: 1rem;">
                <strong>📚 Aanbevolen leerpad:</strong>
                <ol style="margin: 0.5rem 0; padding-left: 1.5rem;">
        `;
        
        if (weakAreas.length > 0) {
            weakAreas.slice(0, 3).forEach((area, index) => {
                const priorityMap = {
                    phishing: "Bestudeer phishing-voorbeelden uit het echte leven",
                    passwords: "Oefen met het maken van sterke wachtwoorden",
                    malware: "Leer malware-typen en preventiemethoden",
                    social: "Herken sociale manipulatietechnieken",
                    data: "Begrijp data-classificatie en bescherming"
                };
                
                recommendationsHTML += `<li>${priorityMap[area.category] || 'Herhaal deze module'}</li>`;
            });
        } else {
            recommendationsHTML += `<li>Herhaal alle modules systematisch</li>`;
        }
        
        recommendationsHTML += `
                    <li>Neem de toets opnieuw af over een week</li>
                    <li>Bespreek twijfels met je manager of IT-afdeling</li>
                </ol>
            </div>
        `;
    }
    
    // Add simulated phishing test offer (part of killer feature)
    recommendationsHTML += `
        <div style="background: #e8f4ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #3498db;">
            <strong>🎮 Interactieve Training Beschikbaar:</strong><br>
            <em>Wil je je vaardigheden testen met een gesimuleerde phishing test? Deze realistische oefening helpt je bedreigingen te herkennen in een veilige omgeving.</em>
            <br><br>
            <button onclick="startPhishingSimulation()" class="btn" style="margin-top: 0.5rem;">
                🎯 Start Phishing Simulatie
            </button>
        </div>
    `;
    
    recommendationsHTML += `</div>`;
    
    // Insert recommendations before wrong answers section
    const quizResults = document.getElementById('quiz-results');
    const existingRecommendations = document.getElementById('ai-recommendations');
    
    if (existingRecommendations) {
        existingRecommendations.innerHTML = recommendationsHTML;
    } else {
        const div = document.createElement('div');
        div.id = 'ai-recommendations';
        div.innerHTML = recommendationsHTML;
        quizResults.insertBefore(div, quizResults.children[1]);
    }
}

function showWrongAnswersWithAI() {
    const wrongAnswersSection = document.getElementById('wrongAnswersSection');
    const wrongAnswersList = document.getElementById('wrongAnswersList');
    
    let wrongAnswersHTML = '';
    wrongAnswers.forEach((item, index) => {
        const aiInsight = generateAIInsightForAnswer(item);
        
        wrongAnswersHTML += `
            <div class="wrong-answer-item">
                <h4>❌ Vraag ${index + 1}</h4>
                <p><strong>Vraag:</strong> ${item.question}</p>
                <p><strong>Jouw antwoord:</strong> <span style="color: #e74c3c;">${item.selectedAnswer}</span></p>
                <p><strong>Correct antwoord:</strong> <span style="color: #2ecc71;">${item.correctAnswer}</span></p>
                
                <div class="info-box">
                    <strong>💡 Uitleg:</strong> ${item.explanation}
                </div>
                
                <div style="background: #f0f8ff; padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #3498db;">
                    <strong>🤖 AI-Inzicht:</strong> ${aiInsight}
                </div>
            </div>
        `;
    });
    
    wrongAnswersList.innerHTML = wrongAnswersHTML;
    wrongAnswersSection.style.display = 'block';
}

function generateAIInsightForAnswer(wrongAnswer) {
    const insights = {
        phishing: [
            "Dit type vraag test je vermogen om subtiele verschillen in URLs en e-mailadressen te herkennen. Focus op domeinverificatie.",
            "Phishing-aanvallen gebruiken vaak urgentie als psychologische druk. Leer om te pauzeren bij 'urgente' verzoeken.",
            "De beste verdediging tegen phishing is directe verificatie via bekende kanalen, niet via de verdachte e-mail zelf."
        ],
        passwords: [
            "Wachtwoordbeveiliging gaat verder dan complexiteit - uniekheid en lengte zijn vaak belangrijker.",
            "Moderne aanvallers gebruiken geavanceerde technieken. Een sterk wachtwoordbeleid beschermt tegen deze bedreigingen.",
            "Multi-factor authenticatie is je beste verdediging, zelfs als wachtwoorden gecompromitteerd zijn."
        ],
        malware: [
            "Malware-detectie vereist voorzichtigheid bij onbekende bestanden en bronnen. Vertrouw op je instinct.",
            "Snelle reactie bij malware-verdenking kan schade beperken. Isolatie is altijd de eerste stap.",
            "Moderne malware kan erg subtiel zijn. Regelmatige scans en updates zijn essentieel."
        ],
        social: [
            "Social engineering exploiteert menselijke emoties. Bewustwording van manipulatietechnieken is je beste bescherming.",
            "Verificatie van identiteit via onafhankelijke kanalen voorkomt de meeste social engineering aanvallen.",
            "Gezonde scepsis bij onverwachte verzoeken, zelfs van bekenden, beschermt tegen manipulatie."
        ],
        data: [
            "Data-bescherming begint bij classificatie. Weet welke data gevoelig is en hoe deze beschermd moet worden.",
            "GDPR-compliance is niet alleen wet, maar ook beste praktijk voor data-beveiliging.",
            "Principes van 'privacy by design' integreren beveiliging in alle processen."
        ]
    };
    
    const categoryInsights = insights[wrongAnswer.category] || insights.phishing;
    return categoryInsights[Math.floor(Math.random() * categoryInsights.length)];
}

// Phishing Simulation Feature (Part of Killer Feature)
function startPhishingSimulation() {
    const simulationContent = `
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); max-width: 800px; margin: 2rem auto;">
            <h2 style="color: #2c3e50; text-align: center; margin-bottom: 2rem;">
                🎮 Phishing Simulatie Training
            </h2>
            
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
                <strong>⚠️ Veilige Oefenomgeving</strong><br>
                Deze simulatie toont realistische phishing-voorbeelden in een veilige omgeving. Alle links en acties zijn gedeactiveerd.
            </div>
            
            <div id="phishing-examples">
                <h3>📧 Voorbeeld 1: Verdachte Bankmail</h3>
                <div style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 1rem; border-radius: 8px; font-family: monospace; margin: 1rem 0;">
                    <strong>Van:</strong> security@ing-banknl.com<br>
                    <strong>Onderwerp:</strong> URGENT: Uw rekening wordt geblokkeerd<br><br>
                    Beste klant,<br><br>
                    We hebben verdachte activiteit gedetecteerd op uw rekening. Klik onmiddellijk op onderstaande link om uw account te verifiëren, anders wordt deze binnen 24 uur geblokkeerd.<br><br>
                    <a href="#" style="color: #007bff; text-decoration: underline;">[GEBLOKKEERDE LINK] Verifieer Account</a><br><br>
                    Met vriendelijke groet,<br>
                    ING Beveiligingsteam
                </div>
                
                <div style="background: #f0f8ff; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>🔍 Wat zie je voor verdachte elementen?</strong>
                    <div style="margin-top: 1rem;">
                        <label style="display: block; margin: 0.5rem 0;">
                            <input type="checkbox" onchange="checkPhishingElement(this, true)"> Domein verschilt subtiel van echte ING (ing-banknl.com vs ing.nl)
                        </label>
                        <label style="display: block; margin: 0.5rem 0;">
                            <input type="checkbox" onchange="checkPhishingElement(this, true)"> Urgentie wordt gebruikt om druk te creëren
                        </label>
                        <label style="display: block; margin: 0.5rem 0;">
                            <input type="checkbox" onchange="checkPhishingElement(this, false)"> De Nederlandse taal lijkt correct
                        </label>
                        <label style="display: block; margin: 0.5rem 0;">
                            <input type="checkbox" onchange="checkPhishingElement(this, true)"> Link vraagt om directe actie zonder verificatie
                        </label>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 2rem;">
                <button onclick="closePhishingSimulation()" class="btn">
                    ✅ Simulatie Voltooien
                </button>
            </div>
        </div>
        
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;" id="simulation-overlay"></div>
    `;
    
    const overlay = document.createElement('div');
    overlay.innerHTML = simulationContent;
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.zIndex = '1001';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.padding = '2rem';
    overlay.style.overflowY = 'auto';
    overlay.id = 'phishing-simulation';
    
    document.body.appendChild(overlay);
}

function checkPhishingElement(checkbox, isCorrect) {
    const label = checkbox.parentElement;
    if (checkbox.checked) {
        if (isCorrect) {
            label.style.background = '#d4edda';
            label.style.color = '#155724';
            label.style.padding = '0.5rem';
            label.style.borderRadius = '4px';
            label.style.border = '1px solid #c3e6cb';
        } else {
            label.style.background = '#f8d7da';
            label.style.color = '#721c24';
            label.style.padding = '0.5rem';
            label.style.borderRadius = '4px';
            label.style.border = '1px solid #f5c6cb';
        }
    } else {
        label.style.background = '';
        label.style.color = '';
        label.style.padding = '';
        label.style.borderRadius = '';
        label.style.border = '';
    }
}

function closePhishingSimulation() {
    const simulation = document.getElementById('phishing-simulation');
    if (simulation) {
        simulation.remove();
    }
    
    // Add completion badge/achievement
    if (!bookmarks.find(b => b.id === 'phishing-simulation')) {
        bookmarks.push({
            id: 'phishing-simulation',
            title: '🎮 Phishing Simulatie Voltooid',
            section: 'achievements',
            timestamp: Date.now()
        });
        updateBookmarksList();
        saveProgress();
    }
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

// Enhanced keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) return; // Ignore shortcuts
    
    // Don't interfere when user is typing in inputs
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    switch(e.key) {
        case 'ArrowLeft':
        case 'ArrowUp':
            e.preventDefault();
            if (currentSection !== 'intro') {
                previousSection();
            }
            break;
        case 'ArrowRight':
        case 'ArrowDown':
            e.preventDefault();
            if (currentSection !== sections[sections.length - 1]) {
                nextSection();
            }
            break;
        case ' ': // Spacebar
            e.preventDefault();
            if (currentSection !== sections[sections.length - 1]) {
                nextSection();
            }
            break;
        case 'Home':
            e.preventDefault();
            showSection('intro');
            break;
        case 'End':
            e.preventDefault();
            if (completedSections.length >= sections.length - 2) {
                showSection('quiz');
            }
            break;
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
            e.preventDefault();
            const sectionIndex = parseInt(e.key) - 1;
            if (sectionIndex < sections.length - 1) {
                showSection(sections[sectionIndex]);
            }
            break;
    }
});

// Add keyboard hints
function showKeyboardHints() {
    const hints = document.createElement('div');
    hints.id = 'keyboard-hints';
    hints.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-size: 0.8rem;
        z-index: 1000;
        max-width: 200px;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    hints.innerHTML = `
        <div style="font-weight: bold; margin-bottom: 0.5rem;">⌨️ Sneltoetsen</div>
        <div>← → : Navigeren</div>
        <div>Spatie : Volgende</div>
        <div>1-6 : Direct naar module</div>
        <div>Home : Naar begin</div>
    `;
    
    document.body.appendChild(hints);
    
    // Show hints briefly on page load
    setTimeout(() => {
        hints.style.opacity = '1';
        setTimeout(() => {
            hints.style.opacity = '0';
        }, 3000);
    }, 2000);
}

// Initialize keyboard hints
document.addEventListener('DOMContentLoaded', function() {
    showKeyboardHints();
});

// Auto-save progress to localStorage with enhanced data
function saveProgress() {
    const currentTime = Date.now();
    timeSpent += Math.round((currentTime - sectionStartTime) / 60000); // Convert to minutes
    sectionStartTime = currentTime;
    
    const progress = {
        currentSection,
        completedSections,
        quizAttempts,
        usedQuestions,
        timeSpent,
        bookmarks,
        lastSaved: currentTime
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
        timeSpent = progress.timeSpent || 0;
        bookmarks = progress.bookmarks || [];
        
        // Restore UI state
        completedSections.forEach(section => markSectionCompleted(section));
        updateBookmarksList();
        showSection(currentSection);
    }
}

// Enhanced progress dashboard update
function updateProgressDashboard() {
    const progressPercent = Math.round((completedSections.length / (sections.length - 1)) * 100);
    const completedCount = completedSections.length;
    const totalModules = sections.length - 1; // Exclude quiz from modules count
    
    document.getElementById('progressText').textContent = `${progressPercent}% voltooid`;
    document.getElementById('completedModules').textContent = `${completedCount}/${totalModules} modules`;
    document.getElementById('timeSpent').textContent = `Tijd besteed: ${timeSpent} min`;
    
    // Update quiz score if available
    const quizElement = document.getElementById('quizScore');
    if (quizAttempts > 0) {
        const lastScore = localStorage.getItem('last-quiz-score');
        if (lastScore) {
            quizElement.textContent = `Toets: ${lastScore}% behaald`;
        }
    }
    
    // Update module status indicators
    sections.forEach(section => {
        const statusElement = document.getElementById(`status-${section}`);
        if (statusElement) {
            if (completedSections.includes(section)) {
                statusElement.textContent = '✅';
                statusElement.className = 'module-status completed';
            } else if (section === currentSection) {
                statusElement.textContent = '🔄';
                statusElement.className = 'module-status in-progress';
            } else {
                statusElement.textContent = '';
                statusElement.className = 'module-status';
            }
        }
    });
    
    // Update learning path
    updateLearningPath();
    
    // Check for achievements
    checkAchievements();
}

function checkAchievements() {
    // First step achievement
    if (completedSections.length >= 1) {
        earnAchievement('first-step');
    }
    
    // Halfway achievement
    if (completedSections.length >= Math.ceil((sections.length - 1) / 2)) {
        earnAchievement('halfway');
    }
    
    // Speed demon (module completed in less than 5 minutes)
    if (timeSpent <= 5 && completedSections.length > 0) {
        earnAchievement('speed-demon');
    }
    
    // Course completed
    if (completedSections.length >= sections.length - 1) {
        earnAchievement('completed');
    }
    
    // Perfect score (checked in quiz results)
    const lastScore = localStorage.getItem('last-quiz-score');
    if (lastScore && parseInt(lastScore) === 100) {
        earnAchievement('perfect-score');
    }
}

// Time tracking
function updateTimeSpent() {
    setInterval(() => {
        const currentTime = Date.now();
        timeSpent += Math.round((currentTime - sectionStartTime) / 60000);
        sectionStartTime = currentTime;
        document.getElementById('timeSpent').textContent = `Tijd besteed: ${timeSpent} min`;
        saveProgress();
    }, 60000); // Update every minute
}

// Bookmark functionality
function toggleBookmark(id, title) {
    const existingIndex = bookmarks.findIndex(b => b.id === id);
    
    if (existingIndex !== -1) {
        // Remove bookmark
        bookmarks.splice(existingIndex, 1);
        document.getElementById(`bookmark-${id}`).classList.remove('bookmarked');
    } else {
        // Add bookmark
        bookmarks.push({
            id: id,
            title: title,
            section: currentSection,
            timestamp: Date.now()
        });
        document.getElementById(`bookmark-${id}`).classList.add('bookmarked');
    }
    
    updateBookmarksList();
    saveProgress();
}

function updateBookmarksList() {
    const bookmarksList = document.getElementById('bookmarksList');
    
    if (bookmarks.length === 0) {
        bookmarksList.innerHTML = '<p style="color: #7f8c8d; font-size: 0.9rem;">Nog geen bladwijzers toegevoegd</p>';
        return;
    }
    
    let bookmarkHTML = '';
    bookmarks.forEach(bookmark => {
        bookmarkHTML += `
            <div class="bookmark-item" onclick="jumpToBookmark('${bookmark.id}', '${bookmark.section}')">
                🔖 ${bookmark.title}
                <small style="display: block; color: #7f8c8d;">${getSectionName(bookmark.section)}</small>
            </div>
        `;
    });
    
    bookmarksList.innerHTML = bookmarkHTML;
    
    // Update bookmark button states
    bookmarks.forEach(bookmark => {
        const bookmarkBtn = document.getElementById(`bookmark-${bookmark.id}`);
        if (bookmarkBtn) {
            bookmarkBtn.classList.add('bookmarked');
        }
    });
}

function jumpToBookmark(bookmarkId, section) {
    showSection(section);
    setTimeout(() => {
        const element = document.getElementById(`bookmark-${bookmarkId}`);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Highlight the bookmarked section briefly
            const parent = element.closest('h2, h3, h4');
            if (parent) {
                parent.style.background = '#fff3cd';
                setTimeout(() => {
                    parent.style.background = '';
                }, 2000);
            }
        }
    }, 300);
}

function getSectionName(section) {
    const sectionNames = {
        'intro': 'Introductie',
        'phishing': 'Phishing & Email Beveiliging',
        'passwords': 'Wachtwoord Beveiliging',
        'malware': 'Malware & Ransomware',
        'social': 'Social Engineering',
        'data': 'Data Bescherming',
        'quiz': 'Toets',
        'phishing-demo': 'Live Phishing Simulation Demo'
    };
    return sectionNames[section] || section;
}

// Live Phishing Simulation Demo Functionality
let demoState = {
    currentEmailIndex: 0,
    emailsAnalyzed: 0,
    threatsDetected: 0,
    startTime: null,
    isActive: false
};

// Sample phishing emails for demonstration
const phishingDemoEmails = [
    {
        id: 1,
        from: "security@banknl-verificatie.com",
        subject: "URGENT: Account Verification Required",
        body: `Dear Customer,

We have detected suspicious activity on your account. For your security, we need you to verify your identity immediately.

Click here to verify your account: https://banknl-secure.com/verify?token=abc123

If you do not verify within 24 hours, your account will be suspended.

Best regards,
Security Team
Bank Nederland`,
        threatLevel: "critical",
        indicators: [
            "Suspicious domain (banknl-verificatie.com instead of official domain)",
            "Generic greeting ('Dear Customer')",
            "Urgency tactics ('URGENT', '24 hours')",
            "Suspicious verification link",
            "Threatening language about account suspension"
        ],
        confidence: 0.95,
        recommendations: [
            "Block sender domain immediately",
            "Quarantine email and prevent delivery",
            "Alert security team about phishing campaign",
            "Train users about this attack pattern",
            "Implement additional domain filtering"
        ]
    },
    {
        id: 2,
        from: "hr@euramax.eu",
        subject: "New Employee Benefits Document",
        body: `Hi there,

Please find attached the updated employee benefits document. You need to fill it out and return it by Friday.

The document contains sensitive HR information, so please ensure you're logged into the secure portal when opening it.

Download document: https://euramax-hr.secure-docs.eu/benefits.pdf

Thanks,
HR Department`,
        threatLevel: "high",
        indicators: [
            "Domain spoofing (euramax-hr.secure-docs.eu)",
            "Request for sensitive information",
            "External download link masquerading as internal",
            "Social engineering using HR context",
            "Time pressure ('by Friday')"
        ],
        confidence: 0.87,
        recommendations: [
            "Verify with HR department via phone",
            "Block suspicious domain",
            "Scan download link for malware",
            "Implement sender verification policies",
            "Educate staff about HR impersonation"
        ]
    },
    {
        id: 3,
        from: "it-support@microsoft.com",
        subject: "Office 365 License Expiring Today",
        body: `Microsoft Office User,

Your Office 365 license is expiring today. To avoid interruption of service, please renew immediately.

Click here to renew: https://office365-renewal.microsoft-security.net/renew

Your current license details:
- User: [Your Email]
- License Type: Office 365 Business Premium
- Expiry: Today

Microsoft Support Team`,
        threatLevel: "medium",
        indicators: [
            "Suspicious renewal domain (microsoft-security.net)",
            "Generic addressing ('Microsoft Office User')",
            "Fake urgency ('expiring today')",
            "Credential harvesting attempt",
            "Impersonating Microsoft support"
        ],
        confidence: 0.78,
        recommendations: [
            "Verify Office 365 status through official portal",
            "Report phishing attempt to Microsoft",
            "Block fraudulent domain",
            "Educate users about license scams",
            "Implement multi-factor authentication"
        ]
    }
];

function startPhishingDemo() {
    demoState = {
        currentEmailIndex: 0,
        emailsAnalyzed: 0,
        threatsDetected: 0,
        startTime: Date.now(),
        isActive: true
    };
    
    updateDemoProgress(10, "Initializing AI threat detection engine...");
    
    setTimeout(() => {
        updateDemoProgress(25, "Loading machine learning models...");
        setTimeout(() => {
            updateDemoProgress(50, "Ready for email analysis");
            loadCurrentEmail();
        }, 1000);
    }, 800);
}

function loadCurrentEmail() {
    const email = phishingDemoEmails[demoState.currentEmailIndex];
    const emailContainer = document.getElementById('demoEmailContainer');
    const currentEmailDemo = document.getElementById('currentEmailDemo');
    
    emailContainer.innerHTML = `
        <div class="email-header">
            <div><strong>From:</strong> <span class="email-from">${email.from}</span></div>
            <div><strong>Subject:</strong> <span class="email-subject">${email.subject}</span></div>
            <div><strong>Received:</strong> ${new Date().toLocaleString('nl-NL')}</div>
        </div>
        <div class="email-body">
            ${email.body.replace(/\n/g, '<br>').replace(/(https?:\/\/[^\s]+)/g, '<span class="suspicious-link">$1</span>')}
        </div>
    `;
    
    currentEmailDemo.style.display = 'block';
    document.getElementById('startDemoBtn').style.display = 'none';
    document.getElementById('analyzeBtn').style.display = 'inline-block';
    
    updateDemoProgress(60, `Email ${demoState.currentEmailIndex + 1}/${phishingDemoEmails.length} loaded. Ready for AI analysis.`);
}

function analyzeCurrentEmail() {
    const email = phishingDemoEmails[demoState.currentEmailIndex];
    const aiProcessing = document.getElementById('aiProcessing');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    analyzeBtn.style.display = 'none';
    aiProcessing.style.display = 'block';
    
    // Simulate AI processing steps
    const processingSteps = [
        "Analyzing email headers and metadata...",
        "Scanning for malicious URLs and attachments...",
        "Performing sentiment and linguistic analysis...",
        "Cross-referencing with threat intelligence databases...",
        "Applying machine learning threat classification...",
        "Generating confidence score and recommendations..."
    ];
    
    let stepIndex = 0;
    const processInterval = setInterval(() => {
        document.getElementById('processingStatus').textContent = processingSteps[stepIndex];
        stepIndex++;
        
        if (stepIndex >= processingSteps.length) {
            clearInterval(processInterval);
            showThreatAnalysis(email);
        }
    }, 1200);
}

function showThreatAnalysis(email) {
    document.getElementById('aiProcessing').style.display = 'none';
    
    const threatAnalysis = document.getElementById('threatAnalysisResults');
    const threatContent = document.getElementById('threatAnalysisContent');
    
    let indicatorsHTML = email.indicators.map(indicator => 
        `<li>🚨 ${indicator}</li>`
    ).join('');
    
    threatContent.innerHTML = `
        <div style="margin-bottom: 1rem;">
            <h4>🔍 Detection Results</h4>
            <span class="threat-level threat-${email.threatLevel}">
                ${email.threatLevel.toUpperCase()} THREAT
            </span>
            <p style="margin-top: 0.5rem;">
                <strong>Confidence Score:</strong> ${(email.confidence * 100).toFixed(1)}%
            </p>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <h4>⚠️ Threat Indicators Detected</h4>
            <ul class="indicators-list">
                ${indicatorsHTML}
            </ul>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <h4>🤖 AI Analysis Summary</h4>
            <p>
                Our advanced machine learning algorithms have identified this email as a 
                <strong>${email.threatLevel}</strong> threat with <strong>${(email.confidence * 100).toFixed(1)}%</strong> confidence.
                The email exhibits multiple indicators commonly associated with phishing attacks.
            </p>
        </div>
    `;
    
    threatAnalysis.style.display = 'block';
    
    setTimeout(() => {
        showRecommendations(email);
    }, 2000);
}

function showRecommendations(email) {
    const recommendationsSection = document.getElementById('recommendationsSection');
    const recommendationsList = document.getElementById('recommendationsList');
    
    let recommendationsHTML = email.recommendations.map(rec => 
        `<li>✅ ${rec}</li>`
    ).join('');
    
    recommendationsList.innerHTML = recommendationsHTML;
    recommendationsSection.style.display = 'block';
    
    demoState.emailsAnalyzed++;
    if (email.confidence > 0.7) {
        demoState.threatsDetected++;
    }
    
    updateDemoProgress(70 + (demoState.currentEmailIndex * 10), 
        `Analysis complete. ${demoState.threatsDetected} threats detected from ${demoState.emailsAnalyzed} emails.`);
    
    if (demoState.currentEmailIndex < phishingDemoEmails.length - 1) {
        document.getElementById('nextExampleBtn').style.display = 'inline-block';
    } else {
        document.getElementById('summaryBtn').style.display = 'inline-block';
    }
}

function nextPhishingExample() {
    demoState.currentEmailIndex++;
    
    // Hide current results
    document.getElementById('threatAnalysisResults').style.display = 'none';
    document.getElementById('recommendationsSection').style.display = 'none';
    document.getElementById('nextExampleBtn').style.display = 'none';
    
    loadCurrentEmail();
}

function showDemoSummary() {
    document.getElementById('currentEmailDemo').style.display = 'none';
    document.getElementById('threatAnalysisResults').style.display = 'none';
    document.getElementById('recommendationsSection').style.display = 'none';
    document.getElementById('summaryBtn').style.display = 'none';
    
    const demoSummary = document.getElementById('demoSummary');
    const demoStats = document.getElementById('demoStats');
    
    const elapsedTime = Math.round((Date.now() - demoState.startTime) / 1000);
    const avgAnalysisTime = Math.round(elapsedTime / demoState.emailsAnalyzed);
    const detectionRate = Math.round((demoState.threatsDetected / demoState.emailsAnalyzed) * 100);
    
    demoStats.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;">
            <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #27ae60;">${demoState.emailsAnalyzed}</div>
                <div style="color: #27ae60;">Emails Analyzed</div>
            </div>
            <div style="background: #ffebee; padding: 1rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #e74c3c;">${demoState.threatsDetected}</div>
                <div style="color: #e74c3c;">Threats Detected</div>
            </div>
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #3498db;">${avgAnalysisTime}s</div>
                <div style="color: #3498db;">Avg Analysis Time</div>
            </div>
            <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #f39c12;">${detectionRate}%</div>
                <div style="color: #f39c12;">Detection Rate</div>
            </div>
        </div>
        
        <p style="margin: 1rem 0; font-size: 1.1rem;">
            🎉 <strong>Excellent!</strong> You've successfully completed the Euramax AI Phishing Detection Demo. 
            Our system analyzed ${demoState.emailsAnalyzed} phishing emails in ${elapsedTime} seconds, 
            achieving a ${detectionRate}% threat detection rate.
        </p>
    `;
    
    demoSummary.style.display = 'block';
    updateDemoProgress(100, "Demo completed successfully!");
    
    // Mark phishing demo as completed
    if (!completedSections.includes('phishing-demo')) {
        completedSections.push('phishing-demo');
        updateProgress();
        markSectionCompleted('phishing-demo');
    }
}

function restartPhishingDemo() {
    // Reset demo state
    document.getElementById('demoSummary').style.display = 'none';
    document.getElementById('currentEmailDemo').style.display = 'none';
    document.getElementById('threatAnalysisResults').style.display = 'none';
    document.getElementById('recommendationsSection').style.display = 'none';
    document.getElementById('nextExampleBtn').style.display = 'none';
    document.getElementById('analyzeBtn').style.display = 'none';
    document.getElementById('summaryBtn').style.display = 'none';
    document.getElementById('startDemoBtn').style.display = 'inline-block';
    
    updateDemoProgress(0, "Klik op 'Start Simulatie' om te beginnen");
}

function updateDemoProgress(percentage, statusText) {
    const progressFill = document.getElementById('demoProgressFill');
    const progressText = document.getElementById('demoProgressText');
    
    if (progressFill) {
        progressFill.style.width = `${percentage}%`;
    }
    
    if (progressText) {
        progressText.textContent = statusText;
    }
}

// Save progress periodically
setInterval(saveProgress, 30000); // Every 30 seconds

// Load progress on page load
document.addEventListener('DOMContentLoaded', loadProgress);

console.log('Euramax Cybersecurity Course JavaScript loaded successfully');