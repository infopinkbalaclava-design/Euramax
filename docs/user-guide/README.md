# Euramax Gebruikershandleiding

## Inhoudsopgave

1. [Inleiding](#inleiding)
2. [Dashboard Overzicht](#dashboard-overzicht)
3. [Bedreigingsdetectie](#bedreigingsdetectie)
4. [Notificaties](#notificaties)
5. [AI-Bot Functies](#ai-bot-functies)
6. [Taalinstellingen](#taalinstellingen)
7. [Veelgestelde Vragen](#veelgestelde-vragen)

## Inleiding

Welkom bij Euramax, uw AI-gestuurde cybersecurity verdedigingssysteem. Dit systeem beschermt uw organisatie tegen phishing-aanvallen en andere cyberbedreigingen door middel van geavanceerde machine learning en automatische respons.

### Belangrijkste Functies

- **Real-time Bedreigingsdetectie**: Automatische scanning van emails en web traffic
- **AI-gestuurde Respons**: Onmiddellijke automatische acties bij gedetecteerde bedreigingen
- **Nederlandse Lokalisatie**: Volledige interface en instructies in het Nederlands
- **Live Dashboard**: Real-time overzicht van beveiligingsstatus

## Dashboard Overzicht

Het hoofddashboard geeft u een compleet overzicht van uw beveiligingsstatus.

### Secties

#### 🔒 Beveiligingsscore
- Toont de algehele beveiligingsstatus (0-100%)
- Gebaseerd op gedetecteerde bedreigingen en systeemprestaties
- Groen (90-100%): Uitstekend
- Geel (70-89%): Goed
- Rood (<70%): Aandacht vereist

#### 🚨 Bedreigingen Vandaag
- Aantal gedetecteerde bedreigingen in de afgelopen 24 uur
- Specifiek aantal phishing-pogingen
- Automatisch geblokkeerde bedreigingen

#### 🤖 AI-Bot Status
- Aantal automatische acties uitgevoerd
- Geblokkeerde domeinen
- Geïsoleerde emails
- Gemiddelde reactietijd

#### 📱 Notificaties
- Aantal ongelezen meldingen
- Recente beveiligingswaarschuwingen

### Dashboard Vernieuwen

Het dashboard wordt automatisch elke 30 seconden bijgewerkt. U kunt ook handmatig vernieuwen door de pagina te herladen.

## Bedreigingsdetectie

### Automatische Scanning

Het systeem scant automatisch:
- **Binnenkomende emails**: Controle op phishing-indicatoren
- **Web traffic**: Detectie van malicious websites
- **Downloads**: Scanning op malware
- **Links**: Verificatie van URL-veiligheid

### Handmatige Scanning

#### Content Scannen
1. Ga naar de "Bedreigingen" pagina
2. Plak verdachte tekst in het scan-veld
3. Klik "Scannen"
4. Bekijk de resultaten

**Voorbeeld Phishing Content:**
```
URGENT: Your bank account has been compromised. 
Click here to secure it immediately.
```

### Bedreigingstypen

#### 🎣 Phishing
- **Kenmerken**: Urgente taal, nep-websites, credential theft
- **Actie**: Automatische blokkering en quarantaine
- **Gebruikersacties**: Niet klikken, melden aan IT

#### 🦠 Malware
- **Kenmerken**: Verdachte downloads, executable files
- **Actie**: Bestanden blokkeren, systeem isoleren
- **Gebruikersacties**: Niet downloaden, systeem scannen

#### 🎭 Social Engineering
- **Kenmerken**: Manipulatieve berichten, informatieverzoeken
- **Actie**: Waarschuwingen genereren
- **Gebruikersacties**: Verificeren via alternatief kanaal

### Ernst Niveaus

- **🔴 Kritiek**: Onmiddellijke actie vereist
- **🟠 Hoog**: Spoedige actie aanbevolen
- **🟡 Gemiddeld**: Monitoring vereist
- **🟢 Laag**: Informatief

## Notificaties

### Typen Notificaties

#### 🚨 Phishing Waarschuwing
Onmiddellijke melding bij gedetecteerde phishing-poging:

**Inhoud:**
- Bedreigingsdetails
- Automatische acties uitgevoerd
- Stap-voor-stap instructies
- Herkenningskenmerken

**Voorbeeld:**
```
🚨 PHISHING AANVAL GEDETECTEERD

ONMIDDELLIJKE ACTIES:
1. KLIK NIET op verdachte links
2. Geef GEEN persoonlijke informatie prijs
3. Verwijder het bericht NIET
4. Meld aan IT-beveiliging

STATUS: Automatisch geblokkeerd door AI-systeem
```

#### 🛡️ Bedreiging Geblokkeerd
Bevestiging dat een bedreiging succesvol is gestopt.

#### 📋 Beveiligingsupdate
Informatie over nieuwe beveiligingsmaatregelen.

### Notificaties Beheren

#### Markeren als Gelezen
- Klik op "Markeren als gelezen" bij elke notificatie
- Ongelezen notificaties hebben blauwe rand

#### Filteren
- **Alle**: Toon alle notificaties
- **Ongelezen**: Toon alleen nieuwe meldingen

### Real-time Updates

Notificaties worden real-time getoond via WebSocket verbinding. Geen vernieuwing nodig.

## AI-Bot Functies

### Automatische Acties

De AI-bot voert automatisch de volgende acties uit:

#### Bij Phishing-detectie:
1. **Bronblokkering**: Email-adres of domein blokkeren
2. **Quarantaine**: Verdachte emails isoleren
3. **Gebruikerswaarschuwing**: Onmiddellijke notificatie
4. **IT-melding**: Security team informeren

#### Bij Malware:
1. **Bestand blokkeren**: Download stoppen
2. **URL blacklisten**: Malicious websites blokkeren
3. **Systeem isoleren**: Geïnfecteerde systemen afschermen

### Reactietijden

- **Detectie**: < 1 seconde
- **Automatische respons**: < 2 seconden
- **Notificatie**: < 3 seconden

### Blocked Domains

Overzicht van geblokkeerde websites:
- **Automatisch**: Door AI-systeem geblokkeerd
- **Handmatig**: Door security team toegevoegd
- **Tijdelijk**: Met vervaldatum

### Quarantaine

Geïsoleerde emails:
- **Phishing**: Verdachte phishing-emails
- **Malware**: Emails met malicious attachments
- **Spam**: Bulk unwanted emails

#### Quarantaine Beheer
- **Vrijgeven**: Als email legitiem blijkt
- **Permanent verwijderen**: Bij bevestigde dreiging
- **Analyseren**: Voor threat intelligence

## Taalinstellingen

### Ondersteunde Talen

- **🇳🇱 Nederlands**: Standaard taal
- **🇬🇧 Engels**: Internationale ondersteuning

### Taal Wijzigen

1. Klik op de taalknop in de header (NL/EN)
2. Selecteer gewenste taal
3. Interface wordt onmiddellijk bijgewerkt

### Automatische Detectie

Het systeem detecteert automatisch:
- Browser taalvoorkeur
- Systeemlocatie
- Gebruikersprofiel (indien ingelogd)

## Veelgestelde Vragen

### ❓ Wat moet ik doen bij een phishing-waarschuwing?

**Antwoord:**
1. **Stop** alle activiteit met het verdachte bericht
2. **Klik niet** op links of bijlagen
3. **Geef geen** informatie prijs
4. **Meld** aan IT-security
5. **Bewaar** het bericht voor onderzoek

### ❓ Hoe weet ik of een email echt phishing is?

**Herkenningskenmerken:**
- Urgente taal ("ONMIDDELLIJK", "BINNEN 24 UUR")
- Spelling-/grammaticafouten
- Verdachte afzender
- Verzoek om persoonlijke gegevens
- Onbekende links

### ❓ Wat gebeurt er met geblokkeerde emails?

**Proces:**
1. **Quarantaine**: Email wordt geïsoleerd
2. **Analyse**: Automatische threat analysis
3. **Rapportage**: Incident wordt gelogd
4. **Actie**: Verdere maatregelen indien nodig

### ❓ Kan ik de AI-beslissingen overschrijven?

**Handmatige Override:**
- Alleen door geautoriseerd security personeel
- Met proper justificatie
- Volledig gelogd voor audit
- Tweede verificatie vereist

### ❓ Hoe accuraat is het detectiesysteem?

**Prestaties:**
- **Nauwkeurigheid**: 98.5%
- **False Positives**: <2%
- **Reactietijd**: <1.2 seconden
- **Uptime**: 99.98%

### ❓ Wat gebeurt er met mijn privacy?

**Privacy Bescherming:**
- **GDPR Compliant**: Nederlandse wetgeving
- **End-to-end Encryption**: Alle communicatie
- **Minimale Data**: Alleen security-relevante info
- **Audit Logging**: Transparante operations

### ❓ Hoe vaak wordt het systeem bijgewerkt?

**Update Schema:**
- **AI Models**: Dagelijks
- **Threat Intelligence**: Real-time
- **Software**: Wekelijks
- **Security Patches**: Onmiddellijk

## Ondersteuning

### Contact

- **Email**: support@euramax.nl
- **Telefoon**: +31 (0)20 123 4567
- **Noodlijn**: +31 (0)800 SECURITY

### Documentatie

- **Technische Docs**: `/docs/technical/`
- **API Reference**: `/docs/api/`
- **Best Practices**: `/docs/security/`

### Training

Beschikbare trainingen:
- **Phishing Herkenning**: 2 uur basis training
- **Incident Response**: 4 uur gevorderde training
- **System Administration**: 8 uur technische training

---

**Euramax** - Uw partner in cybersecurity 🛡️