from fastapi import APIRouter, Request, HTTPException
from app.entities.vocabulary import Vocabulary
from app.routers.models.vocabulary import RowsAffectedResponse, VocabularyRequest, VocabularyListResponse, VocabularyResponse
from app.services import vocabulary as service

router = APIRouter()

@router.post("/vocabularies", response_model=RowsAffectedResponse)
async def create_vocabulary(request: Request, body: VocabularyRequest) -> RowsAffectedResponse:
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
    return RowsAffectedResponse(rows_affected=rows_affected)

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

@router.get("/vocabularies/{vocabulary_no}", response_model=VocabularyResponse)
async def fetch_vocabulary_by_id(request: Request, vocabulary_no: int) -> VocabularyResponse:
    # Get a DB connection
    db = request.app.state.db_pool

    # Execute the service
    try:
        vocabulary = await service.fetch_vocabulary_by_id(db, vocabulary_no)

        if vocabulary is None:
            raise HTTPException(status_code=404, detail="Vocabulary not found")

        # Return the response
        return VocabularyResponse(**vocabulary.model_dump())

    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/vocabularies/{vocabulary_no}", response_model=RowsAffectedResponse)
async def update_vocabulary(request: Request, vocabulary_no: int, body: VocabularyRequest) -> RowsAffectedResponse:
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
        rows_affected = await service.update_vocabulary(db, vocabulary_no, vocabulary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return the response
    return RowsAffectedResponse(rows_affected=rows_affected)
