from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password_hash = Column(String(500))
    role = Column(String(50), default="user")
    is_demo = Column(Boolean, default=False)
    disclaimer_accepted = Column(Boolean, default=False)
    preferred_language = Column(String(50), default="English")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    legal_queries = relationship("LegalQuery", back_populates="user", cascade="all, delete-orphan")
    location_profile = relationship("LocationProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500))
    document_type = Column(String(100))
    file_size = Column(Integer)
    extracted_text = Column(Text)
    language = Column(String(50), default="English")
    status = Column(String(50), default="uploaded")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="documents")
    analysis = relationship("DocumentAnalysis", back_populates="document", uselist=False, cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="document", cascade="all, delete-orphan")


class DocumentAnalysis(Base):
    __tablename__ = "document_analyses"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    overall_risk_score = Column(Float)
    risk_category = Column(String(50))
    rule_based_score = Column(Float)
    llm_score = Column(Float)
    ml_score = Column(Float)
    executive_summary = Column(Text)
    what_it_means = Column(Text)
    important_dates = Column(JSON)
    financial_obligations = Column(JSON)
    party_obligations = Column(JSON)
    ambiguous_terms = Column(JSON)
    status = Column(String(50), default="pending")
    processing_time_seconds = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    document = relationship("Document", back_populates="analysis")
    clauses = relationship("Clause", back_populates="analysis", cascade="all, delete-orphan")
    risk_findings = relationship("RiskFinding", back_populates="analysis", cascade="all, delete-orphan")
    missing_clauses = relationship("MissingClause", back_populates="analysis", cascade="all, delete-orphan")
    negotiation_points = relationship("NegotiationPoint", back_populates="analysis", cascade="all, delete-orphan")
    lawyer_questions = relationship("LawyerQuestion", back_populates="analysis", cascade="all, delete-orphan")


class Clause(Base):
    __tablename__ = "clauses"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("document_analyses.id"), nullable=False)
    clause_number = Column(Integer)
    title = Column(String(300))
    original_text = Column(Text)
    plain_english = Column(Text)
    risk_level = Column(String(50))
    risk_reason = Column(Text)
    confidence_score = Column(Float)
    suggested_action = Column(Text)
    keywords = Column(JSON)
    lawyer_review_recommended = Column(Boolean, default=False)
    analysis = relationship("DocumentAnalysis", back_populates="clauses")


class RiskFinding(Base):
    __tablename__ = "risk_findings"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("document_analyses.id"), nullable=False)
    title = Column(String(300))
    description = Column(Text)
    severity = Column(String(50))
    clause_reference = Column(String(200))
    analysis = relationship("DocumentAnalysis", back_populates="risk_findings")


class MissingClause(Base):
    __tablename__ = "missing_clauses"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("document_analyses.id"), nullable=False)
    clause_name = Column(String(300))
    why_important = Column(Text)
    suggested_text = Column(Text)
    priority = Column(String(50))
    analysis = relationship("DocumentAnalysis", back_populates="missing_clauses")


class NegotiationPoint(Base):
    __tablename__ = "negotiation_points"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("document_analyses.id"), nullable=False)
    title = Column(String(300))
    current_text = Column(Text)
    suggested_change = Column(Text)
    reason = Column(Text)
    priority = Column(String(50))
    analysis = relationship("DocumentAnalysis", back_populates="negotiation_points")


class LawyerQuestion(Base):
    __tablename__ = "lawyer_questions"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("document_analyses.id"), nullable=False)
    question = Column(Text)
    category = Column(String(100))
    priority = Column(String(50))
    analysis = relationship("DocumentAnalysis", back_populates="lawyer_questions")


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    title = Column(String(300))
    session_type = Column(String(50), default="document")  # document | general | rights
    language = Column(String(50), default="English")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="chat_sessions")
    document = relationship("Document", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20))
    content = Column(Text)
    clause_references = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    session = relationship("ChatSession", back_populates="messages")


class LegalQuery(Base):
    """General legal questions not tied to a document."""
    __tablename__ = "legal_queries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    category = Column(String(100))
    language = Column(String(50), default="English")
    helpful_votes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="legal_queries")


class LocationProfile(Base):
    __tablename__ = "location_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    city = Column(String(200))
    state = Column(String(200))
    pincode = Column(String(20))
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="location_profile")


class LegalAidResource(Base):
    __tablename__ = "legal_aid_resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300))
    resource_type = Column(String(100))
    city = Column(String(200))
    state = Column(String(200))
    address = Column(Text)
    phone = Column(String(50))
    website = Column(String(300))
    description = Column(Text)
    is_free = Column(Boolean, default=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(200))
    resource_type = Column(String(100))
    resource_id = Column(Integer)
    log_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="audit_logs")
