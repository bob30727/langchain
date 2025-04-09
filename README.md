# Building a LangChain Chat AI Agent Using Web Scraped Data


## Beckend

This project focuses on stylizing motions.


## Installation Guide

Follow these steps to install and set up the project:

1. **Clone the project repository:**

   ```bash
   git clone git@github.com:XRSPACE-Inc/tp-five-pm-stylized-motion-creation.git

2. Pre-requisites:

    Before using this project, download and install the FBX SDK:

    * Download the FBX SDK for Linux: 
    
        [Click here to download](https://damassets.autodesk.net/content/dam/autodesk/www/files/fbx202037_fbxsdk_gcc_linux.tar.gz)

    * Download the FBX Python SDK: 
    
        [Click here to download](https://damassets.autodesk.net/content/dam/autodesk/www/files/fbx202037_fbxpythonsdk_linux.tar.gz)

    * Move the downloaded files to the specified directory: 
    
        Place both files into the directory ./back_end_motion_stylization/lib_third/fbxsdk/

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
