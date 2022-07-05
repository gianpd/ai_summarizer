import sys
import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")

from fastapi import APIRouter

from pipelines.extractive_summary import get_lsa_extractive_summary
from pipelines.abstractive_summary import get_summaries_from_hf_api

from models.pydantic import SummaryPayloadText, SummaryTextResponseSchema, SummaryPayloadURL, SummaryURLResponseSchema

router = APIRouter()

@router.post("/summary_text", response_model=SummaryTextResponseSchema, status_code=201)
async def create_summary_from_text(payload: SummaryPayloadText) -> SummaryTextResponseSchema:
    """POST method receiving a text to be summarized"""
    text = payload.text
    logger.info(f"Received text: {text}")
    extractive_summary = get_lsa_extractive_summary(text, url=False)
    logger.info(f"EXCTRACTIVE SUMMARY: {extractive_summary}")
    abstractive_summary = get_summaries_from_hf_api(extractive_summary)
    logger.info(f"ABSTRACTIVE SUMMARY: {abstractive_summary}")
    return {"text": text, "extractive_summary": extractive_summary, "abstractive_summary": abstractive_summary}

@router.post("/summary_url", response_model=SummaryURLResponseSchema, status_code=201)
async def create_summary_from_text(payload: SummaryPayloadURL) -> SummaryURLResponseSchema:
    """POST method receiving an URL to be parsed and summarized"""
    str_url = payload.url
    logger.info(f"Received url: {str_url}")
    extractive_summary = get_lsa_extractive_summary(str_url, url=True)
    logger.info(f"EXCTRACTIVE SUMMARY: {extractive_summary}")
    abstractive_summary = get_summaries_from_hf_api(extractive_summary)
    logger.info(f"ABSTRACTIVE SUMMARY: {abstractive_summary}")
    return {"url": str_url, "extractive_summary": extractive_summary, "abstractive_summary": abstractive_summary}