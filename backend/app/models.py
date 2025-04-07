from pydantic import BaseModel

class Question(BaseModel):
    query: str

class Answer(BaseModel):
    answer: str
    image_url: str
