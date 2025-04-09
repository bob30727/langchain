from enum import StrEnum
from enum import auto
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import RootModel
from uuid import UUID

from .utils import FrozenModel


class PerformanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)
    
    agent_id: str
    motion_id: str
    performance_id: str
    content: str
    
    
class LangchainPgEmbeddingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)
    
    id: str
    collection_id: UUID
    document: str
    cmetadata: dict
    
class LangchainPgEmbeddingResponseList(RootModel):
    root: list[LangchainPgEmbeddingResponse]

class DocumentsPgEmbeddingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)
    
    page_content: str
    metadata: dict
    
class DocumentsPgEmbeddingResponseList(RootModel):
    root: list[DocumentsPgEmbeddingResponse]
    
    
class PerformanceMotionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    motion_id: str | None
    

class SSEvent(StrEnum):
    chat = auto()
    end = auto()
    error = auto()
    
    
class ChatResponse(FrozenModel):
    message: str
    ssml: str
