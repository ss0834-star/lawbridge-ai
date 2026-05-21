from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import User, Document, DocumentAnalysis, LocationProfile, LegalAidResource, AuditLog
from app.api.auth import auth_required
from app.services.location_service import INDIA_STATES, LEGAL_AID_DATA, get_checklist, get_resources_by_state, KNOW_YOUR_RIGHTS

location_router = APIRouter()
admin_router = APIRouter()
rights_router = APIRouter()

class LocationIn(BaseModel):
    city: Optional[str] = ""
    state: str
    pincode: Optional[str] = ""

@location_router.post("/update")
def update_location(data: LocationIn, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    loc = db.query(LocationProfile).filter(LocationProfile.user_id == user.id).first()
    if loc:
        loc.city = data.city; loc.state = data.state; loc.pincode = data.pincode
    else:
        loc = LocationProfile(user_id=user.id, city=data.city, state=data.state, pincode=data.pincode)
        db.add(loc)
    db.commit()
    return {"message": "Location updated", "state": data.state, "city": data.city}

@location_router.get("/resources")
def get_resources(state: Optional[str] = None, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    if not state:
        loc = db.query(LocationProfile).filter(LocationProfile.user_id == user.id).first()
        state = loc.state if loc else None
    resources = db.query(LegalAidResource).filter(LegalAidResource.state == state).all() if state else []
    if not resources:
        resources = db.query(LegalAidResource).all()[:3]
    return [{"id": r.id, "name": r.name, "resource_type": r.resource_type, "city": r.city, "state": r.state,
             "address": r.address, "phone": r.phone, "website": r.website, "description": r.description, "is_free": r.is_free} for r in resources]

@location_router.get("/checklist")
def get_loc_checklist(state: str, document_type: str = "Rental Agreement", user: User = Depends(auth_required)):
    return {"state": state, "document_type": document_type, "checklist": get_checklist(state, document_type)}

@location_router.get("/states")
def list_states():
    return {"states": INDIA_STATES}

@location_router.get("/my")
def my_location(db: Session = Depends(get_db), user: User = Depends(auth_required)):
    loc = db.query(LocationProfile).filter(LocationProfile.user_id == user.id).first()
    return {"city": loc.city if loc else "", "state": loc.state if loc else "", "set": loc is not None}


# ── Know Your Rights ──────────────────────────────────────────────────────────

@rights_router.get("/categories")
def rights_categories():
    return {"categories": [
        {"key": "tenant", "title": "Tenant Rights", "icon": "🏠", "description": "Rental agreements, deposits, eviction, landlord disputes"},
        {"key": "employee", "title": "Employee Rights", "icon": "💼", "description": "Salary, notice period, termination, PF, gratuity"},
        {"key": "consumer", "title": "Consumer Rights", "icon": "🛒", "description": "Defective products, refunds, e-commerce, complaints"},
        {"key": "digital", "title": "Digital Rights", "icon": "🔐", "description": "Privacy, cybercrime, social media, data protection"},
    ]}

@rights_router.get("/{category}")
def get_rights(category: str, user: User = Depends(auth_required)):
    data = KNOW_YOUR_RIGHTS.get(category)
    if not data: raise HTTPException(404, "Category not found")
    return data


# ── Admin ─────────────────────────────────────────────────────────────────────

def require_admin(user: User = Depends(auth_required)):
    if user.role != "admin": raise HTTPException(403, "Admin access required")
    return user

@admin_router.get("/stats")
def stats(db: Session = Depends(get_db), user: User = Depends(require_admin)):
    from app.models import LegalQuery
    total_users = db.query(func.count(User.id)).scalar()
    total_docs = db.query(func.count(Document.id)).scalar()
    total_analyses = db.query(func.count(DocumentAnalysis.id)).scalar()
    total_queries = db.query(func.count(LegalQuery.id)).scalar()
    avg_risk = db.query(func.avg(DocumentAnalysis.overall_risk_score)).scalar() or 0
    analyses = db.query(DocumentAnalysis).all()
    risk_dist = {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0, "Critical Risk": 0}
    for a in analyses:
        if a.risk_category in risk_dist: risk_dist[a.risk_category] += 1
    doc_types = {}
    for d in db.query(Document).all():
        dt = d.document_type or "Unknown"
        doc_types[dt] = doc_types.get(dt, 0) + 1
    return {"total_users": total_users, "total_documents": total_docs, "total_analyses": total_analyses,
            "total_legal_queries": total_queries, "avg_risk_score": round(float(avg_risk), 1),
            "risk_distribution": risk_dist, "document_types": doc_types}

@admin_router.get("/users")
def admin_users(db: Session = Depends(get_db), user: User = Depends(require_admin)):
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role, "created_at": u.created_at.isoformat()} for u in db.query(User).order_by(User.created_at.desc()).all()]

@admin_router.get("/system-health")
def health(db: Session = Depends(get_db), user: User = Depends(require_admin)):
    from app.services.cache_service import redis_health
    from sqlalchemy import text
    db_ok = "connected"
    try: db.execute(text("SELECT 1"))
    except: db_ok = "disconnected"
    return {"database": db_ok, "redis": redis_health(), "status": "operational"}

@admin_router.get("/audit-logs")
def audit_logs(db: Session = Depends(get_db), user: User = Depends(require_admin)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(50).all()
    return [{"id": l.id, "user_id": l.user_id, "action": l.action, "resource_type": l.resource_type, "created_at": l.created_at.isoformat()} for l in logs]
