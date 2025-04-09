from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
import json
import os

# 初始化 FastAPI 應用
app = FastAPI()

# 設定 OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"  # 請替換為你的 API Key


# 📌 定義嵌入向量 API
@app.post("/embed_data")
def embed_data():
    """處理 JSON 資料並轉換成嵌入向量"""
    try:
        # ✅ 讀取 JSON 檔案
        with open("web_crawler_1.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        doc_list = []  # 儲存 Document 物件

        # 📌 轉換 JSON -> 文本格式
        for idx, item in enumerate(data):
            text = f"{item['name']} - {item['introduction']}"

            if "nearby" in item and item["nearby"]:
                text += f"，靠近 {', '.join(item['nearby'])}"
            if "address" in item and item["address"]:
                text += f"，地址：{item['address']}"
            if "ticket" in item and item["ticket"]:
                text += f"，門票資訊：{item['ticket']}"
            if "open_hour" in item and item["open_hour"]:
                text += f"，開放時間：{item['open_hour']}"

            # 建立 Document 物件
            doc = Document(
                page_content=text,
                metadata={
                    "id": str(idx),
                    "name": item["name"],
                    "address": item.get("address", ""),
                    "ticket": item.get("ticket", ""),
                    "open_hour": item.get("open_hour", "")
                }
            )
            doc_list.append(doc)

        print(f"✅ 轉換完成，共處理 {len(doc_list)} 筆資料")

        # 📌 切割文本，避免過長
        text_splitter = CharacterTextSplitter(chunk_size=40, chunk_overlap=10)
        split_docs = text_splitter.split_documents(doc_list)

        # 📌 建立嵌入向量
        embeddings = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(split_docs, embeddings, persist_directory="./vector_store_PTT")

        return {"message": "✅ 嵌入向量儲存成功", "total_docs": len(split_docs)}

    except Exception as e:
        return {"error": str(e)}


# ✅ FastAPI 啟動方式
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)