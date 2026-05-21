from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Document, DocumentAnalysis, Clause, RiskFinding, MissingClause, NegotiationPoint, LawyerQuestion, AuditLog
from app.api.auth import auth_required
from app.ml.features import run_rule_analysis, extract_clauses, extract_dates, extract_financial, compute_final_score
from app.services.ai_service import analyze_document_ai
import time

router = APIRouter()

@router.post("/start/{doc_id}")
def start_analysis(doc_id: int, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.user_id == user.id).first()
    if not doc: raise HTTPException(404, "Document not found")
    if not doc.extracted_text: raise HTTPException(400, "No extractable text in document")
    existing = db.query(DocumentAnalysis).filter(DocumentAnalysis.document_id == doc_id).first()
    if existing and existing.status == "completed":
        return _analysis_out(existing, db)
    t0 = time.time()
    doc.status = "analyzing"
    db.commit()
    try:
        text = doc.extracted_text
        doc_type = doc.document_type or "General Agreement"
        rule = run_rule_analysis(text, doc_type)
        clauses_data = extract_clauses(text)
        ai_data = analyze_document_ai(text, doc_type, rule["risk_findings"], doc.language)
        ai_score = float(ai_data.get("ai_risk_score", 50))
        ml_score = min(100.0, float(len(rule["risk_findings"]) * 10 + 20))
        final = compute_final_score(rule["rule_based_score"], ai_score, ml_score)
        analysis = DocumentAnalysis(
            document_id=doc_id, user_id=user.id,
            overall_risk_score=final["score"], risk_category=final["category"],
            rule_based_score=rule["rule_based_score"], llm_score=ai_score, ml_score=ml_score,
            executive_summary=ai_data.get("executive_summary", ""),
            what_it_means=ai_data.get("what_it_means", ""),
            important_dates=extract_dates(text),
            financial_obligations=extract_financial(text),
            party_obligations=[], ambiguous_terms=[],
            status="completed", processing_time_seconds=round(time.time()-t0, 2)
        )
        db.add(analysis)
        db.flush()
        for i, c in enumerate(clauses_data[:15]):
            db.add(Clause(analysis_id=analysis.id, clause_number=c["clause_number"], title=c["title"],
                          original_text=c["original_text"], plain_english=f"This clause establishes specific terms — see AI analysis for plain-English explanation.",
                          risk_level=c["risk_level"], risk_reason=c["risk_reason"], confidence_score=c["confidence_score"],
                          keywords=c["keywords"], lawyer_review_recommended=c["lawyer_review_recommended"]))
        for f in rule["risk_findings"][:10]:
            db.add(RiskFinding(analysis_id=analysis.id, title=f["title"], description=f["description"], severity=f["severity"], clause_reference=f.get("clause_reference","")))
        for m in rule["missing_clauses"][:8]:
            db.add(MissingClause(analysis_id=analysis.id, clause_name=m["name"], why_important=m["why"],
                                 suggested_text=f"Consider adding a clause that clearly defines {m['name'].lower()}.", priority=m["priority"]))
        for np in ai_data.get("negotiation_points", [])[:5]:
            db.add(NegotiationPoint(analysis_id=analysis.id, title=np.get("title",""), current_text=np.get("current",""),
                                    suggested_change=np.get("suggested",""), reason=np.get("reason",""), priority="medium"))
        for q in ai_data.get("lawyer_questions", [])[:7]:
            db.add(LawyerQuestion(analysis_id=analysis.id, question=q, category="General", priority="high"))
        doc.status = "analyzed"
        db.add(AuditLog(user_id=user.id, action="analysis_complete", resource_type="analysis", log_data={"doc_id": doc_id, "score": final["score"]}))
        db.commit()
        db.refresh(analysis)
        return _analysis_out(analysis, db)
    except Exception as e:
        doc.status = "error"
        db.commit()
        raise HTTPException(500, f"Analysis failed: {str(e)}")

@router.get("/{doc_id}")
def get_analysis(doc_id: int, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.user_id == user.id).first()
    if not doc: raise HTTPException(404, "Document not found")
    a = db.query(DocumentAnalysis).filter(DocumentAnalysis.document_id == doc_id).first()
    if not a: raise HTTPException(404, "No analysis found. Start analysis first.")
    return _analysis_out(a, db)

def _analysis_out(a: DocumentAnalysis, db):
    return {
        "id": a.id, "document_id": a.document_id,
        "overall_risk_score": a.overall_risk_score, "risk_category": a.risk_category,
        "rule_based_score": a.rule_based_score, "llm_score": a.llm_score, "ml_score": a.ml_score,
        "executive_summary": a.executive_summary, "what_it_means": a.what_it_means,
        "important_dates": a.important_dates or [], "financial_obligations": a.financial_obligations or [],
        "status": a.status, "created_at": a.created_at.isoformat(),
        "clauses": [{"id": c.id, "clause_number": c.clause_number, "title": c.title, "original_text": c.original_text,
                     "plain_english": c.plain_english, "risk_level": c.risk_level, "risk_reason": c.risk_reason,
                     "confidence_score": c.confidence_score, "keywords": c.keywords or [],
                     "lawyer_review_recommended": c.lawyer_review_recommended} for c in a.clauses],
        "risk_findings": [{"id": r.id, "title": r.title, "description": r.description, "severity": r.severity, "clause_reference": r.clause_reference} for r in a.risk_findings],
        "missing_clauses": [{"id": m.id, "clause_name": m.clause_name, "why_important": m.why_important, "priority": m.priority} for m in a.missing_clauses],
        "negotiation_points": [{"id": n.id, "title": n.title, "current_text": n.current_text, "suggested_change": n.suggested_change, "reason": n.reason} for n in a.negotiation_points],
        "lawyer_questions": [{"id": q.id, "question": q.question, "category": q.category, "priority": q.priority} for q in a.lawyer_questions],
    }
