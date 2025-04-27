from fastapi import APIRouter, Request, HTTPException
from app.entities.vocabulary import Vocabulary
from app.routers.models.vocabulary import VocabularyCreateRequest, VocabularyCreateResponse, VocabularyListResponse, VocabularyResponse
from app.services import vocabulary as service

router = APIRouter()

@router.post("/vocabularies", response_model=VocabularyCreateResponse)
async def create_vocabulary(request: Request, body: VocabularyCreateRequest) -> VocabularyCreateResponse:
    # Get a DB connection
    db = request.app.state.db_pool

    # Transform the request model into the vocabulary entity
    vocabulary = Vocabulary(
        title=body.title,
        meaning=body.meaning,
        sentence=body.sentence
    )

    # Execute the service
    try:
        rows_affected = await service.create_vocabulary(db, vocabulary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return the response
    return VocabularyCreateResponse(rows_affected=rows_affected)

@router.get("/vocabularies", response_model=VocabularyListResponse)
async def fetch_all_vocabularies(request: Request) -> VocabularyListResponse:
    # Get a DB connection
    db = request.app.state.db_pool

    # Execute the service
    try:
        vocabularies = await service.fetch_all_vocabularies(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return the response
    vocabularies=[VocabularyResponse(**vocabulary.model_dump()) for vocabulary in vocabularies]
    return VocabularyListResponse(vocabularies=vocabularies)
