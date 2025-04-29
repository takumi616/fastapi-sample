from app.db.repositories import vocabulary as repository
from app.entities.vocabulary import Vocabulary

async def create_vocabulary(db, vocabulary: Vocabulary) -> int:
    # Execute the repository
    rows_affected = await repository.insert_vocabulary(db, vocabulary)
    return rows_affected

async def fetch_all_vocabularies(db) -> list[Vocabulary]:
    # Execute the repository
    vocabularies = await repository.select_all_vocabularies(db=db)
    return vocabularies

async def fetch_vocabulary_by_id(db, vocabulary_no) -> Vocabulary | None:
    # Execute the repository
    vocabulary = await repository.select_vocabulary_by_id(db=db, vocabulary_no=vocabulary_no)
    return vocabulary

async def update_vocabulary(db, vocabulary_no: int, vocabulary: Vocabulary) -> int:
    # Execute the repository
    rows_affected = await repository.update_vocabulary(db, vocabulary_no, vocabulary)
    return rows_affected
