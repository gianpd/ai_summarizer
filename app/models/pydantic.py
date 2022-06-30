import string
from pydantic import BaseModel, AnyUrl

class SummaryPayloadText(BaseModel):
    text: string

class SummaryTextResponseSchema(SummaryPayloadText):
    summary: string

