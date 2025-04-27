from typing import List
from pydantic import BaseModel

class VocabularyCreateRequest(BaseModel):
    title: str
    meaning: str
    sentence: str

class VocabularyCreateResponse(BaseModel):
    rows_affected: int

class VocabularyResponse(BaseModel):
    vocabulary_no: int
    title: str
    meaning: str
    sentence: str

class VocabularyListResponse(BaseModel):
    vocabularies: List[VocabularyResponse]