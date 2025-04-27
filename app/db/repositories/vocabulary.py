import pysqlx_core
from app.entities.vocabulary import Vocabulary

async def insert_vocabulary(db, vocabulary: Vocabulary) -> int:
    stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql",
        sql="INSERT INTO vocabularies (title, meaning, sentence) VALUES (:title, :meaning, :sentence);",
        params={
            "title": vocabulary.title,
            "meaning": vocabulary.meaning,
            "sentence": vocabulary.sentence
        }
    )
    return await db.execute(stmt=stmt)

async def select_all_vocabularies(db) -> list[Vocabulary]:
    stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql",
        sql="SELECT * FROM vocabularies;"
    )
    result = await db.query_typed(stmt=stmt)
    rows = result.get_all()

    vocabularies = [Vocabulary(**row) for row in rows]
    return vocabularies
    
