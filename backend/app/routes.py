from fastapi import APIRouter
from app.models import Question, Answer
from app.services import get_answer_and_image

router = APIRouter()

@router.post("/ask", response_model=Answer)
def ask_question(data: Question):
    return get_answer_and_image(data.query)
