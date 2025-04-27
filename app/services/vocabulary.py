from app.db.repositories import vocabulary as repository
from app.models.vocabulary import VocabularyCreateRequest

async def create_vocabulary(db, vocabulary: VocabularyCreateRequest) -> int:
    rows_affected = await repository.insert_vocabulary(db, vocabulary)
    return rows_affected

async def fetch_all_vocabularies(db) -> list:
    rows = await repository.select_all_vocabularies(db=db)
    return rows
