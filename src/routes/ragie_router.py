from fastapi import APIRouter, UploadFile, File
import os
import requests

from src.components.llm import LLM

ragie_router = APIRouter(prefix="/rag")


@ragie_router.post("/create-document")
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
        # "external_id": "1",
        "name": document.filename,
        # "metadata": json.dumps({"name": "Hassan Mehmood", "file": "Resume"}),
    }

    file_bytes = await document.read()
    files = {"file": (document.filename, file_bytes, document.content_type)}

    try:
        url = f"{base_url}/documents"
        response = requests.post(url, headers=headers, data=data, files=files)

        if response.status_code == 201:
            response_json = response.json()

            print(response_json)

            return response_json

        else:
            raise Exception("Failed to create document")

    except Exception as e:
        return {"error": str(e)}


@ragie_router.post("/retrieve")
async def retrieve(query: str):
    base_url = os.getenv("RAGIE_BASE_URL")
    api_key = os.getenv("RAGIE_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    payload = {"query": "What is The Op-Amp Differentiator", "top_k": 3}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}",
    }

    try:
        url = f"{base_url}/retrievals"

        response = requests.post(url, headers=headers, json=payload)

        print("Status code", response.status_code)
        if response.status_code == 200:
            response = response.text

            llm = LLM()

            llm_response = llm.generate_response(query, response)

            print(llm_response.output_text)

            return llm_response.output_text

        else:
            raise Exception("Failed to retrieve")

    except Exception as e:
        print(e)
        return {"error": str(e)}
