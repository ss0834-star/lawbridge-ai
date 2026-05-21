from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import User, Document, AuditLog
from app.api.auth import auth_required
from app.services.document_parser import parse_document
from app.ml.features import classify_document_type

router = APIRouter()
ALLOWED = {"pdf", "docx", "txt"}
MAX_BYTES = 10 * 1024 * 1024

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(None),
    language: Optional[str] = Form("English"),
    db: Session = Depends(get_db),
    user: User = Depends(auth_required)
):
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED:
        raise HTTPException(400, f"Unsupported file type. Use: {', '.join(ALLOWED)}")
    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(400, "File too large. Max 10MB.")
    text = parse_document(content, file.filename)
    if not document_type:
        document_type = classify_document_type(text)["document_type"]
    doc = Document(user_id=user.id, filename=file.filename, original_filename=file.filename,
                   document_type=document_type, file_size=len(content), extracted_text=text,
                   language=language, status="uploaded")
    db.add(doc)
    db.add(AuditLog(user_id=user.id, action="upload", resource_type="document", log_data={"filename": file.filename}))
    db.commit()
    db.refresh(doc)
    return _doc_out(doc)

@router.get("")
def list_docs(db: Session = Depends(get_db), user: User = Depends(auth_required)):
    return [_doc_out(d) for d in db.query(Document).filter(Document.user_id == user.id).order_by(Document.created_at.desc()).all()]

@router.get("/{doc_id}")
def get_doc(doc_id: int, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    d = db.query(Document).filter(Document.id == doc_id, Document.user_id == user.id).first()
    if not d: raise HTTPException(404, "Document not found")
    return _doc_out(d)

@router.delete("/{doc_id}")
def delete_doc(doc_id: int, db: Session = Depends(get_db), user: User = Depends(auth_required)):
    d = db.query(Document).filter(Document.id == doc_id, Document.user_id == user.id).first()
    if not d: raise HTTPException(404, "Document not found")
    db.delete(d)
    db.commit()
    return {"message": "Deleted"}

def _doc_out(d: Document):
    return {"id": d.id, "filename": d.filename, "original_filename": d.original_filename,
            "document_type": d.document_type, "file_size": d.file_size, "language": d.language,
            "status": d.status, "created_at": d.created_at.isoformat()}
