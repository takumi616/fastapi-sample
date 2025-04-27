from fastapi import FastAPI
from app.db.connection import lifespan
from app.routers import vocabulary
from app.common.exception_handler import internal_server_error_handler

app = FastAPI(lifespan=lifespan)

app.include_router(vocabulary.router)

app.add_exception_handler(Exception, internal_server_error_handler)