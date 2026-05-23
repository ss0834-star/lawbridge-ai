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
    resources = get_resources_by_state(state) if state else [r for r in LEGAL_AID_DATA if "NALSA" in r["name"]]
    return [{"id": i + 1, **r} for i, r in enumerate(resources)]

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


# ── Nearest DLSA by GPS ───────────────────────────────────────────────────────
from app.services.district_service import get_nearest_dlsa

@location_router.get("/nearest")
def nearest_dlsa(lat: float, lon: float, limit: int = 3, user: User = Depends(auth_required)):
    results = get_nearest_dlsa(lat, lon, limit)
    return {"nearest": results, "count": len(results)}


# ── Google Places Nearby Legal Aid ────────────────────────────────────────────
import httpx
import os

@location_router.get("/places-nearby")
async def places_nearby(lat: float, lon: float, user: User = Depends(auth_required)):
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return {"places": [], "error": "Places API not configured"}
    try:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lon}",
            "radius": 5000,
            "keyword": "legal aid lawyer advocate court",
            "type": "lawyer",
            "key": api_key
        }
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(url, params=params)
            data = res.json()
        places = []
        for p in data.get("results", [])[:5]:
            places.append({
                "name": p.get("name"),
                "address": p.get("vicinity"),
                "rating": p.get("rating"),
                "open_now": p.get("opening_hours", {}).get("open_now"),
                "lat": p["geometry"]["location"]["lat"],
                "lon": p["geometry"]["location"]["lng"],
                "place_id": p.get("place_id"),
                "directions_url": f"https://www.google.com/maps/dir/?api=1&destination={p['geometry']['location']['lat']},{p['geometry']['location']['lng']}&destination_place_id={p.get('place_id')}",
                "maps_url": f"https://www.google.com/maps/place/?q=place_id:{p.get('place_id')}"
            })
        return {"places": places, "count": len(places)}
    except Exception as e:
        return {"places": [], "error": str(e)}


# ── Google Places Nearby Legal Aid v2 ────────────────────────────────────────
@location_router.get("/places-nearby-v2")
async def places_nearby_v2(lat: float, lon: float, user: User = Depends(auth_required)):
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return {"places": [], "error": "Places API not configured"}
    try:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lon}",
            "radius": 10000,
            "keyword": "advocate lawyer legal",
            "key": api_key
        }
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.get(url, params=params)
            data = res.json()
        if data.get("status") != "OK":
            return {"places": [], "error": data.get("status"), "message": data.get("error_message", "")}
        places = []
        for p in data.get("results", [])[:6]:
            places.append({
                "name": p.get("name"),
                "address": p.get("vicinity"),
                "rating": p.get("rating"),
                "total_ratings": p.get("user_ratings_total"),
                "open_now": p.get("opening_hours", {}).get("open_now"),
                "lat": p["geometry"]["location"]["lat"],
                "lon": p["geometry"]["location"]["lng"],
                "place_id": p.get("place_id"),
                "directions_url": f"https://www.google.com/maps/dir/?api=1&destination={p['geometry']['location']['lat']},{p['geometry']['location']['lng']}",
                "maps_url": f"https://www.google.com/maps/place/?q=place_id:{p.get('place_id')}"
            })
        return {"places": places, "count": len(places), "status": data.get("status")}
    except Exception as e:
        return {"places": [], "error": str(e)}
