from database import get_vector_store
from langchain_core.documents import Document
from sqlalchemy import and_
from sqlalchemy.orm import Session

from models import LangchainPgEmbedding
from nlp import LLMFactory
from schemas import AIAgentModelSetting


class EmbeddingService:
    @staticmethod
    def insert_pgvector_embedding(
        content: str,
        metadata: dict,
        collection_name: str,
        embedding_setting,
    ):
        docs = [
            Document(
                page_content=content,
                metadata=metadata,
            )
        ]
        
        embeddings = LLMFactory.get_embedding_model(embedding_setting)
        vector_store = get_vector_store(collection_name, embeddings)
        vector_store.add_documents(docs)
        
    @staticmethod
    def get_langchain_pg_embedding_by_metadata(metadata_params: dict, db: Session):
        filters = [LangchainPgEmbedding.cmetadata[field].astext == value for field, value in metadata_params.items()]
        return db.query(LangchainPgEmbedding).filter(and_(*filters))
    
    @staticmethod
    def get_langchain_pg_embedding_by_metadata_all(metadata_params: dict, db: Session):
        return EmbeddingService.get_langchain_pg_embedding_by_metadata(metadata_params, db).all()

    @staticmethod
    def get_langchain_pg_embedding_by_metadata_first(metadata_params: dict, db: Session):
        return EmbeddingService.get_langchain_pg_embedding_by_metadata(metadata_params, db).first()
    
    @staticmethod
    def similarity_search_results(agent_id: str, collection_name: str, embedding_setting: AIAgentModelSetting, query: str, k: int = 1):
        embeddings = LLMFactory.get_embedding_model(embedding_setting)

        vector_store = get_vector_store(collection_name, embeddings)
        return vector_store.similarity_search_with_score(query=query, k=k, filter={"agent_id": {"$eq": agent_id}})