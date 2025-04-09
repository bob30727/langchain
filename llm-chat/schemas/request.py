from typing import Annotated
from typing import List, Union

from pydantic import BaseModel
from pydantic import Field

from .history import RecentMessages
from .utils import FrozenModel


class PerformanceRequest(BaseModel):
    agent_id: str
    motion_id: str
    performance_id: str
    content: str
    host_by: str
    model: str
    api_key: str
    
    
class ModelSettings(BaseModel):
    api_key: str | None = None
    endpoint: str
    host_by: str
    max_token: int
    embedd_model: str
    openai_api_version: str | None = None
    
    
class ChatParametersRequest(FrozenModel):
    frequency_penalty: float = 1.5
    history_message_limit: int = 5
    score_threshold: float = 0.5
    temperature: float = 0
    top_k_docs: int = 5
    top_k_keywords: int = 5

class ExperimentFeaturesRequest(FrozenModel):
    memory_mode: str
    performance_distance_threshold: Annotated[float, Field(ge=0, le=1, default=0.38)]
    replace_numbers_with_en_template: bool = False
    sentence_split_max_length: Annotated[int, Field(gt=0, default=20)]
    spell_out_numbers: bool = False
    stop_reading_at_url: bool = False


class ModelsRequest(FrozenModel):
    embedding: ModelSettings
    text: ModelSettings


class PromptRequest(FrozenModel):
    default: str | None = None


class ProfileRequest(FrozenModel):
    embedding_id: str | None = None
    description: str = None
    chat_parameters: ChatParametersRequest
    experiment_features: ExperimentFeaturesRequest
    models: ModelsRequest
    name: str | None = None
    prompt: PromptRequest
    

class RetrievalQARequest(FrozenModel):
    message: str
    recent_messages: list[str] | None = None
    history: RecentMessages | None = None
    profile: ProfileRequest
    
