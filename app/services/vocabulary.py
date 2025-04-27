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
