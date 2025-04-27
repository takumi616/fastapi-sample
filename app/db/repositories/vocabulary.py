import pysqlx_core

from app.models.vocabulary import VocabularyCreateRequest

async def insert_vocabulary(db, vocabulary: VocabularyCreateRequest) -> int:
    stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql",
        sql="INSERT INTO vocabularies (title, meaning, sentence) VALUES (:title, :meaning, :sentence);",
        params=vocabulary.model_dump()
    )
    return await db.execute(stmt=stmt)

async def select_all_vocabularies(db) -> list:
    stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql",
        sql="SELECT * FROM vocabularies;"
    )
    result = await db.query_typed(stmt=stmt)
    return result.get_all()
