from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from pydantic import BaseModel
import pysqlx_core
import os

class VocabularyCreateRequest(BaseModel):
    title: str
    meaning: str
    sentence: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure DATABASE_URL is present
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set.")

    # Create a connection 
    pool = await pysqlx_core.new(uri=database_url)

    # Create a table
    stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql", 
        sql="""
            CREATE TABLE IF NOT EXISTS vocabularies (
                vocabulary_no SERIAL PRIMARY KEY,
                title VARCHAR(20) NOT NULL,
                meaning TEXT NOT NULL,
                sentence TEXT NOT NULL
            );
        """)
    await pool.execute(stmt=stmt)

    app.state.db_pool = pool

    yield

    # Close the connection
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

@app.post("/vocabularies", response_model=dict)
async def create_vocabulary(request: Request, body: VocabularyCreateRequest) -> dict:
    db = request.app.state.db_pool

    # Insert a row and return quantity rows affected
    insert_stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql", 
        sql="INSERT INTO vocabularies (title, meaning, sentence) VALUES (:title, :meaning, :sentence);",
        params=body.model_dump()
    )
    try:
        affected = await db.execute(stmt=insert_stmt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert vocabulary: {str(e)}")
    
    return {"affected": affected}

@app.get("/vocabularies", response_model=dict)
async def fetch_all_vocabularies(request: Request) -> dict:
    db = request.app.state.db_pool

    select_stmt = pysqlx_core.PySQLxStatement(
        provider="postgresql",
        sql="SELECT * FROM vocabularies;"
    )

    try:
        result = await db.query_typed(stmt=select_stmt)
        rows = result.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch vocabularies: {str(e)}")

    return {"vocab": rows}

# @app.get("/vocabularies/{vocab_id}")
# async def fetch_vocabulary_by_id(vocab_id: int):
#     return {"vocab_id": vocab_id}