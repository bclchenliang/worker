FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

LABEL author="biancl"

# cuda env path
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
ENV PATH=$PATH:/usr/local/cuda/bin
ENV CUDA_HOME=/usr/local/cuda

# python and vim
RUN apt-get update && \
    apt-get install -y --no-install-recommends vim \
    python3-dev \
    python3-pip &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# chatglm requirements
RUN pip3 install  --no-cache-dir --upgrade pip && \
    pip3 install  --no-cache-dir torch==2.0.1+cu117 \
    --index-url https://download.pytorch.org/whl/cu117 &&\
    pip3 install  --no-cache-dir  transformers==4.33.2 datasets>=2.12.0 \
    accelerate>=0.21.0 peft>=0.4.0 trl>=0.7.1 scipy sentencepiece protobuf \
    tiktoken fire jieba rouge-chinese nltk gradio==3.38.0 uvicorn pydantic==1.10.11 \
    fastapi==0.95.1 sse-starlette matplotlib minio pillow deepspeed bitsandbytes==0.39.0 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple
