import string
from pydantic import BaseModel

class SummaryPayloadText(BaseModel):
    text: str

class SummaryTextResponseSchema(SummaryPayloadText):
    summary: str

