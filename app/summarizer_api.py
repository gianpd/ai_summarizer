import sys
import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.summarizer_pipeline import get_summaries_from_hf
from app.models.pydantic import SummaryPayloadText, SummaryTextResponseSchema

app = FastAPI()
origins = [
    'http://localhost:3000' # testing the frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mangum(app) # handler for lambda function 

@app.post("/summary", response_model=SummaryTextResponseSchema, status_code=201)
async def create_summary_from_text(payload: SummaryPayloadText) -> SummaryTextResponseSchema:
    """POST method for receiving the text to be summarized"""
    text = payload.text
    logger.info(f"Received text: {text}")
    summary = get_summaries_from_hf(text)
    return {"text": text, "summary": summary}