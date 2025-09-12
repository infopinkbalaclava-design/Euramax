# Euramax Intern Beveiligingssysteem

AI-aangedreven phishing beveiligingssysteem - Intern ontwikkelde geautomatiseerde bedreigingsdetectie en medewerkerstraining platform voor Euramax

## 🛡️ Over dit project

Dit is een intern ontwikkeld beveiligingssysteem door en voor Euramax. Het platform biedt AI-aangedreven phishing detectie en uitgebreide training voor onze eigen medewerkers om cybersecurity bedreigingen te herkennen en te voorkomen.

## ✨ Hoofdfunctionaliteiten

### 🔍 AI-Aangedreven Beveiliging
- **Real-time Phishing Detectie**: Intern ontwikkelde machine learning algoritmen voor 24/7 bedreigingsmonitoring
- **Email Scanning**: Automatische analyse van inkomende emails voor phishing indicators
- **Malware Detection**: Geavanceerde malware detectie en quarantine systemen
- **Threat Intelligence**: Real-time updates van nieuwe bedreigingspatronen

### 📊 Geavanceerd Dashboard
- **Live Monitoring**: Real-time overzicht van beveiligingsstatus en bedreigingen
- **Interactive Analytics**: Visuele rapportages en trends analysis
- **System Health**: Component status monitoring en performance metrics
- **Quick Actions**: Directe toegang tot kritieke functies en escalatie procedures

### 👥 Team Management
- **Intern Team Directory**: Overzicht van alle security team leden met real-time status
- **Role-based Access**: Verschillende toegangsniveaus (Admin, Manager, User)
- **Contact Integration**: Directe integratie met email en Microsoft Teams
- **Emergency Contacts**: 24/7 escalatie procedures voor kritieke incidents

### 📚 Uitgebreide Documentatie
- **API Documentation**: Volledige REST API documentatie met voorbeelden
- **Developer Guide**: Setup, coding standards en development workflows
- **User Manuals**: Stap-voor-stap handleidingen voor alle functionaliteiten
- **Troubleshooting**: Uitgebreide probleemoplossing en FAQ sectie

### 🎫 Support Systeem
- **Ticket Management**: Volledig geïntegreerd support ticket systeem
- **Knowledge Base**: Doorzoekbare kennisbank met veelgestelde vragen
- **Auto-save**: Automatisch opslaan van concepttickets
- **Priority Escalation**: Automatische escalatie voor kritieke security incidents

### 🎓 Medewerkerstraining
- **Interactieve Modules**: Aangepaste trainingsprogramma's per afdeling
- **Progress Tracking**: Real-time voortgang monitoring per medewerker en afdeling
- **Phishing Simulations**: Praktische oefeningen met echte scenario's
- **Certificates**: Digitale certificaten bij voltooiing van trainingen

## 🚀 Snelle Start

### Systeemvereisten
- **Operating System**: Windows 10/11 of macOS 10.14+
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Netwerk**: Actieve VPN-verbinding met Euramax netwerk
- **Authenticatie**: Geldige Euramax Active Directory account

### Toegang Verkrijgen
1. **VPN Verbinding**: Verbind met het Euramax VPN netwerk
2. **Website Toegang**: Navigeer naar `https://security.internal.euramax.nl`
3. **Authenticatie**: Log in met je Active Directory credentials
4. **Onboarding**: Voltooi de initiële beveiligingstraining (verplicht)
5. **Dashboard**: Configureer je persoonlijke dashboard en notificatie-instellingen

### Voor Ontwikkelaars

```bash
# Clone het repository (intern GitLab)
git clone https://gitlab.internal.euramax.nl/security/phishing-protection.git

# Installeer dependencies
cd phishing-protection
npm install

# Configureer environment variabelen
cp .env.example .env.development
nano .env.development

# Start development server
npm run dev

# Run tests
npm test

# Build voor productie
npm run build
```

## 📁 Project Structuur

```
euramax-security-system/
├── static/                     # Frontend bestanden
│   ├── index.html             # Homepage - systeem overzicht
│   ├── dashboard.html         # Real-time beveiligingsdashboard
│   ├── docs.html              # Uitgebreide documentatie
│   ├── team.html              # Intern team directory
│   ├── support.html           # Support ticket systeem
│   ├── about.html             # Over het interne project
│   ├── services.html          # Interne functionaliteiten
│   ├── education.html         # Medewerkerstraining
│   ├── contact.html           # Interne IT support
│   ├── login.html             # Authenticatie pagina
│   ├── css/                   # Stylesheets
│   │   ├── main.css          # Basis styling
│   │   ├── dashboard.css     # Dashboard specifieke styles
│   │   ├── docs.css          # Documentatie styling
│   │   ├── team.css          # Team directory styling
│   │   └── support.css       # Support systeem styling
│   └── js/                    # JavaScript modules
│       ├── main.js           # Basis functionaliteit
│       ├── dashboard.js      # Dashboard interactiviteit
│       ├── docs.js           # Documentatie features
│       ├── team.js           # Team directory functionaliteit
│       └── support.js        # Support systeem workflows
├── README.md                  # Dit bestand
├── CHANGELOG.md              # Versie geschiedenis
└── .gitignore                # Git ignore regels
```

## 🔧 Technische Specificaties

### Frontend Technologieën
- **HTML5**: Semantische markup en accessibility features
- **CSS3**: Modern layout met Grid en Flexbox, responsive design
- **JavaScript ES6+**: Modulaire architectuur met async/await patterns
- **Font**: Inter font family voor optimale leesbaarheid

### Integraties
- **Active Directory**: Single Sign-On (SSO) voor alle medewerkers
- **Microsoft 365**: Email scanning en SharePoint integratie
- **VPN**: Verplichte VPN toegang voor alle functionaliteiten
- **ServiceNow**: Automatische ticket creation voor kritieke incidents

### Performance Features
- **Real-time Updates**: WebSocket verbindingen voor live data
- **Caching**: Local storage voor user preferences en form data
- **Responsive Design**: Optimized voor desktop, tablet en mobile
- **Progressive Enhancement**: Graceful degradation voor oudere browsers

## 🔒 Beveiliging & Compliance

### Toegangscontrole
- **Multi-factor Authentication**: Verplichte MFA voor alle accounts
- **Role-based Permissions**: Granular toegangsrechten per functie
- **Session Management**: Automatische uitlog na inactiviteit
- **IP Whitelisting**: Alleen toegang vanaf Euramax netwerk

### Data Protection
- **Encryption**: All data encrypted in transit en at rest
- **Audit Logging**: Uitgebreide logging van alle gebruikersacties
- **Data Retention**: 2 jaar bewaarperiode conform company policy
- **GDPR Compliance**: Privacy-by-design en data minimization

### Monitoring & Incident Response
- **24/7 Monitoring**: Continues bewaking van alle systemen
- **Automated Alerts**: Real-time notificaties voor security events
- **Incident Escalation**: Automatische escalatie procedures
- **Forensic Capabilities**: Detailed logging voor security investigations

## 📞 Intern Support

### Emergency Contacts
- **🚨 Kritieke Security Incidents**: +31 6 1234 5678 (24/7)
- **🛠️ IT Support Helpdesk**: +31 20 123 4567 (Ma-Vr 08:00-18:00)
- **📧 Email Support**: security@euramax.nl

### Support Kanalen
- **Support Tickets**: Via ingebouwde ticket systeem
- **Knowledge Base**: Doorzoekbare FAQ en troubleshooting
- **Microsoft Teams**: Direct contact met IT Security team
- **Documentatie**: Uitgebreide handleidingen en API docs

### Service Level Agreements
- **Kritieke Issues**: < 30 minuten response tijd
- **High Priority**: < 2 uur response tijd  
- **Medium Priority**: < 4 uur response tijd
- **Low Priority**: < 24 uur response tijd

## 🏗️ Development Team

### Core Team
- **Mark Rijksen** - Lead Intern Ontwikkelaar (TypeScript, Python, AI/ML)
- **Sophie Bakker** - Frontend Ontwikkelaar (React, CSS, UI/UX)
- **Jan van der Berg** - Backend Ontwikkelaar (Node.js, SQL Server, API Design)
- **Emma Kuiper** - Intern Cybersecurity Specialist (Threat Analysis, SIEM)
- **Robert Jansen** - IT Security Manager (Security Strategy, Team Leadership)

### Development Workflow
- **Git Flow**: Feature branches met peer review requirements
- **Testing**: Minimum 80% code coverage met Jest
- **Code Quality**: ESLint + Prettier volgens Euramax standards
- **CI/CD**: Automated testing en deployment via GitLab pipelines

## 📈 Versioning & Updates

### Huidige Versie: 2.1.4
- **Release Date**: 15 maart 2024
- **Major Features**: Dashboard, Documentatie, Team Directory, Support Systeem
- **Next Release**: Q2 2024 - Advanced AI features en mobile app

### Update Procedures
- **Maintenance Windows**: Elke 2e zondag van de maand (02:00-04:00)
- **Emergency Updates**: 24/7 deployment capability voor kritieke fixes
- **Rollback Procedures**: Automated rollback binnen 15 minuten
- **Communication**: Alle updates gecommuniceerd via interne kanalen

## 📋 Changelog

Zie [CHANGELOG.md](CHANGELOG.md) voor een volledige versiegeschiedenis.

## 📄 Licentie & Gebruik

**Intern Gebruik - Vertrouwelijk**

Dit systeem is exclusief ontwikkeld voor intern gebruik bij Euramax en is niet bedoeld voor externe distributie of commercieel gebruik. Alle rechten voorbehouden aan Euramax organisatie.

### Gebruik Voorwaarden
- Alleen toegankelijk voor Euramax medewerkers
- Verplichte acceptatie van interne security policies
- Monitoring van alle gebruikersactiviteiten
- Verbod op ongeautoriseerde data export

---

**© 2024 Euramax Intern Beveiligingssysteem. Alle rechten voorbehouden.**

Voor vragen of support, neem contact op met het IT Security team via security@euramax.nl of het interne support systeem.
