import json
import logging
from collections.abc import Iterable

from fastapi import APIRouter
from fastapi import status
from langchain_core.messages import BaseMessage

from nlp import split_messages_into_sentences
from schemas import ChatResponse
from schemas import ProfileRequest
from schemas import RetrievalQARequest
from schemas import SSEvent

from .utils import create_stream_event
from .utils import initialize_agent
from .utils import sse_resp
from .utils import SPELL_OUT_NUMBER_PATTERN


router = APIRouter()
logger = logging.getLogger("uvicorn.error")


@router.post("", status_code=status.HTTP_201_CREATED, tags=["Chat"])
def api_retrieval_qa(body: RetrievalQARequest):
    message = body.message
    recent_messages = body.recent_messages
    history = body.history
    profile = body.profile

    agent = initialize_agent(profile)
    message_stream = agent.stream(
        msg=message, recent_messages=recent_messages, history=history
    )
    return sse_resp(lambda: generate_stream_events(message_stream, message, profile))


def generate_stream_events(
    message_stream: Iterable[BaseMessage | str], question: str, profile: ProfileRequest
):
    try:
        answer = ""
        chat_resp_factory = ChatResponseFactory()
        for sentence in split_messages_into_sentences(
            message_stream, profile.experiment_features.sentence_split_max_length
        ):
            resp = chat_resp_factory.create(sentence, profile)
            answer += resp.message
            yield create_stream_event(
                event=SSEvent.chat, data=json.dumps(resp.model_dump(mode="json"))
            )

        yield create_stream_event(
            event=SSEvent.end,
            data=json.dumps(ChatResponse(message="[END]", ssml="").model_dump(mode="json"),)
        )

        logger.info(f"Adding message to conversation: {question=}, {answer=}")

    except Exception as e:
        logger.error(f"Encountered an error: {e}")
        yield create_stream_event(event=SSEvent.error, data=json.dumps({"error": str(e)}))


class ChatResponseFactory:
    def create(self, sentence: str, profile: ProfileRequest) -> ChatResponse:
        if profile.experiment_features.spell_out_numbers:
            sentence = SPELL_OUT_NUMBER_PATTERN.sub(lambda m: m.group(1), sentence)
        return ChatResponse(message=sentence, ssml="")
