# 選擇基底映像
FROM ubuntu:20.04

# 設定環境變數以防止互動式安裝卡住
ENV DEBIAN_FRONTEND=noninteractive

# 更新套件並安裝必要工具
RUN apt update && apt install -y \
    curl \
    ca-certificates \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# 開放必要的伺服器埠
EXPOSE 11434

