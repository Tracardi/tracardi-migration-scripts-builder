from pydantic import BaseModel
from typing import Optional


class IndexName(BaseModel):
    index: str


class PainlessScript(BaseModel):
    source: Optional[str] = None
    lang: Optional[str] = "painless"


class EndpointBody(BaseModel):
    source: IndexName
    dest: IndexName
    script: PainlessScript


class ReindexEndpoint(BaseModel):
    method: Optional[str] = "POST"
    body: EndpointBody
