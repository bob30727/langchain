import requests
from bs4 import BeautifulSoup
import json
import re

# 設定 PTT 18+ Cookie
cookies = {'over18': '1'}
url = "https://www.ptt.cc/bbs/Taoyuan/M.1706183855.A.F44.html"
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.1"

def get_llm_response(post_data: str) -> str:
    messages = [
        {"role": "system", "content": "你是一個協助結構化的工具"},
        {"role": "user", "content": f"""
請將以下文章內容轉換為結構化 JSON 格式：
---
{post_data}
---
輸出格式如下：
[
  {{
    "name": "地點名稱",
    "introduction": "簡介",
    "nearby": ["附近地點1", "附近地點2"],
    "address": "地址",
    "ticket": "門票資訊",
    "open_hour": "開放時間"
  }}
]
"""}
    ]

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": MODEL_NAME, "messages": messages, "temperature": 0},
            timeout=10,
            stream=True
        )

        response.raise_for_status()  # 若 API 回應錯誤，拋出例外
        response_text = ""
        for line in response.iter_lines(decode_unicode=True):
            if line.strip():  # 確保每行有內容
                try:
                    data = json.loads(line)  # 解析單行 JSON
                    message_content = data.get("message", {}).get("content", "")
                    if message_content:
                        response_text += message_content  # 合併內容
                except json.JSONDecodeError as e:
                    print(f"JSON 解析錯誤: {e}")

        return response_text.strip()

    except requests.exceptions.RequestException as e:
        print(f"API 請求失敗: {e}")
        return ""

def clean_content(text: str) -> str:
    """移除 PTT 文章內的系統訊息與簽名檔"""
    text = text.split("※ 發信站:")[0]  # 移除系統訊息
    text = re.sub(r"(\[.*?\])", "", text)  # 移除 [推/噓文] 等標籤
    return text.strip()

# 爬取 PTT 內容
response = requests.get(url, cookies=cookies)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one("title").text.strip()
    main_content = clean_content(soup.select_one("#main-content").text)

    comments = [push.select_one(".push-content").text.strip(": ") for push in soup.select(".push")]

    # 組合 JSON 格式
    post_data = json.dumps({"title": title, "content": main_content, "comments": comments}, ensure_ascii=False, indent=2)

    response_text = get_llm_response(post_data)

    match = re.search(r"\[\s*{.*}\s*\]", response_text, re.DOTALL)

    try:
        json_content = match.group(0)  # 取得匹配的 JSON 內容
        json_content = json.loads(json_content)
        with open("web_crawler_1.json", "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=2)
        print("JSON 已成功儲存為 web_crawler_1.json")
    except json.JSONDecodeError:
        print("JSON 解析失敗")
else:
    print("無法獲取頁面，狀態碼:", response.status_code)
