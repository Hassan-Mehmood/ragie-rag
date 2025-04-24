from fastapi import FastAPI


app = FastAPI(
    title="Raggie API", description="A basic FastAPI application", version="0.1.0"
)


@app.get("/")
async def root():
    return {"message": "Welcome to Raggie API! Go to /docs for the API documentation."}
