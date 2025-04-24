from fastapi import FastAPI, File, UploadFile
from typing import Annotated
import json

import requests

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Raggie API", description="A basic FastAPI application", version="0.1.0"
)


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/create-document")
async def create_document(document: UploadFile = File(...)):
    base_url = os.getenv("RAGIE_BASE_URL")
    api_key = os.getenv("RAGIE_API_KEY")

    headers = {
        "accept": "application/json",
        # "content-type": "multipart/form-data",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "mode": "fast",
        "external_id": "1",
        "name": "Hassan Mehmood Resume",
        "metadata": json.dumps({"name": "Hassan Mehmood", "file": "Resume"}),
    }

    file_bytes = await document.read()
    files = {"file": (document.filename, file_bytes, document.content_type)}

    try:
        url = f"{base_url}/documents"
        response = requests.post(url, headers=headers, data=data, files=files)

        print("response", response)

        response_json = response.json()
        print(response_json)

        return response_json
    except Exception as e:
        return {"error": str(e)}


@app.get("/get-document")
async def get_document():
    return {"message": "Document retrieved"}
