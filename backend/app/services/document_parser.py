import io
def parse_document(content: bytes, filename: str) -> str:
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    if ext == 'pdf':
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            return "\n".join(p.extract_text() or '' for p in reader.pages).strip()
        except Exception as e:
            return f"[PDF extraction note: {e}. Paste text manually for best results.]"
    elif ext == 'docx':
        try:
            from docx import Document
            doc = Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs).strip()
        except Exception as e:
            return f"[DOCX extraction note: {e}]"
    return content.decode('utf-8', errors='ignore')
