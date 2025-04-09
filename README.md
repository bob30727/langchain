# Building a LangChain Chat AI Agent Using Web Scraped Data


## Installation Guide

Follow these steps to install and set up the project:

1. **Clone the project repository:**

   ```bash
   git clone git@github.com:bob30727/langchain.git

2. use vs code to build docker container
   ![image](https://github.com/user-attachments/assets/868c2008-9ae7-4ecd-a44d-f6b96c94c786)
   


4. get json from wed:

    run web_crawler_to_json.py 
then you will get 
web_crawler_1.json
```bash
[
  {
    "name": "桃園月眉人工濕地生態公園",
    "introduction": "如天空之鏡般的漸層落羽松絕美倒影，湖邊375棵落羽松林變幻萬千的色彩、夢幻湖畔風光彷彿置身小歐洲～近年新興秘境！",
    "nearby": [
      "大溪老街",
      "慈湖"
    ],
    "address": "桃園市大溪區月湖路200號",
    "ticket": "免費",
    "open_hour": "24小時"
  },
  {
    "name": "桃園大溪河濱公園",
    "introduction": "冬日裡的金色仙境就屬桃園大溪河濱公園啦！沒想到河濱公園也有一片落羽松美景，藍天白雲下一棵棵落羽松顯出迷人景緻～",
    "nearby": [
      ""
    ],
    "address": "",
    "ticket": "",
    "open_hour": ""
  },
  {
    "name": "桃園霄裡大池落羽松",
    "introduction": "距離僅800公尺，也是熱門免費桃園落羽松景點，可以直接散步過去安排順遊，堤岸邊整排高大落羽松漸層色彩非常迷人，配上湖景相互輝映，詩情畫意好不浪漫～",
    "nearby": [
      "霄裡大池"
    ],
    "address": "桃園市八德區龍南路洪圳路交叉口",
    "ticket": "免費",
    "open_hour": ""
  },
  {
    "name": "桃園楊梅落羽松秘境",
    "introduction": "藏身於桃園鄉間的落羽松林，位處非常偏僻所以人也比較少，且這裡的落羽松種植很整齊，距離也比較近，也因此更好拍照～",
    "nearby": [],
    "address": "桃園市楊梅區高新街底",
    "ticket": "",
    "open_hour": ""
  },
  {
    "name": "桃園霄裡大池落羽松",
    "introduction": "距離僅800公尺，也是熱門免費桃園落羽松景點，可以直接散步過去安排順遊，堤岸邊整排高大落羽松漸層色彩非常迷人，配上湖景相互輝映，詩情畫意好不浪漫～",
    "nearby": [
      "霄裡大池"
    ],
    "address": "",
    "ticket": "免費",
    "open_hour": ""
  },
  {
    "name": "桃園八德落羽松秘境",
    "introduction": "種滿3000棵落羽松壯觀又夢幻，同時也是免費桃園落羽松IG打卡熱點，現更名南興落羽松～",
    "nearby": [
      "霄裡大池"
    ],
    "address": "桃園市八德區浮筧街158之1號",
    "ticket": "免費",
    "open_hour": ""
  }
]
```

3. Build Docker image
```bash
    cd back_end_motion_stylization
    docker build -t mcm-ldm-backend -f ./dockerfile_server ./ --no-cache
```
4. Run service


Windows (CMD 命令提示字元)
```bash
docker run -it --name mcm-ldm-backend-container --gpus all ^
  -e NVIDIA_VISIBLE_DEVICES=all -p 8765:8765 ^
  -v %cd%\..\front_end_speech_motion_aligner\speech_motion_align\Assets\Animations\fbx:/exports ^
  -v %cd%\lib_third\MCM-LDM\deps:/workspaces/lib_third/MCM-LDM/deps ^
  -v %cd%\lib_third\MCM-LDM\datasets\humanml3d:/workspaces/lib_third/MCM-LDM/datasets/humanml3d ^
  -v %cd%\lib_third\MCM-LDM\checkpoints:/workspaces/lib_third/MCM-LDM/checkpoints ^
  mcm-ldm-backend

```
Windows (PowerShell)
```
docker run -it --name mcm-ldm-backend-container --gpus all `
  -e NVIDIA_VISIBLE_DEVICES=all -p 8765:8765 `
  -v ${PWD}\..\front_end_speech_motion_aligner\speech_motion_align\Assets\Animations\fbx:/exports `
  -v ${PWD}\lib_third\MCM-LDM\deps:/workspaces/lib_third/MCM-LDM/deps `
  -v ${PWD}\lib_third\MCM-LDM\datasets\humanml3d:/workspaces/lib_third/MCM-LDM/datasets/humanml3d `
  -v ${PWD}\lib_third\MCM-LDM\checkpoints:/workspaces/lib_third/MCM-LDM/checkpoints `
  mcm-ldm-backend
```

Linux / macOS (bash, zsh)
```
docker run -it --name mcm-ldm-backend-container --gpus all \
  -e NVIDIA_VISIBLE_DEVICES=all -p 8765:8765 \
  -v $(realpath ../front_end_speech_motion_aligner/speech_motion_align/Assets/Animations/fbx):/exports \
  -v $(realpath ./lib_third/MCM-LDM/deps):/workspaces/lib_third/MCM-LDM/deps \
  -v $(realpath ./lib_third/MCM-LDM/datasets/humanml3d):/workspaces/lib_third/MCM-LDM/datasets/humanml3d \
  -v $(realpath ./lib_third/MCM-LDM/checkpoints):/workspaces/lib_third/MCM-LDM/checkpoints \
  mcm-ldm-backend

```
5. 
Download pretrained weight from
[google drive](https://drive.google.com/uc?id=1vNsNnvGHw8p7cY2RD5lLtE-MgDNNS52b) and unzip to the path "./lib_third/MCM-LDM/checkpoints"

Download dependency model from 
[google drive](https://drive.google.com/uc?id=152jnHIKZk0wInfWvz95jeeVaWqoHHd4Z) and unzip to the path "./lib_third/MCM-LDM/deps"

Download Humanml3D dataset from
[google drive](https://drive.google.com/uc?id=180urHIMUNioZOPD_MP4viT6k7E4M45K4) and unzip to the path "./lib_third/MCM-LDM/datasets/humanml3d"
