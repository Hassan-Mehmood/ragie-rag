from fastapi import FastAPI
from dotenv import load_dotenv

from src.routes.ragie_router import ragie_router

load_dotenv()

app = FastAPI(
    title="Raggie API", description="A basic FastAPI application", version="0.1.0"
)


@app.get("/")
async def root():
    return {"Hello": "World"}


app.include_router(ragie_router)
