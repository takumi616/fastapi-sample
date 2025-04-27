from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import pysqlx_core

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
    



