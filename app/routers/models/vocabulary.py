from typing import List
from pydantic import BaseModel

class VocabularyRequest(BaseModel):
    title: str
    meaning: str
    sentence: str

class RowsAffectedResponse(BaseModel):
    rows_affected: int

class VocabularyResponse(BaseModel):
    vocabulary_no: int
    title: str
    meaning: str
    sentence: str

class VocabularyListResponse(BaseModel):
    vocabularies: List[VocabularyResponse]