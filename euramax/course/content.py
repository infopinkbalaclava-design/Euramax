"""
Course Content Data
Nederlandse cybersecurity cursusinhoud voor werknemers
"""

from euramax.course.models import CourseModule, QuizQuestion, QuestionType, DifficultyLevel, CourseStructure


# Module 1: Phishing Herkenning
phishing_module = CourseModule(
    id="phishing_recognition",
    title="Phishing Aanvallen Herkennen",
    description="Leer hoe je phishing-e-mails en verdachte websites kunt herkennen en vermijden",
    difficulty=DifficultyLevel.BEGINNER,
    estimated_duration=20,
    content=[
        "# Wat is Phishing?",
        "Phishing is een cybercriminele techniek waarbij oplichters zich voordoen als betrouwbare organisaties om gevoelige informatie te stelen zoals wachtwoorden, creditcardnummers of persoonlijke gegevens.",
        
        "## Veelvoorkomende Phishing Technieken",
        "**E-mail Phishing**: De meest voorkomende vorm waarbij nepberichten worden verstuurd die lijken te komen van bekende bedrijven.",
        "**Spear Phishing**: Gerichte aanvallen op specifieke personen of organisaties.",
        "**Whaling**: Aanvallen gericht op hooggeplaatste functionarissen.",
        "**Vishing**: Phishing via telefoongesprekken.",
        "**Smishing**: Phishing via SMS-berichten.",
        
        "## Rode Vlaggen van Phishing E-mails",
        "🚩 **Urgente of dreigende taal**: 'Uw account wordt binnen 24 uur gesloten!'",
        "🚩 **Spelfouten en grammaticale fouten**: Professionele organisaties maken zelden zulke fouten",
        "🚩 **Verdachte afzenders**: Controleer het e-mailadres zorgvuldig",
        "🚩 **Onverwachte bijlagen**: Vooral .exe, .zip of .doc bestanden",
        "🚩 **Links naar onbekende websites**: Beweeg je muis over links zonder te klikken",
        "🚩 **Verzoeken om gevoelige informatie**: Echte bedrijven vragen nooit om wachtwoorden via e-mail",
        
        "## Hoe Te Reageren",
        "✅ **Verifieer de afzender**: Bel het bedrijf via hun officiële nummer",
        "✅ **Gebruik officiële websites**: Type de URL handmatig in plaats van links te klikken",
        "✅ **Rapporteer verdachte e-mails**: Doorsturen naar IT-beveiliging",
        "✅ **Verwijder de e-mail**: Na rapportage veilig verwijderen",
        
        "## Praktische Tips",
        "- Installeer e-mailfilters en houd ze up-to-date",
        "- Gebruik tweefactorauthenticatie waar mogelijk",
        "- Houd je browser en antivirus software actueel",
        "- Wees extra voorzichtig met e-mails die persoonlijke actie vereisen"
    ],
    learning_objectives=[
        "Verschillende soorten phishing aanvallen kunnen identificeren",
        "Rode vlaggen in verdachte e-mails herkennen", 
        "Weten hoe adequaat te reageren op phishing pogingen",
        "Best practices implementeren voor e-mailbeveiliging"
    ]
)

# Module 2: Wachtwoordbeveiliging
password_module = CourseModule(
    id="password_security",
    title="Wachtwoordbeveiliging",
    description="Maak sterke wachtwoorden en beheer ze veilig om je accounts te beschermen",
    difficulty=DifficultyLevel.BEGINNER,
    estimated_duration=15,
    content=[
        "# Waarom Wachtwoordbeveiliging Belangrijk Is",
        "Wachtwoorden zijn de eerste verdedigingslinie van je digitale accounts. Zwakke wachtwoorden maken het gemakkelijk voor cybercriminelen om toegang te krijgen tot gevoelige informatie.",
        
        "## Kenmerken van Sterke Wachtwoorden",
        "✅ **Minimaal 12 karakters lang**: Langere wachtwoorden zijn exponentieel moeilijker te kraken",
        "✅ **Mix van karaktertypes**: Hoofdletters, kleine letters, cijfers en speciale tekens",
        "✅ **Geen voorspelbare patronen**: Vermijd 'Password123' of '12345678'",
        "✅ **Geen persoonlijke informatie**: Geen namen, geboortedata of adressen",
        "✅ **Uniek per account**: Hergebruik nooit hetzelfde wachtwoord",
        
        "## Wachtwoord Aanmaaktechnieken",
        "**Passphrase Methode**: Gebruik een zin zoals 'MijnKat3tGraag#Vis!' (gemakkelijk te onthouden, moeilijk te kraken)",
        "**Eerste Letter Methode**: 'Ik hou van Nederland sinds 1945!' wordt 'IhvNs1945!'",
        "**Willekeurige Generator**: Gebruik wachtwoordmanagers voor volledig willekeurige wachtwoorden",
        
        "## Wachtwoordmanagers",
        "**Voordelen van wachtwoordmanagers:**",
        "- Genereren sterke, unieke wachtwoorden",
        "- Bewaren wachtwoorden veilig versleuteld",
        "- Automatisch invullen voor gemak",
        "- Synchroniseren tussen apparaten",
        "- Waarschuwen voor hergebruik of zwakke wachtwoorden",
        
        "**Aanbevolen wachtwoordmanagers:**",
        "- 1Password",
        "- Bitwarden", 
        "- LastPass",
        "- Ingebouwde browser managers (met voorzichtigheid)",
        
        "## Tweefactorauthenticatie (2FA)",
        "Voeg een extra beveiligingslaag toe naast je wachtwoord:",
        "**SMS-codes**: Eenvoudig maar minder veilig",
        "**Authenticator apps**: Google Authenticator, Microsoft Authenticator",
        "**Hardware tokens**: Fysieke beveiligingssleutels voor maximale beveiliging",
        
        "## Wat Te Doen Bij Inbreuk",
        "1. **Verander onmiddellijk het wachtwoord** van het gecompromitteerde account",
        "2. **Controleer andere accounts** met hetzelfde wachtwoord",
        "3. **Schakel 2FA in** voor extra beveiliging",
        "4. **Monitor je accounts** voor verdachte activiteit",
        "5. **Rapporteer het incident** aan IT-beveiliging"
    ],
    learning_objectives=[
        "Sterke wachtwoorden kunnen maken volgens best practices",
        "Begrijpen waarom unieke wachtwoorden essentieel zijn",
        "Wachtwoordmanagers effectief kunnen gebruiken",
        "Tweefactorauthenticatie kunnen implementeren",
        "Weten hoe te reageren bij wachtwoordinbreuken"
    ]
)

# Module 3: Veilig Omgaan met Gevoelige Data
data_handling_module = CourseModule(
    id="secure_data_handling", 
    title="Veilig Omgaan met Gevoelige Data",
    description="Leer hoe je vertrouwelijke bedrijfsinformatie veilig kunt opslaan, delen en beschermen",
    difficulty=DifficultyLevel.INTERMEDIATE,
    estimated_duration=25,
    content=[
        "# Wat is Gevoelige Data?",
        "Gevoelige data omvat alle informatie die schade kan veroorzaken als het in verkeerde handen valt:",
        "- **Persoonlijke gegevens**: Namen, adressen, BSN-nummers, geboortedatums",
        "- **Financiële informatie**: Bankrekeningen, creditcardgegevens, salarissen",
        "- **Bedrijfsgeheimen**: Strategische plannen, klantendatabases, intellectueel eigendom",
        "- **Technische data**: Systeeminloggegevens, netwerkconfiguraties, beveiligingssleutels",
        
        "## Classificatie van Data",
        "**🔴 Strikt Vertrouwelijk**: Topgeheim, alleen voor geautoriseerde personen",
        "**🟡 Vertrouwelijk**: Interne informatie, niet voor externe distributie",
        "**🟢 Intern**: Voor werknemers, maar niet publiek",
        "**⚪ Publiek**: Vrij te delen zonder risico",
        
        "## Veilige Opslag Praktijken",
        "**Lokale Opslag:**",
        "✅ Gebruik versleutelde harde schijven (BitLocker, FileVault)",
        "✅ Wachtwoordbescherming op bestanden en mappen",
        "✅ Regelmatige backups op veilige locaties",
        "❌ Geen gevoelige data op desktops of in Downloads",
        
        "**Cloud Opslag:**",
        "✅ Gebruik goedgekeurde bedrijfs-cloudservices",
        "✅ Schakel versleuteling in voor cloud bestanden",
        "✅ Beperk toegang met sterke authenticatie",
        "❌ Geen persoonlijke cloud accounts voor bedrijfsdata",
        
        "## Veilig Delen van Data",
        "**E-mail Beveiliging:**",
        "- Gebruik versleutelde e-mail voor gevoelige informatie",
        "- Controleer altijd de ontvangers voor verzending",
        "- Vermijd cc/bcc fouten bij gevoelige lijsten",
        "- Gebruik wachtwoordbescherming voor bijlagen",
        
        "**Veilige Bestandsdeling:**",
        "- Gebruik bedrijfs-goedgekeurde platforms (SharePoint, OneDrive Business)",
        "- Stel vervaldatums in voor gedeelde links",
        "- Beperk download- en wijzigingsrechten",
        "- Monitor wie toegang heeft tot gedeelde bestanden",
        
        "## Data Vernietiging",
        "**Digitale Vernietiging:**",
        "- Gebruik professionele data-wissing tools",
        "- Versleutel data voor vernietiging als extra zekerheid",
        "- Vernietig alle kopieën en backups",
        "- Documenteer vernietigingsprocessen voor compliance",
        
        "**Fysieke Vernietiging:**",
        "- Gebruik gecertificeerde versnipperaars voor documenten",
        "- Fysieke vernietiging van harde schijven en USB-sticks",
        "- Veilige vernietiging van printouts en notities",
        
        "## Incident Respons",
        "**Bij Data Lekken:**",
        "1. **Stop onmiddellijk** verdere verspreiding",
        "2. **Documenteer** wat er gebeurd is",
        "3. **Rapporteer onmiddellijk** aan IT-beveiliging",
        "4. **Informeer betrokken partijen** volgens protocol",
        "5. **Onderzoek** hoe het kon gebeuren",
        "6. **Implementeer** maatregelen om herhaling te voorkomen",
        
        "## Juridische Aspecten",
        "**AVG (GDPR) Compliance:**",
        "- Privacy by design in alle processen",
        "- Minimale dataverzameling (alleen wat nodig is)",
        "- Toestemming voor verwerking van persoonlijke data",
        "- Recht op vergetelheid en gegevenstoegang",
        "- Meldingsplicht bij datalekken binnen 72 uur"
    ],
    learning_objectives=[
        "Verschillende types gevoelige data kunnen classificeren",
        "Veilige opslag- en deelpraktijken implementeren", 
        "Data vernietiging correct uitvoeren",
        "Adequaat reageren op data-incidenten",
        "AVG/GDPR compliance begrijpen en naleven"
    ]
)

# Module 4: Apparaat- en Netwerkbeveiliging  
device_security_module = CourseModule(
    id="device_network_security",
    title="Apparaat- en Netwerkbeveiliging",
    description="Beveilig je werkcomputer, mobiele apparaten en netwerkverbindingen tegen cyberbedreigingen",
    difficulty=DifficultyLevel.INTERMEDIATE,
    estimated_duration=20,
    content=[
        "# Apparaatbeveiliging Fundamenten",
        "Je werkcomputer en mobiele apparaten zijn toegangspoorten tot bedrijfsgegevens. Goede beveiliging voorkomt ongeautoriseerde toegang en malware-infecties.",
        
        "## Computer Beveiligingsmaatregelen",
        "**Besturingssysteem Updates:**",
        "✅ Automatische updates inschakelen voor het OS",
        "✅ Kritieke patches onmiddellijk installeren",
        "✅ Regelmatige herstart na updates",
        "✅ End-of-life software vervangen",
        
        "**Antivirus & Anti-malware:**",
        "✅ Installeer bedrijfs-goedgekeurde beveiligingssoftware",
        "✅ Houd virus definities up-to-date",
        "✅ Voer regelmatige volledige scans uit",
        "✅ Real-time bescherming ingeschakeld houden",
        
        "**Firewall Configuratie:**",
        "✅ Windows/macOS firewall altijd ingeschakeld",
        "✅ Alleen noodzakelijke poorten open",
        "✅ Blokkeer verdachte uitgaande verbindingen",
        "✅ Monitor netwerk verkeer voor afwijkingen",
        
        "## Mobiele Apparaat Beveiliging",
        "**Smartphone & Tablet Beveiliging:**",
        "🔒 Sterke lockscreen (PIN, patroon, biometrie)",
        "🔒 Automatische vergrendeling na inactiviteit",
        "🔒 Apps alleen uit officiële stores installeren",
        "🔒 Regelmatige backup van belangrijke data",
        "🔒 Remote wipe mogelijkheid configureren",
        
        "**BYOD (Bring Your Own Device) Beleid:**",
        "- Gescheiden bedrijfs- en persoonlijke profielen",
        "- MDM (Mobile Device Management) software",
        "- Versleuteling van apparaatopslag",
        "- Verbod op jailbreak/root toegang",
        
        "## Netwerkbeveiliging",
        "**WiFi Beveiliging:**",
        "✅ **Gebruik alleen beveiligde netwerken**: WPA3 of minimaal WPA2",
        "✅ **Vermijd openbare WiFi**: Voor bedrijfsactiviteiten",
        "✅ **VPN gebruik**: Altijd bij externe verbindingen",
        "❌ **Nooit automatisch verbinden**: Met onbekende netwerken",
        
        "**VPN (Virtual Private Network):**",
        "- Versleutelt al je internetverkeer",
        "- Maskeert je IP-adres en locatie",
        "- Veilige toegang tot bedrijfsnetwerk",
        "- Gebruik altijd bij thuiswerken of reizen",
        
        "**Thuisnetwerk Beveiliging:**",
        "🏠 Verander standaard router wachtwoorden",
        "🏠 WPA3 versleuteling op WiFi netwerk",
        "🏠 Gastnetwerk voor bezoekers",
        "🏠 Firmware updates voor router",
        "🏠 Firewall instellingen controleren",
        
        "## USB en Externe Apparaten",
        "**USB Beveiliging:**",
        "⚠️ **Nooit onbekende USB-sticks gebruiken**: Kunnen malware bevatten",
        "⚠️ **Scan externe apparaten**: Voor gebruik met bedrijfssystemen",
        "⚠️ **Versleutel USB-opslag**: Voor gevoelige data transport",
        "⚠️ **Autorun uitschakelen**: Voorkomt automatische malware uitvoering",
        
        "## Fysieke Beveiliging",
        "**Werkplek Beveiliging:**",
        "🔐 Computer vergrendelen bij verlaten werkplek",
        "🔐 Screen privacy filters in publieke ruimtes",
        "🔐 Gevoelige documenten opgeborgen houden",
        "🔐 Bezoekers niet onbewaakt bij computers",
        
        "**Laptop & Apparaat Bescherming:**",
        "- Gebruik laptopsloten in publieke ruimtes",
        "- Laat nooit apparaten onbeheerd achter",
        "- Backup belangrijke data regelmatig",
        "- Asset tags voor bedrijfsapparatuur",
        
        "## Incident Detectie & Respons",
        "**Waarschuwingssignalen:**",
        "🚨 Ongewone traagheid van systeem",
        "🚨 Pop-ups of onbekende software",
        "🚨 Onverwachte netwerk activiteit",
        "🚨 Veranderingen in bestandslocaties",
        "🚨 Ongeautoriseerde inlogpogingen",
        
        "**Reactiestappen:**",
        "1. **Isoleer** het geïnfecteerde apparaat van netwerk",
        "2. **Documenteer** symptomen en tijdlijn",
        "3. **Rapporteer** onmiddellijk aan IT-beveiliging",
        "4. **Scan** het systeem met up-to-date antivirus",
        "5. **Verander** wachtwoorden van accounts die mogelijk gecompromitteerd zijn"
    ],
    learning_objectives=[
        "Computer en mobiele apparaten effectief beveiligen",
        "Netwerkverbindingen veilig configureren en gebruiken",
        "Fysieke beveiliging van apparaten implementeren",
        "Beveiligingsincidenten herkennen en erop reageren",
        "VPN en andere beveiligingstools correct gebruiken"
    ]
)

# Module 5: Rapporteren van Beveiligingsincidenten
incident_reporting_module = CourseModule(
    id="incident_reporting",
    title="Rapporteren van Beveiligingsincidenten", 
    description="Leer hoe je beveiligingsincidenten herkent, documenteert en rapporteert volgens bedrijfsprotocol",
    difficulty=DifficultyLevel.INTERMEDIATE,
    estimated_duration=18,
    content=[
        "# Wat is een Beveiligingsincident?",
        "Een beveiligingsincident is elke gebeurtenis die de vertrouwelijkheid, integriteit of beschikbaarheid van bedrijfsinformatie in gevaar brengt.",
        
        "## Types Beveiligingsincidenten",
        "**🚨 Kritieke Incidenten (Onmiddellijke actie vereist):**",
        "- Actieve malware infectie",
        "- Datalek met persoonlijke gegevens",
        "- Ransomware aanval",
        "- Ongeautoriseerde toegang tot kritieke systemen",
        "- DDoS aanval op bedrijfsservices",
        
        "**⚠️ Ernstige Incidenten (Actie binnen 4 uur):**",
        "- Phishing aanval op werknemers",
        "- Verdachte netwerkactiviteit",
        "- Verlies of diefstal van bedrijfsapparatuur",
        "- Compromitteerde gebruikersaccounts",
        "- Interne beveiligingsschendingen",
        
        "**ℹ️ Standaard Incidenten (Actie binnen 24 uur):**",
        "- Spam of ongewenste e-mails",
        "- Minor software kwetsbaarheden",
        "- Verdachte website activiteit",
        "- Niet-kritieke systeem anomalieën",
        
        "## Herkenning van Incidenten",
        "**Technische Indicatoren:**",
        "- Ongewoon langzame systeem prestaties",
        "- Onverwachte pop-ups of berichten",
        "- Bestanden die verdwijnen of wijzigen",
        "- Onbekende software installaties",
        "- Abnormaal netwerkverkeer",
        
        "**Gedragsindicatoren:**",
        "- Collega's die vragen naar informatie die ze niet zouden moeten weten",
        "- Ongeautoriseerde personen in beveiligde gebieden",
        "- Verdachte telefoongesprekken over bedrijfsinformatie",
        "- USB-sticks of apparaten die 'gevonden' zijn",
        
        "## Onmiddellijke Responsstappen",
        "**1. STOP en DENK (Niet in paniek raken)**",
        "- Beoordeel snel de situatie",
        "- Voorkom verdere schade",
        "- Raak niets aan dat bewijsmateriaal kan zijn",
        
        "**2. ISOLEER (Beperk de schade)**",
        "- Koppel geïnfecteerde apparaten los van netwerk",
        "- Verander wachtwoorden van betrokken accounts",
        "- Blokkeer verdachte gebruikersaccounts",
        "- Bewaar alle relevante informatie",
        
        "**3. DOCUMENTEER (Verzamel informatie)**",
        "- Tijd en datum van ontdekking",
        "- Beschrijving van wat er gebeurd is",
        "- Screenshots van foutmeldingen",
        "- Lijst van betrokken systemen/accounts",
        "- Namen van betrokken personen",
        
        "## Rapportageproces",
        "**Stap 1: Initiële Melding**",
        "📞 **Telefonisch contact**: IT-beveiliging +31-20-SECURITY",
        "📧 **E-mail rapport**: security@euramax.eu",
        "🌐 **Online portal**: https://security.euramax.eu/incident",
        
        "**Stap 2: Gedetailleerd Incident Rapport**",
        "Vul binnen 2 uur een gedetailleerd rapport in met:",
        "- **Incident ID**: Unieke identificatie (wordt automatisch toegewezen)",
        "- **Prioriteit**: Kritiek/Hoog/Medium/Laag",
        "- **Beschrijving**: Wat er precies gebeurd is",
        "- **Impact**: Welke systemen/data zijn betrokken",
        "- **Tijdlijn**: Wanneer begon het incident",
        "- **Eerste respons**: Welke stappen zijn al genomen",
        
        "**Stap 3: Follow-up Communicatie**",
        "- Regelmatige status updates naar IT-beveiliging",
        "- Documentatie van alle verdere bevindingen",
        "- Medewerking aan forensisch onderzoek",
        "- Implementatie van aanbevolen maatregelen",
        
        "## Incident Classificatie Matrix",
        "```",
        "Impact →    Laag      Medium    Hoog      Kritiek",
        "Kans ↓",
        "Laag        Laag      Laag      Medium    Medium",
        "Medium      Laag      Medium    Hoog      Hoog", 
        "Hoog        Medium    Hoog      Hoog      Kritiek",
        "Kritiek     Medium    Hoog      Kritiek   Kritiek",
        "```",
        
        "## Communicatie Protocol",
        "**Interne Communicatie:**",
        "✅ Rapporteer altijd eerst aan IT-beveiliging",
        "✅ Informeer je directe leidinggevende",
        "✅ Gebruik alleen goedgekeurde communicatiekanalen",
        "❌ Deel geen details via sociale media",
        "❌ Speculeer niet over oorzaken in e-mails",
        
        "**Externe Communicatie:**",
        "- Alleen geautoriseerd personeel communiceert extern",
        "- Alle externe communicatie via PR/communicatie afdeling",
        "- Juridische review voor officiële statements",
        "- Coordinatie met regelgevende instanties indien nodig",
        
        "## Post-Incident Activiteiten",
        "**Lessons Learned Sessies:**",
        "- Wat ging goed tijdens de respons?",
        "- Wat kan verbeterd worden?",
        "- Welke aanvullende training is nodig?",
        "- Hoe kunnen we soortgelijke incidenten voorkomen?",
        
        "**Preventieve Maatregelen:**",
        "- Update van beveiligingsbeleid",
        "- Aanvullende technische controles",
        "- Extra training voor werknemers",
        "- Verbeterde monitoring en detectie",
        
        "## Juridische en Compliance Aspecten",
        "**AVG/GDPR Meldingsplicht:**",
        "- Datalekken melden binnen 72 uur aan AP (Autoriteit Persoonsgegevens)",
        "- Betrokkenen informeren bij hoog risico",
        "- Documentatie voor compliance audits",
        "- Samenwerking met externe autoriteiten",
        
        "**Bewijs Behoud:**",
        "- Geen systemen wissen zonder toestemming IT-forensics",
        "- Chain of custody voor bewijsmateriaal",
        "- Logbestanden bewaren voor onderzoek",
        "- Screenshots en documentatie archiveren"
    ],
    learning_objectives=[
        "Verschillende types beveiligingsincidenten kunnen herkennen",
        "Correcte eerste responsstappen kunnen uitvoeren",
        "Incidenten effectief kunnen documenteren en rapporteren",
        "Communicatieprotocollen begrijpen en naleven",
        "Post-incident activiteiten ondersteunen voor preventie"
    ]
)

# Module 6: Social Engineering Bewustzijn
social_engineering_module = CourseModule(
    id="social_engineering_awareness",
    title="Social Engineering Bewustzijn",
    description="Herken en weerstaan manipulatietechnieken die cybercriminelen gebruiken om toegang te krijgen tot gevoelige informatie",
    difficulty=DifficultyLevel.ADVANCED,
    estimated_duration=22,
    content=[
        "# Wat is Social Engineering?",
        "Social engineering is de kunst van het manipuleren van mensen om vertrouwelijke informatie prijs te geven of beveiligingsmaatregelen te omzeilen. Het maakt gebruik van menselijke psychologie in plaats van technische hacking.",
        
        "## Waarom Social Engineering Effectief Is",
        "**Menselijke Factoren:**",
        "- **Vertrouwen**: Mensen willen van nature helpen",
        "- **Autoriteit**: Respect voor gezagsfiguren", 
        "- **Urgentie**: Druk om snel te handelen",
        "- **Nieuwsgierigheid**: Verlangen naar informatie",
        "- **Angst**: Vrees voor negatieve gevolgen",
        "- **Hebzucht**: Verlokking van voordelen",
        
        "## Veelvoorkomende Social Engineering Technieken",
        "**🎭 Pretexting (Voorwendsel)**",
        "De aanvaller creëert een verhaal om vertrouwen te winnen:",
        "- 'Ik ben van IT en moet uw wachtwoord verifiëren'",
        "- 'Ik ben een nieuwe collega en heb toegang nodig'",
        "- 'Dit is de bank, we hebben verdachte activiteit gedetecteerd'",
        
        "**📞 Vishing (Voice Phishing)**",
        "Telefonische social engineering aanvallen:",
        "- Nabootsen van banken of overheidsinstanties",
        "- Urgent technische problemen die wachtwoorden vereisen",
        "- 'Gratis' aanbiedingen in ruil voor persoonlijke gegevens",
        
        "**🎣 Baiting (Lokken)**",
        "Gebruik maken van nieuwsgierigheid of hebzucht:",
        "- USB-sticks gelabeld 'Salarissen 2024' in parkeerplaats",
        "- 'Gratis' software downloads met malware",
        "- Fysieke media met aantrekkelijke labels",
        
        "**🚪 Tailgating/Piggybacking**",
        "Ongeautoriseerde fysieke toegang verkrijgen:",
        "- Volgen van geautoriseerde personen door beveiligde deuren",
        "- Vragen om 'even mee te lopen' omdat badge vergeten is",
        "- Zich voordoen als bezorger of onderhoudspersoneel",
        
        "**⚡ Quid Pro Quo**",
        "Aanbieden van diensten in ruil voor informatie:",
        "- 'Gratis' technische ondersteuning",
        "- Aanbieden van upgrades of voordelen",
        "- 'Onderzoek' waarbij gevoelige vragen gesteld worden",
        
        "## Digitale Social Engineering",
        "**Spear Phishing**",
        "Gerichte e-mails gebaseerd op onderzoek:",
        "- Gebruik van sociale media informatie",
        "- Nabootsen van bekende contacten",
        "- Referenties naar actuele gebeurtenissen",
        
        "**Watering Hole Aanvallen**",
        "Infecteren van websites die doelgroep bezoekt:",
        "- Compromitteren van branchespecifieke sites",
        "- Injecteren van malware in vertrouwde platforms",
        "- Uitbuiting van zero-day kwetsbaarheden",
        
        "**Social Media Mining**",
        "Verzamelen van informatie via sociale platforms:",
        "- Persoonlijke details voor identity theft",
        "- Werkgerelateerde informatie voor spear phishing",
        "- Relaties en connecties voor trust building",
        
        "## Fysieke Social Engineering",
        "**Dumpster Diving**",
        "Zoeken naar waardevolle informatie in afval:",
        "- Niet-versnipperde documenten",
        "- Weggegooid hardware met data",
        "- Organisatieschema's en contactlijsten",
        
        "**Shoulder Surfing**",
        "Observeren van gevoelige informatie:",
        "- Wachtwoorden bij intypen",
        "- Pincode bij geldautomaten",
        "- Vertrouwelijke gesprekken in openbare ruimtes",
        
        "**Impersonation**",
        "Zich voordoen als andere personen:",
        "- Nep ID-badges of uniformen",
        "- Nabootsen van autoriteiten",
        "- Claimen van toegangsprivileges",
        
        "## Verdedigingsstrategieën",
        "**🛡️ Verificatie Protocollen**",
        "✅ **Altijd verifiëren**: Bel terug via officiële nummers",
        "✅ **Gebruik alternatieve kanalen**: Niet hetzelfde medium als eerste contact",
        "✅ **Vraag naar ID**: Badge, legitimatie, autorisatie",
        "✅ **Check autorisaties**: Bevestig toegangsrechten met supervisor",
        
        "**🔒 Informatie Bescherming**",
        "❌ **Deel nooit gevoelige info**: Via onveilige kanalen",
        "❌ **Geen wachtwoorden**: Aan onbekende personen",
        "❌ **Geen interne details**: Aan externe partijen",
        "❌ **Geen toegangscodes**: Zonder proper verificatie",
        
        "**🤔 Kritisch Denken**",
        "- **Pauzeer bij urgentie**: Legitimate verzoeken kunnen wachten",
        "- **Vraag jezelf af**: Waarom heeft deze persoon deze info nodig?",
        "- **Zoek bevestiging**: Bij twijfel, verifieer met collega's",
        "- **Vertrouw je instinct**: Als iets verdacht voelt, is het dat waarschijnlijk",
        
        "## Organisatorische Maatregelen",
        "**Beleid en Procedures**",
        "- Duidelijke protocollen voor informatie delen",
        "- Verificatie procedures voor externe verzoeken",
        "- Incident rapportage procedures",
        "- Regelmatige beveiligingsawareness training",
        
        "**Fysieke Beveiliging**",
        "- Toegangscontrole met badge systemen",
        "- Bezoekersregistratie en escort beleid",
        "- Clean desk policy voor gevoelige documenten",
        "- Beveiligde vernietiging van documenten",
        
        "**Technische Controles**",
        "- Email filtering en anti-phishing systemen",
        "- Multi-factor authenticatie voor kritieke systemen",
        "- Monitoring van abnormale account activiteit",
        "- Regular security awareness testing",
        
        "## Incident Response",
        "**Bij Vermoeden van Social Engineering:**",
        "1. **Stop de interactie** onmiddellijk",
        "2. **Documenteer** alle details van het contact",
        "3. **Rapporteer** aan IT-beveiliging",
        "4. **Verifieer** of gevoelige informatie gecompromitteerd is",
        "5. **Waarschuw** andere potentiële doelwitten",
        "6. **Implementeer** aanvullende beveiligingsmaatregelen",
        
        "**Damage Assessment:**",
        "- Welke informatie is mogelijk gedeeld?",
        "- Welke systemen kunnen gecompromitteerd zijn?",
        "- Wie anders kan benaderd zijn?",
        "- Welke accounts moeten gereset worden?",
        
        "## Preventie Tips",
        "**👤 Persoonlijke Beveiliging:**",
        "- Beperk informatie op sociale media",
        "- Gebruik privacy instellingen consequent",
        "- Wees voorzichtig met persoonlijke details in gesprekken",
        "- Train familie en vrienden in awareness",
        
        "**🏢 Workplace Beveiliging:**",
        "- Challenge onbekende personen beleefd",
        "- Escort bezoekers naar hun bestemming",
        "- Rapporteer verdachte activiteiten onmiddellijk",
        "- Participeer actief in security awareness programma's"
    ],
    learning_objectives=[
        "Verschillende social engineering technieken kunnen herkennen",
        "Psychologische manipulatie tactieken begrijpen",
        "Effectieve verdedigingsstrategieën kunnen implementeren",
        "Fysieke en digitale social engineering kunnen onderscheiden",
        "Adequate respons op social engineering pogingen uitvoeren"
    ]
)

# Quiz vragen voor alle modules
quiz_questions = [
    # Phishing Module Quiz
    QuizQuestion(
        id="phishing_q1",
        module_id="phishing_recognition",
        question_type=QuestionType.MULTIPLE_CHOICE,
        question_text="Wat is de meest betrouwbare manier om een verdachte e-mail te verifiëren?",
        options=[
            "De link in de e-mail klikken en kijken waar het naar toe gaat",
            "Antwoorden op de e-mail om te vragen of het echt is", 
            "Het bedrijf bellen via hun officiële telefoonnummer",
            "Kijken of de e-mail correct gespeld is"
        ],
        correct_answer=2,
        explanation="Bellen via het officiële nummer is de veiligste verificatiemethode. Klikken op links of antwoorden kan je blootstellen aan malware of bevestigt dat je e-mailadres actief is.",
        difficulty=DifficultyLevel.BEGINNER,
        points=2
    ),
    QuizQuestion(
        id="phishing_q2", 
        module_id="phishing_recognition",
        question_type=QuestionType.TRUE_FALSE,
        question_text="Phishing e-mails bevatten altijd spelfouten en grammaticale fouten.",
        options=["Waar", "Onwaar"],
        correct_answer=1,
        explanation="Onwaar. Moderne phishing aanvallen kunnen zeer professioneel zijn zonder spelfouten. Cybercriminelen worden steeds beter in het nabootsen van legitieme communicatie.",
        difficulty=DifficultyLevel.BEGINNER,
        points=1
    ),
    QuizQuestion(
        id="phishing_q3",
        module_id="phishing_recognition", 
        question_type=QuestionType.SCENARIO,
        question_text="Je ontvangt een e-mail van 'je bank' die zegt dat je account gehackt is en je onmiddellijk moet inloggen via de bijgevoegde link. Wat doe je?",
        options=[
            "Klik onmiddellijk op de link om je account te controleren",
            "Verwijder de e-mail zonder actie",
            "Bel je bank via het officiële nummer en verifieer de e-mail",
            "Stuur de e-mail door naar vrienden om hen te waarschuwen"
        ],
        correct_answer=2,
        explanation="Bellen naar de bank via hun officiële nummer is de juiste actie. Zo kun je verifiëren of de e-mail echt is en krijg je hulp als er daadwerkelijk een probleem is.",
        difficulty=DifficultyLevel.INTERMEDIATE,
        points=3
    ),
    
    # Password Module Quiz  
    QuizQuestion(
        id="password_q1",
        module_id="password_security",
        question_type=QuestionType.MULTIPLE_CHOICE,
        question_text="Wat is de minimaal aanbevolen lengte voor een sterk wachtwoord?",
        options=[
            "8 karakters",
            "10 karakters", 
            "12 karakters",
            "16 karakters"
        ],
        correct_answer=2,
        explanation="12 karakters is de huidige minimaal aanbevolen lengte. Langere wachtwoorden zijn exponentieel moeilijker te kraken, zelfs met krachtige computers.",
        difficulty=DifficultyLevel.BEGINNER,
        points=1
    ),
    QuizQuestion(
        id="password_q2",
        module_id="password_security",
        question_type=QuestionType.TRUE_FALSE,
        question_text="Het is veilig om hetzelfde sterke wachtwoord te gebruiken voor meerdere belangrijke accounts.",
        options=["Waar", "Onwaar"],
        correct_answer=1,
        explanation="Onwaar. Hergebruik van wachtwoorden betekent dat als één account gehackt wordt, alle andere accounts ook gecompromitteerd zijn. Elk account moet een uniek wachtwoord hebben.",
        difficulty=DifficultyLevel.BEGINNER,
        points=2
    ),
    
    # Data Handling Module Quiz
    QuizQuestion(
        id="data_q1",
        module_id="secure_data_handling",
        question_type=QuestionType.MULTIPLE_CHOICE,
        question_text="Hoe lang heb je volgens de AVG/GDPR om een datalek te melden aan de Autoriteit Persoonsgegevens?",
        options=[
            "24 uur",
            "48 uur",
            "72 uur", 
            "1 week"
        ],
        correct_answer=2,
        explanation="Onder de AVG/GDPR moet een datalek binnen 72 uur gemeld worden aan de toezichthouder (in Nederland de Autoriteit Persoonsgegevens).",
        difficulty=DifficultyLevel.INTERMEDIATE,
        points=2
    ),
    
    # Device Security Module Quiz
    QuizQuestion(
        id="device_q1",
        module_id="device_network_security", 
        question_type=QuestionType.SCENARIO,
        question_text="Je werkt in een café met gratis WiFi. Welke actie is het meest veilig voor bedrijfsactiviteiten?",
        options=[
            "Direct verbinden met het gratis WiFi",
            "Alleen websites bezoeken met HTTPS",
            "Een VPN gebruiken voor alle internetverkeer",
            "Hotspot maken met je telefoon"
        ],
        correct_answer=2,
        explanation="Een VPN versleutelt al je verkeer en beschermt tegen afluisteren op openbare netwerken. Dit is de veiligste optie voor bedrijfsactiviteiten.",
        difficulty=DifficultyLevel.INTERMEDIATE,
        points=3
    ),
    
    # Incident Reporting Module Quiz
    QuizQuestion(
        id="incident_q1",
        module_id="incident_reporting",
        question_type=QuestionType.MULTIPLE_CHOICE,
        question_text="Wat is de eerste stap bij het ontdekken van een mogelijk beveiligingsincident?",
        options=[
            "Proberen het probleem zelf op te lossen",
            "Stop en beoordeel de situatie zonder verder te handelen",
            "Onmiddellijk alle collega's waarschuwen via e-mail",
            "Het systeem opnieuw opstarten"
        ],
        correct_answer=1,
        explanation="Stop en denk na om verdere schade te voorkomen. Ondoordachte acties kunnen bewijs vernietigen of de situatie verergeren.",
        difficulty=DifficultyLevel.INTERMEDIATE,
        points=2
    ),
    
    # Social Engineering Module Quiz
    QuizQuestion(
        id="social_q1",
        module_id="social_engineering_awareness",
        question_type=QuestionType.SCENARIO,
        question_text="Iemand belt zich voorstellend als IT-support en zegt je wachtwoord nodig te hebben voor 'systeem onderhoud'. Wat doe je?",
        options=[
            "Je wachtwoord geven omdat IT dit regelmatig doet",
            "Vragen naar hun werknemers-ID nummer",
            "Weigeren en contact opnemen met IT via officiële kanalen",
            "Het gesprek beëindigen zonder uitleg"
        ],
        correct_answer=2,
        explanation="Legitieme IT-afdelingen vragen nooit om wachtwoorden. Weiger vriendelijk en verifieer via officiële kanalen. Dit is een klassieke social engineering techniek.",
        difficulty=DifficultyLevel.ADVANCED,
        points=3
    )
]

# Voeg quiz vragen toe aan de juiste modules
for question in quiz_questions:
    for module in [phishing_module, password_module, data_handling_module, 
                   device_security_module, incident_reporting_module, social_engineering_module]:
        if question.module_id == module.id:
            module.quiz_questions.append(question)

# Complete cursusstructuur
cybersecurity_course = CourseStructure(
    course_title="Nederlandse Cybersecurity Cursus voor Werknemers",
    course_description="Een uitgebreide interactieve cursus over cybersecurity best practices voor werknemers die met gevoelige bedrijfsdata werken. De cursus behandelt alle essentiële onderwerpen van phishing herkenning tot incident rapportage.",
    modules=[
        phishing_module,
        password_module, 
        data_handling_module,
        device_security_module,
        incident_reporting_module,
        social_engineering_module
    ],
    total_duration=120,  # Totaal 2 uur
    completion_certificate=True
)