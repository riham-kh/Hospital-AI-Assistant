
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Hospital Knowledge Assistant")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Hospital AI Assistant is running!"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return {
        "question": request.question,
        "answer": "This is a placeholder answer. AI coming soon!"
    }
