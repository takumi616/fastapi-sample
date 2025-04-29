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

async def select_vocabulary_by_id(db, vocabulary_no) -> Vocabulary | None:
    stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql",
        sql="SELECT * FROM vocabularies where vocabulary_no=:vocabulary_no;",
        params={
            "vocabulary_no": vocabulary_no
        }
    )
    result = await db.query_typed(stmt=stmt)
    row = result.get_first()

    if row is None:
        return None  
    return Vocabulary(**row)

async def update_vocabulary(db, vocabulary_no: int, vocabulary: Vocabulary) -> int:
    stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql",
        sql="UPDATE vocabularies SET title=:title, meaning=:meaning, sentence=:sentence WHERE vocabulary_no=:vocabulary_no;",
        params={
            "title": vocabulary.title,
            "meaning": vocabulary.meaning,
            "sentence": vocabulary.sentence,
            "vocabulary_no": vocabulary_no
        }
    )
    return await db.execute(stmt=stmt)
    
