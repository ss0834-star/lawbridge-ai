from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine
from app.models import Base
from app.api.auth import router as auth_router
from app.api.documents import router as docs_router
from app.api.analysis import router as analysis_router
from app.api.chat import chat_router, qa_router
from app.api.location_admin import location_router, admin_router, rights_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LawBridge AI", description="India's AI legal document intelligence platform", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(docs_router, prefix="/documents", tags=["Documents"])
app.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(qa_router, prefix="/legal-qa", tags=["Legal Q&A"])
app.include_router(location_router, prefix="/location", tags=["Location"])
app.include_router(rights_router, prefix="/rights", tags=["Know Your Rights"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

@app.get("/health")
def health():
    from app.services.cache_service import redis_health
    from app.database import SessionLocal
    from sqlalchemy import text
    db_status = "connected"
    try:
        db = SessionLocal(); db.execute(text("SELECT 1")); db.close()
    except: db_status = "disconnected"
    return {"status": "ok", "database": db_status, "redis": redis_health(), "version": "2.0.0"}

@app.get("/")
def root():
    return {"message": "LawBridge AI v2", "docs": "/docs", "health": "/health"}

@app.on_event("startup")
def on_startup():
    try:
        from app.database import SessionLocal
        from app.models import User
        db = SessionLocal()
        if db.query(User).count() == 0:
            print("📦 Auto-seeding database...")
            _seed(db)
        db.close()
    except Exception as e:
        print(f"⚠️ Startup seed failed: {e}")

def _seed(db):
    from app.models import User, LegalAidResource
    from app.api.auth import hash_pw
    from app.services.location_service import LEGAL_AID_DATA
    for model in [User, LegalAidResource]:
        db.query(model).delete()
    db.commit()
    admin = User(name="Admin", email="admin@lawbridge.ai", password_hash=hash_pw("admin123"), role="admin")
    demo = User(name="Priya Sharma", email="demo@lawbridge.ai", password_hash=hash_pw("demo123"), role="user", is_demo=True, disclaimer_accepted=True)
    demo2 = User(name="Rahul Verma", email="rahul@lawbridge.ai", password_hash=hash_pw("demo123"), role="user", disclaimer_accepted=True)
    for u in [admin, demo, demo2]: db.add(u)
    for r in LEGAL_AID_DATA: db.add(LegalAidResource(**r))
    db.commit()
    print("✅ Seed complete — admin@lawbridge.ai/admin123, demo@lawbridge.ai/demo123")
