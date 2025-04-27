from fastapi import APIRouter, Request, HTTPException
from app.models.vocabulary import VocabularyCreateRequest, VocabularyCreateResponse, VocabularyListResponse, VocabularyResponse
from app.services import vocabulary as service

router = APIRouter()

@router.post("/vocabularies", response_model=VocabularyCreateResponse)
async def create_vocabulary(request: Request, body: VocabularyCreateRequest):
    db = request.app.state.db_pool
    try:
        rows_affected = await service.create_vocabulary(db, body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return VocabularyCreateResponse(rows_affected=rows_affected)

@router.get("/vocabularies", response_model=VocabularyListResponse)
async def fetch_all_vocabularies(request: Request):
    db = request.app.state.db_pool
    try:
        rows = await service.fetch_all_vocabularies(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return VocabularyListResponse(vocabularies=[VocabularyResponse(**row) for row in rows])
