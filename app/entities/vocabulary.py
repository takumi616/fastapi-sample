from pydantic import BaseModel

class Vocabulary(BaseModel):
    vocabulary_no: int | None = None
    title: str
    meaning: str
    sentence: str