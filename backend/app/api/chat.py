from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.models import User, Document, ChatSession, ChatMessage, LegalQuery
from app.api.auth import auth_required
from app.services.ai_service import chat_about_document, answer_legal_question

chat_router = APIRouter()
qa_router = APIRouter()


class CreateSession(BaseModel):
    document_id: Optional[int] = None
    language: Optional[str] = "English"
    session_type: Optional[str] = "document"

class SendMessage(BaseModel):
    session_id: int
    content: str
    language: Optional[str] = "English"

class AskQuestion(BaseModel):
    question: str
    language: Optional[str] = "English"
    context: Optional[str] = ""
    category: Optional[str] = "General"


# ── Chat (document-focused) ────────────────────────────────────────────────────

@chat_router.post("/session")
def create_session(data: CreateSession, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    title = "General Legal Chat"
    if data.document_id:
        doc = db.query(Document).filter(Document.id == data.document_id, Document.user_id == user.id).first()
        if doc: title = f"About: {doc.original_filename or doc.document_type}"
    s = ChatSession(user_id=user.id, document_id=data.document_id, title=title, language=data.language, session_type=data.session_type or "document")
    db.add(s)
    db.commit()
    db.refresh(s)
    return _session_out(s)

@chat_router.get("/session/{sid}")
def get_session(sid: int, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    s = db.query(ChatSession).filter(ChatSession.id == sid, ChatSession.user_id == user.id).first()
    if not s: raise HTTPException(404, "Session not found")
    return _session_out(s)

@chat_router.post("/message")
def send_message(data: SendMessage, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    s = db.query(ChatSession).filter(ChatSession.id == data.session_id, ChatSession.user_id == user.id).first()
    if not s: raise HTTPException(404, "Session not found")
    user_msg = ChatMessage(session_id=data.session_id, role="user", content=data.content)
    db.add(user_msg)
    db.flush()
    doc_text, doc_type = "", "General Agreement"
    if s.document_id:
        doc = db.query(Document).filter(Document.id == s.document_id).first()
        if doc:
            doc_text = doc.extracted_text or ""
            doc_type = doc.document_type or "General Agreement"
    history = [{"role": m.role, "content": m.content} for m in db.query(ChatMessage).filter(ChatMessage.session_id == data.session_id).order_by(ChatMessage.created_at).limit(10).all()]
    if doc_text:
        ai_response = chat_about_document(data.content, doc_text, doc_type, history, data.language or s.language)
    else:
        ai_response = answer_legal_question(data.content, data.language or s.language)
    ai_msg = ChatMessage(session_id=data.session_id, role="assistant", content=ai_response)
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)
    return {"id": ai_msg.id, "role": ai_msg.role, "content": ai_msg.content, "created_at": ai_msg.created_at.isoformat()}

@chat_router.get("/sessions")
def list_sessions(db: Session = Depends(get_db), user: User = Depends(auth_required)):
    return [_session_out(s) for s in db.query(ChatSession).filter(ChatSession.user_id == user.id).order_by(ChatSession.created_at.desc()).limit(20).all()]

@chat_router.get("/document/{doc_id}")
def get_doc_sessions(doc_id: int, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    return [_session_out(s) for s in db.query(ChatSession).filter(ChatSession.document_id == doc_id, ChatSession.user_id == user.id).all()]

def _session_out(s: ChatSession):
    return {"id": s.id, "title": s.title, "language": s.language, "session_type": s.session_type,
            "document_id": s.document_id, "created_at": s.created_at.isoformat(),
            "messages": [{"id": m.id, "role": m.role, "content": m.content, "created_at": m.created_at.isoformat()} for m in s.messages]}


# ── General Legal Q&A ─────────────────────────────────────────────────────────

@qa_router.post("/ask")
def ask_legal_question(data: AskQuestion, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    """Ask any Indian law question — no document required."""
    answer = answer_legal_question(data.question, data.language or "English", data.context or "")
    query = LegalQuery(user_id=user.id, question=data.question, answer=answer, category=data.category or "General", language=data.language or "English")
    db.add(query)
    db.commit()
    db.refresh(query)
    return {"id": query.id, "question": query.question, "answer": query.answer, "category": query.category, "created_at": query.created_at.isoformat()}

@qa_router.get("/history")
def qa_history(db: Session = Depends(get_db), user: User = Depends(auth_required)):
    queries = db.query(LegalQuery).filter(LegalQuery.user_id == user.id).order_by(LegalQuery.created_at.desc()).limit(20).all()
    return [{"id": q.id, "question": q.question, "answer": q.answer, "category": q.category, "created_at": q.created_at.isoformat()} for q in queries]

@qa_router.get("/popular")
def popular_questions():
    """Curated common Indian legal questions."""
    return {"questions": [
        {"category": "Tenant Rights", "question": "What are my rights if my landlord refuses to return my security deposit?"},
        {"category": "Employment", "question": "Can my employer force me to work more than 8 hours without overtime pay?"},
        {"category": "Consumer", "question": "How do I file a consumer complaint against an e-commerce company?"},
        {"category": "Criminal", "question": "What should I do if the police refuse to file my FIR?"},
        {"category": "Digital Rights", "question": "What are my rights if someone is misusing my photos online?"},
        {"category": "NDA", "question": "Can a non-compete clause stop me from joining a competitor in India?"},
        {"category": "Property", "question": "What documents should I check before buying a flat in India?"},
        {"category": "Family Law", "question": "What is the process for filing for divorce in India?"},
        {"category": "RTI", "question": "How do I file an RTI application and what can I ask for?"},
        {"category": "Labour", "question": "My employer hasn't paid salary for 2 months. What can I do?"},
    ]}
