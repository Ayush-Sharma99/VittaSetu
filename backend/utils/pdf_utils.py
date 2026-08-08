# utils/pdf_utils.py

def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file using PyMuPDF or pypdf fallback."""
    # Try PyMuPDF (fitz) first
    try:
        import fitz
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        if text.strip():
            return text
    except Exception as e:
        print(f"PyMuPDF failed or not found: {e}. Falling back to pypdf.")

    # Fallback to pure-python pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t
        return text
    except Exception as e:
        print(f"pypdf extraction failed: {e}")
        return ""
