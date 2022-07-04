from pydantic import BaseModel, AnyHttpUrl

class SummaryPayloadText(BaseModel):
    text: str

class SummaryTextResponseSchema(SummaryPayloadText):
    extractive_summary: str
    abstractive_summary: str

class SummaryPayloadURL(BaseModel):
    url: AnyHttpUrl

class SummaryURLResponseSchema(SummaryPayloadURL):
    extractive_summary: str
    abstractive_summary: str

