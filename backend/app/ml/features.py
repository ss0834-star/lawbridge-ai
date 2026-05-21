"""LawBridge AI v2 — ML & Rule-based risk engine.
Uses trained scikit-learn models when available,
falls back to rule-based when models not found.
"""
import re
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# Load trained models if available
_clause_model = None
_clause_le = None
_doc_model = None
_doc_le = None

def _load_models():
    global _clause_model, _clause_le, _doc_model, _doc_le
    base = os.path.join(os.path.dirname(__file__), 'models')
    try:
        import joblib
        _clause_model = joblib.load(os.path.join(base, 'clause_risk_v1.pkl'))
        _clause_le = joblib.load(os.path.join(base, 'label_encoder_v1.pkl'))
        logger.info("✅ Trained clause risk model loaded")
    except Exception as e:
        logger.info(f"ℹ️ Clause model not found, using rule-based: {e}")
    try:
        import joblib
        _doc_model = joblib.load(os.path.join(base, 'doc_classifier_v1.pkl'))
        _doc_le = joblib.load(os.path.join(base, 'doc_label_encoder_v1.pkl'))
        logger.info("✅ Trained document classifier loaded")
    except Exception as e:
        logger.info(f"ℹ️ Doc model not found, using keyword scoring: {e}")

_load_models()

DOCUMENT_TYPE_KEYWORDS = {
    "Rental Agreement": ["tenant", "landlord", "rent", "property", "lease", "premises", "security deposit", "eviction", "lock-in"],
    "Employment Contract": ["employee", "employer", "salary", "designation", "probation", "notice period", "company", "compensation"],
    "NDA": ["confidential", "non-disclosure", "proprietary", "trade secret", "disclosure", "receiving party"],
    "Loan Document": ["loan", "borrower", "lender", "interest rate", "emi", "repayment", "collateral", "default"],
    "Legal Notice": ["notice", "legal", "lawyer", "advocate", "demand", "respond", "failure", "consequences"],
    "Service Agreement": ["service", "vendor", "client", "deliverable", "payment terms", "service provider"],
    "Business Agreement": ["partnership", "joint venture", "profit sharing", "shareholder"],
    "Freelance Contract": ["freelancer", "contractor", "project", "deliverable", "independent contractor"],
}

RISK_PATTERNS = {
    "Rental Agreement": [
        {"pattern": r"immediate(ly)?\s+(evict|vacate)", "risk": "high", "title": "Immediate Eviction Clause", "description": "Landlord can evict without notice. Request minimum 30-day written notice."},
        {"pattern": r"lock.?in\s+period", "risk": "medium", "title": "Lock-in Period", "description": "You cannot leave before this period ends without financial penalty."},
        {"pattern": r"rent.?(increase|escalat).+(\d+)\s*%", "risk": "medium", "title": "Rent Escalation", "description": "Rent will increase periodically. Verify the percentage is reasonable (≤10-15%)."},
        {"pattern": r"owner.+right.+enter|landlord.+access\s+any", "risk": "high", "title": "Unrestricted Landlord Access", "description": "Landlord can enter without notice. Request 24-hour advance notice requirement."},
        {"pattern": r"tenant.+painting|painting.+cost.+tenant", "risk": "medium", "title": "Painting Cost on Tenant", "description": "You may be responsible for repainting costs on exit."},
        {"pattern": r"no\s+subletting|subletting.+prohibited", "risk": "low", "title": "No Subletting", "description": "You cannot sublet without landlord consent."},
    ],
    "Employment Contract": [
        {"pattern": r"non.?compete.+(\d+)\s*(month|year)", "risk": "high", "title": "Non-Compete Clause", "description": "You cannot work for competitors for the specified period after leaving."},
        {"pattern": r"bond.+amount|training.+bond|service.+bond", "risk": "high", "title": "Service Bond / Training Bond", "description": "You may owe money if you leave before the bond period ends."},
        {"pattern": r"moonlight|outside\s+employment\s+prohibited|second\s+job", "risk": "high", "title": "Anti-Moonlighting", "description": "You cannot do freelance or second job work during employment."},
        {"pattern": r"at.?will\s+termination|terminate\s+without\s+cause", "risk": "high", "title": "At-Will Termination", "description": "Employer can terminate you without cause or detailed notice."},
        {"pattern": r"ip\s+ownership|intellectual\s+property.+company", "risk": "medium", "title": "IP Ownership by Employer", "description": "Company owns all work you create, potentially including personal projects."},
        {"pattern": r"relocation.+required|transfer\s+anywhere", "risk": "medium", "title": "Forced Relocation", "description": "You may be required to relocate at employer's discretion."},
    ],
    "NDA": [
        {"pattern": r"perpetual|indefinite|no\s+time\s+limit|forever", "risk": "high", "title": "Perpetual Confidentiality", "description": "No time limit on obligation. Request a reasonable 3-5 year limit."},
        {"pattern": r"all\s+information|any\s+information|everything", "risk": "medium", "title": "Overly Broad Scope", "description": "Very broad definition of confidential information. Request specific carve-outs."},
        {"pattern": r"penalty.+(\d+)\s*(lakh|crore|thousand)", "risk": "high", "title": "Large Financial Penalty", "description": "Significant penalty for breach. Verify the amount is proportionate."},
        {"pattern": r"injunction|injunctive\s+relief", "risk": "medium", "title": "Injunction Rights", "description": "Other party can seek court order to stop you immediately."},
    ],
    "Loan Document": [
        {"pattern": r"prepayment\s+penalty|foreclosure\s+charge", "risk": "high", "title": "Prepayment Penalty", "description": "Penalty for paying loan early limits your financial flexibility."},
        {"pattern": r"guarantor|personal\s+guarantee", "risk": "high", "title": "Personal Guarantee", "description": "Guarantor is personally liable if you default — serious financial risk."},
        {"pattern": r"cross.?default|event\s+of\s+default", "risk": "high", "title": "Default Triggers", "description": "Multiple events can trigger default. Understand all default conditions."},
        {"pattern": r"compound\s+interest|compounding", "risk": "medium", "title": "Compound Interest", "description": "Interest compounds — total repayment will be significantly higher than principal."},
    ],
    "Legal Notice": [
        {"pattern": r"within\s+(\d+)\s*(day|week|hour)", "risk": "high", "title": "Response Deadline", "description": "You must respond within this time. Missing deadline may have legal consequences."},
        {"pattern": r"criminal\s+complaint|fir|police", "risk": "critical", "title": "Criminal Action Threatened", "description": "Threat of criminal action. Consult a criminal lawyer immediately."},
        {"pattern": r"legal\s+action|court\s+proceedings|litigation", "risk": "high", "title": "Legal Action Threatened", "description": "Sender is threatening to file a lawsuit. Consult a lawyer immediately."},
    ],
}

MISSING_CLAUSES = {
    "Rental Agreement": [
        {"name": "Security Deposit Refund Timeline", "priority": "high", "why": "Without a refund timeline, landlord may delay returning deposit indefinitely."},
        {"name": "Maintenance Responsibility Division", "priority": "high", "why": "Unclear maintenance responsibility leads to disputes about who pays for repairs."},
        {"name": "Rent Escalation Cap", "priority": "high", "why": "Without a cap, rent can be increased by any amount at renewal."},
        {"name": "Notice Period for Vacation", "priority": "high", "why": "Without clear notice period, either party may not have adequate time to prepare."},
        {"name": "Dispute Resolution Mechanism", "priority": "medium", "why": "Without this, disputes may require expensive litigation."},
    ],
    "Employment Contract": [
        {"name": "Salary Revision Policy", "priority": "medium", "why": "Without this, salary increases are entirely at employer's discretion with no timeline."},
        {"name": "Severance / Termination Benefits", "priority": "high", "why": "Without this, you may receive nothing beyond notice period on termination."},
        {"name": "Performance Review Process", "priority": "medium", "why": "Unclear performance review process can lead to subjective evaluations affecting your career."},
        {"name": "Leave Encashment Policy", "priority": "medium", "why": "Without this, accumulated leaves may not be paid out on exit."},
    ],
    "NDA": [
        {"name": "Confidentiality Duration Limit", "priority": "high", "why": "Without a time limit, obligation may last indefinitely — unusual and potentially unenforceable."},
        {"name": "Standard Exceptions to Confidentiality", "priority": "high", "why": "Public information, independently developed info should be excluded from confidentiality."},
        {"name": "Data Return or Deletion Clause", "priority": "medium", "why": "Without this, you may be required to retain confidential information indefinitely."},
    ],
}


def classify_document_type(text: str) -> Dict:
    # Try trained ML model first
    if _doc_model is not None and _doc_le is not None:
        try:
            pred = _doc_model.predict([text[:2000]])[0]
            proba = _doc_model.predict_proba([text[:2000]])[0]
            confidence = float(max(proba))
            doc_type = str(_doc_le.inverse_transform([pred])[0])
            return {"document_type": doc_type, "confidence": round(confidence, 2), "source": "ml_model"}
        except Exception as e:
            logger.warning(f"ML doc classification failed: {e}")
    # Fallback: keyword scoring
    text_lower = text.lower()
    scores = {k: sum(1 for kw in v if kw in text_lower) for k, v in DOCUMENT_TYPE_KEYWORDS.items()}
    if not scores or max(scores.values()) == 0:
        return {"document_type": "General Agreement", "confidence": 0.3, "source": "keyword"}
    best = max(scores, key=scores.get)
    total = sum(scores.values())
    return {"document_type": best, "confidence": min(0.95, scores[best] / total + 0.3) if total > 0 else 0.3, "source": "keyword"}


def run_rule_analysis(text: str, doc_type: str) -> Dict:
    text_lower = text.lower()
    patterns = RISK_PATTERNS.get(doc_type, [])
    findings = []
    risk_scores = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for p in patterns:
        if re.search(p["pattern"], text_lower, re.IGNORECASE):
            findings.append({"title": p["title"], "description": p["description"], "severity": p["risk"], "clause_reference": "Auto-detected"})
            risk_scores[p["risk"]] = risk_scores.get(p["risk"], 0) + 1
    score = min(100, risk_scores.get("critical", 0)*25 + risk_scores.get("high", 0)*15 + risk_scores.get("medium", 0)*8 + risk_scores.get("low", 0)*3)
    missing = [m for m in MISSING_CLAUSES.get(doc_type, []) if not re.search(m["name"].lower().replace(" ", ".?"), text_lower)]
    return {"risk_findings": findings, "rule_based_score": float(score), "missing_clauses": missing}


def classify_clause_risk(text: str) -> Dict:
    """Classify clause risk using best available model."""
    try:
        from app.ml.ml_service import classify_clause_risk as ml_classify
        return ml_classify(text)
    except Exception as e:
        logger.warning(f"ML service failed, using rule-based: {e}")
    # Pure rule-based fallback
    text_lower = text.lower()
    INDICATORS = {
        "critical": ["criminal complaint","fir","arrest","criminal action"],
        "high": ["terminate without cause","non-compete","bond amount","guarantor","moonlighting","at will"],
        "medium": ["lock-in","notice period","escalation","arbitration","ip ownership"],
        "low": ["renewal","force majeure","governing law","good faith"],
    }
    for level in ["critical","high","medium","low"]:
        matches = [ind for ind in INDICATORS[level] if ind in text_lower]
        if matches:
            return {"risk_level": level, "confidence": min(0.95, 0.6+len(matches)*0.1),
                    "matched_indicators": matches[:3], "reason": f"Rule: {', '.join(matches[:2])}", "source": "rule_based"}
    return {"risk_level": "low", "confidence": 0.5, "matched_indicators": [],
            "reason": "No significant risk indicators", "source": "rule_based"}


def extract_clauses(text: str) -> List[Dict]:
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
    clauses = []
    for i, para in enumerate(paragraphs[:20]):
        r = classify_clause_risk(para)
        clauses.append({
            "clause_number": i+1, "title": f"Section {i+1}",
            "original_text": para[:500], "risk_level": r["risk_level"],
            "confidence_score": r["confidence"], "risk_reason": r["reason"],
            "keywords": r["matched_indicators"],
            "lawyer_review_recommended": r["risk_level"] in ["high", "critical"]
        })
    return clauses


def extract_dates(text: str) -> List[Dict]:
    patterns = [r"within\s+(\d+)\s*(day|week|month|hour)s?", r"respond\s+within\s+(\d+)", r"notice\s+period\s+of\s+(\d+)\s*(day|month)"]
    dates = []
    for p in patterns:
        for m in re.findall(p, text, re.IGNORECASE)[:2]:
            dates.append({"description": f"Time requirement: {' '.join(m) if isinstance(m, tuple) else m}", "urgency": "high"})
    return dates[:4]


def extract_financial(text: str) -> List[Dict]:
    obls = []
    for p in [r"Rs\.?\s*([\d,]+)", r"₹\s*([\d,]+)", r"(\d+)\s*lakh", r"(\d+)\s*crore"]:
        for m in re.findall(p, text, re.IGNORECASE)[:2]:
            obls.append({"amount": m, "description": "Financial obligation found"})
    return obls[:4]


def compute_final_score(rule_score: float, ai_score: float, ml_score: float) -> Dict:
    final = round(0.40*rule_score + 0.35*ai_score + 0.25*ml_score, 1)
    if final <= 30: cat = "Low Risk"
    elif final <= 60: cat = "Medium Risk"
    elif final <= 80: cat = "High Risk"
    else: cat = "Critical Risk"
    return {"score": final, "category": cat}
