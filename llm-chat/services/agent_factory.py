import abc
from collections.abc import Iterable

from langchain_core.language_models.llms import BaseLLM
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePick
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain_postgres import PGVector
from jieba.analyse import extract_tags

from nlp import LLMFactory
from schemas import AIAgentModelHost
from schemas import RecentMessages
from schemas import MemoryMode
from schemas import ProfileRequest
from database import connection

from .constants import ASSISTANT
from .constants import FREQUENCY_PENALTY
from .constants import SCORE_THRESHOLD
from .constants import SYSTEM
from .constants import TOP_K
from .constants import USER


class AgentFactory:
    @staticmethod
    def create_agent(profile: ProfileRequest):
        models = profile.models

        if (chat_setting := models.text) is None:
            raise ValueError("Text model not set in profile.")
        chat_model = LLMFactory.get_chat_model(chat_setting)

        if (embedding_model_setting := models.embedding) is None:
            raise ValueError("Embedding model not set in profile")
        embedding_model = LLMFactory.get_embedding_model(embedding_model_setting)

        if chat_setting.host_by == AIAgentModelHost.OLLAMA:
            return LLAMA3Agent(
                profile=profile,
                chat_model=chat_model,
                embedding_model=embedding_model,
                embedding_collection=profile.embedding_id,
                memory_mode=profile.experiment_features.memory_mode,
            )

        return OpenAIAgent(
            profile=profile,
            chat_model=chat_model,
            embedding_model=embedding_model,
            embedding_collection=profile.embedding_id,
            memory_mode=profile.experiment_features.memory_mode,
        )


class AgentBase(abc.ABC):
    def __init__(
        self,
        profile: ProfileRequest,
        chat_model: ChatOpenAI,
        embedding_model: OpenAIEmbeddings,
        embedding_collection: str,
        memory_mode: MemoryMode,
    ):
        self._profile = profile

        self._chat_model = chat_model
        self._embedding_model = embedding_model

        self._retriever = PGVector(
            embeddings=self._embedding_model,
            collection_name=embedding_collection,
            connection=connection,
        ).as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                SCORE_THRESHOLD: self._profile.chat_parameters.score_threshold,
                TOP_K: self._profile.chat_parameters.top_k_docs,
            },
        )

        self._memory_mode = memory_mode

    @staticmethod
    def get_feature_prompts(profile: ProfileRequest):
        phone_number_instructions = (
            "When you mention a phone number in your responses, always wrap it in the format $^phone_number^$. "
            "For example, if you need to tell someone to call the police, "
            'you should say "Please call the police $^110^$". '
            'Do not use the placeholder text "$^phone_number^$"; '
            "instead, replace it with an actual phone number wrapped in the format $^number^$. "
        )
        system_prompts = []
        if profile.experiment_features.spell_out_numbers:
            system_prompts.append(phone_number_instructions)

        return system_prompts

    @abc.abstractmethod
    def get_prompt_and_query(self, *args, **kargs) -> tuple[ChatPromptTemplate | PromptTemplate, str]:
        pass

    def stream(
        self, 
        msg: str, 
        recent_messages: list[str], 
        history: RecentMessages
    ) -> Iterable[BaseMessage | str]:
        
        prompt, query = self.get_prompt_and_query(
            recent_messages,
            history,
            self._profile.chat_parameters.top_k_keywords, 
            msg
        )

        chain = (
            {"docs": RunnablePick("query") | self._retriever, "question": RunnablePick("question")}
            | prompt
            | self._chat_model
        )

        chain_input = {"question": msg, "query": query}

        return chain.stream(chain_input)


class OpenAIAgent(AgentBase):
    def __init__(
        self,
        profile: ProfileRequest,
        chat_model: ChatOpenAI,
        embedding_model: OpenAIEmbeddings,
        embedding_collection: str,
        memory_mode: MemoryMode,
    ):
        super().__init__(profile, chat_model, embedding_model, embedding_collection, memory_mode)
        self._chat_model.model_kwargs[FREQUENCY_PENALTY] = self._profile.chat_parameters.frequency_penalty
        self._chat_model.temperature = self._profile.chat_parameters.temperature

    def get_prompt_and_query(
        self, 
        recent_messages: list[str], 
        history: RecentMessages, 
        top_k_keywords: int, 
        msg: str
    ) -> tuple[ChatPromptTemplate, str]:
        user_message_template = (USER, "{question}")
        system_prompts = self.get_feature_prompts(self._profile)
        system_prompt = self._profile.prompt.default
        if system_prompt is None:
            raise KeyError("Default prompt not set in profile.")

        system_prompts.append(system_prompt)
        match self._memory_mode:
            case MemoryMode.KEYWORD:
                prompt = ChatPromptTemplate.from_messages(
                    [
                        *[(SYSTEM, sp) for sp in system_prompts],
                        user_message_template,
                    ]
                )

                keywords = extract_tags(sentence=recent_messages, topK=top_k_keywords)

                query = ",".join(keywords + [msg])
                return prompt, query

            case MemoryMode.HISTORY:
                history_prompts = [p for m in reversed(history.root) for p in [(USER, m.question), (ASSISTANT, m.answer)] if p[1]]
                prompt = ChatPromptTemplate.from_messages(
                    [
                        *[(SYSTEM, sp) for sp in system_prompts],
                        *history_prompts,
                        user_message_template,
                    ]
                )
                query = msg

                return prompt, query

            case MemoryMode.DISABLED:
                query = msg
                prompt = ChatPromptTemplate.from_messages(
                    [
                        *[(SYSTEM, sp) for sp in system_prompts],
                        user_message_template,
                    ]
                )

                return prompt, query

            case _:
                raise ValueError("Invalid memory mode")


class LLAMA3Agent(AgentBase):
    def __init__(
        self,
        profile: ProfileRequest,
        chat_model: BaseLLM,
        embedding_model: OpenAIEmbeddings,
        embedding_collection: str,
        memory_mode: MemoryMode,
    ):
        super().__init__(profile, chat_model, embedding_model, embedding_collection, memory_mode)
        self._chat_model.repeat_penalty = self._profile.chat_parameters.frequency_penalty
        self._chat_model.temperature = self._profile.chat_parameters.temperature

    def get_prompt_and_query(
        self,
        recent_messages: list[str], 
        history: RecentMessages,  
        top_k_keywords: int, 
        msg: str
    ) -> tuple[PromptTemplate, str]:
        system_prompt = self._profile.prompt.default
        if system_prompt is None:
            raise KeyError("Default prompt not set in profile.")

        match self._memory_mode:
            case MemoryMode.KEYWORD:
                prompt = PromptTemplate(input_variables=["docs", "question"], template=system_prompt)
                keywords = extract_tags(sentence=recent_messages, topK=top_k_keywords)
                query = ",".join(keywords + [msg])
                return prompt, query

            case MemoryMode.HISTORY:
                history.root.reverse()

                history_prompts = "\n".join(
                    [
                        p
                        for m in history.root
                        for p in [
                            f"<|start_header_id|>{USER}<|end_header_id|>\n{m.question}\n<|eot_id|>",
                            f"<|start_header_id|>{ASSISTANT}<|end_header_id|>\n{m.answer}\n<|eot_id|>",
                        ]
                    ]
                )

                template = system_prompt.replace(r"{history}", history_prompts)
                prompt = PromptTemplate(input_variables=["docs", "question"], template=template)
                return prompt, msg

            case MemoryMode.DISABLED:
                prompt = PromptTemplate(input_variables=["docs", "question"], template=system_prompt)
                return prompt, msg

            case _:
                raise ValueError("Invalid memory mode")
