
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_service import generate_answer

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
