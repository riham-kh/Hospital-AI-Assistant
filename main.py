
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_service import generate_answer
from fastapi import UploadFile, File, HTTPException
from document_service import extract_pdf_pages
from database import save_document

app = FastAPI(title="Hospital Knowledge Assistant")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Hospital AI Assistant is running!"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    answer = generate_answer(request.question)

    return {
        "question": request.question,
        "answer": answer
    }



@app.post("/documents/upload")
def upload_document(file: UploadFile = File(...)):
    filename = file.filename or "document.pdf"

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    try:
        pages = extract_pdf_pages(file.file)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Could not read the PDF"
        ) from exc
    finally:
        file.file.close()

    if not pages:
        raise HTTPException(
            status_code=400,
            detail="No extractable text found in the PDF"
        )

    result = save_document(filename, pages)

    return {
        "message": "Document uploaded successfully",
        **result
    }
