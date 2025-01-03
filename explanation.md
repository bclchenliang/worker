### step1: 
## 1.1 拉取镜像，docker pull pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel
## 1.2 如果失败，更换国内源。 vi /etc/docker/daemon.json, 增加 "registry-mirrors": ["http://hub-mirror.c.163.com","https://docker.mirrors.ustc.edu.cn","https://registry.docker-cn.com"]

### step2: 启动镜像，进入容器，增加包
## 1.1 docker run -it --gpus all --shm-size 64g   -p 4010:4006 -v /data/biancl/llm_models/ChatGLM-Finetuning/:/worker  pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel /bin/bash
## 1.2 cd /worker/
## 1.3 pip install minio==7.1.16 datasets==2.14.5 transformers==4.33.1 deepspeed==0.10.3 peft==0.5.0 sentencepiece==0.1.99 tensorboard==2.14.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
## 1.4 测试训练脚本，sh train_lora.sh
## 1.5 容器保存为镜像，docker commit [容器id] [镜像名:版本号]，查看容器id: docker ps
     