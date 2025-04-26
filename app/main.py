from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/vocabularies/{vocab_id}")
async def fetch_vocabulary_by_id(vocab_id: int):
    return {"vocab_id": vocab_id}