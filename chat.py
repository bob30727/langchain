import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaLLM

# 加載環境變數
load_dotenv()

# 環境變數設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
VECTOR_STORE_PATH = "./vector_store_PTT"

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY 未設定，請檢查 .env 檔案")

# 初始化 FastAPI 應用程式
app = FastAPI(title="QA Chatbot API", version="1.0")

# 初始化 LLM
ollama = OllamaLLM(
    base_url=OLLAMA_BASE_URL,
    model=OLLAMA_MODEL,
    temperature=0.1,
    repeat_penalty=1.5,
)

# 初始化嵌入模型
embeddings = OpenAIEmbeddings()

# 初始化向量資料庫
docsearch = Chroma(
    persist_directory=VECTOR_STORE_PATH,
    embedding_function=embeddings,
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Prompt 設定
prompt_template_llama3 = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        "你是一名客服人員，根據以下文章回答問題，回答請簡明扼要，不超過50字，並使用繁體中文。\n"
        "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        "{context}，根據上面的文章\n 問題是: {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    ),
)

qa = RetrievalQA.from_chain_type(
    llm=ollama,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template_llama3},
)

# 定義請求格式
class QuestionRequest(BaseModel):
    question: str

# API 端點: 問答
@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        response = qa.invoke({"query": request.question})
        return {"answer": response["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 啟動測試
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)