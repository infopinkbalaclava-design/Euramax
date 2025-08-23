"""
AI-powered threat detection system
Specializes in phishing detection with machine learning
"""

import asyncio
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

@dataclass
class ThreatInfo:
    threat_id: str
    threat_type: str
    severity: str
    source: str
    content: str
    indicators: List[str]
    confidence: float
    detected_at: datetime
    
    def dict(self):
        return {
            'threat_id': self.threat_id,
            'threat_type': self.threat_type,
            'severity': self.severity,
            'source': self.source,
            'content': self.content,
            'indicators': self.indicators,
            'confidence': self.confidence,
            'detected_at': self.detected_at.isoformat()
        }

class ThreatDetector:
    def __init__(self):
        self.phishing_model = self._load_or_create_phishing_model()
        self.suspicious_patterns = self._load_suspicious_patterns()
        
    def _load_or_create_phishing_model(self):
        """Load or create a basic phishing detection model"""
        model_path = 'models/phishing_detector.joblib'
        
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            # Create a basic model with training data
            return self._create_basic_phishing_model()
    
    def _create_basic_phishing_model(self):
        """Create a basic phishing detection model with sample training data"""
        # Sample training data (in production, this would be much larger)
        phishing_samples = [
            "Urgent: Your account will be suspended. Click here to verify",
            "Congratulations! You've won $1000. Claim your prize now",
            "Your bank account has been compromised. Login immediately",
            "Update your payment information to avoid service interruption",
            "Security alert: Unusual activity detected on your account",
            "Your package delivery failed. Update shipping information",
            "Tax refund available. Download form to claim $500",
            "Your email will be deleted. Verify account now"
        ]
        
        legitimate_samples = [
            "Meeting scheduled for tomorrow at 2 PM in conference room",
            "Please review the attached document and provide feedback",
            "Monthly report is due by end of week",
            "Welcome to our newsletter. Unsubscribe anytime",
            "Your order has been shipped and will arrive tomorrow",
            "Thank you for your purchase. Receipt attached",
            "System maintenance scheduled for this weekend",
            "New policy updates effective next month"
        ]
        
        # Prepare training data
        texts = phishing_samples + legitimate_samples
        labels = [1] * len(phishing_samples) + [0] * len(legitimate_samples)
        
        # Create and train model
        model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        
        model.fit(texts, labels)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/phishing_detector.joblib')
        
        return model
    
    def _load_suspicious_patterns(self) -> Dict[str, List[str]]:
        """Load patterns that indicate various types of cyber threats"""
        return {
            'phishing': [
                r'urgent.*action.*required',
                r'click.*here.*immediately',
                r'verify.*account.*now',
                r'suspended.*account',
                r'security.*alert',
                r'update.*payment',
                r'claim.*prize',
                r'tax.*refund',
                r'login.*verify'
            ],
            'malware': [
                r'download.*now',
                r'install.*update',
                r'virus.*detected',
                r'clean.*computer',
                r'speed.*up.*pc'
            ],
            'social_engineering': [
                r'confidential.*information',
                r'share.*password',
                r'call.*immediately',
                r'urgent.*help.*needed'
            ]
        }
    
    async def scan_for_threats(self) -> List[ThreatInfo]:
        """Main threat scanning function"""
        threats = []
        
        # Simulate email scanning (in production, this would connect to email servers)
        sample_emails = await self._get_sample_emails()
        
        for email in sample_emails:
            threat = await self.analyze_content(email['content'], email['source'])
            if threat:
                threats.append(threat)
        
        return threats
    
    async def _get_sample_emails(self) -> List[Dict]:
        """Simulate getting emails to analyze (mock function)"""
        # In production, this would connect to email servers, web traffic, etc.
        return [
            {
                'content': 'URGENT: Your bank account has been compromised. Click here to secure it immediately.',
                'source': 'email:suspicious@fake-bank.com'
            },
            {
                'content': 'Congratulations! You have won €10,000 in our lottery. Click to claim your prize now!',
                'source': 'email:winner@fake-lottery.org'
            }
        ]
    
    async def analyze_content(self, content: str, source: str) -> Optional[ThreatInfo]:
        """Analyze content for threats using AI and pattern matching"""
        
        # Check for phishing using ML model
        phishing_prob = self.phishing_model.predict_proba([content])[0][1]
        
        # Pattern-based detection
        detected_patterns = []
        threat_type = None
        
        for threat_category, patterns in self.suspicious_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected_patterns.append(pattern)
                    threat_type = threat_category
        
        # Determine if this is a threat
        if phishing_prob > 0.7 or detected_patterns:
            severity = self._calculate_severity(phishing_prob, detected_patterns)
            
            return ThreatInfo(
                threat_id=f"threat_{datetime.now().timestamp()}",
                threat_type=threat_type or "phishing",
                severity=severity,
                source=source,
                content=content,
                indicators=detected_patterns,
                confidence=max(phishing_prob, 0.8 if detected_patterns else 0.0),
                detected_at=datetime.now()
            )
        
        return None
    
    def _calculate_severity(self, ml_confidence: float, patterns: List[str]) -> str:
        """Calculate threat severity based on confidence and patterns"""
        if ml_confidence > 0.9 or len(patterns) > 2:
            return "critical"
        elif ml_confidence > 0.8 or len(patterns) > 1:
            return "high"
        elif ml_confidence > 0.7 or patterns:
            return "medium"
        else:
            return "low"
    
    async def get_threat_statistics(self) -> Dict:
        """Get statistics about detected threats"""
        # In production, this would query the database
        return {
            "total_threats_today": 15,
            "phishing_attempts": 12,
            "malware_detected": 2,
            "blocked_automatically": 14,
            "manual_review_needed": 1
        }