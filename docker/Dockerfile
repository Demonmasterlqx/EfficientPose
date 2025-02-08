FROM ubuntu:22.04

# 所有启动bash替换sh
SHELL ["/bin/bash", "-c"]
# 设shell置环境
ENV SHELL=/bin/bash

# # 为apt换源
RUN cp /etc/apt/sources.list /etc/apt/sources.list.cp \
    && rm /etc/apt/sources.list
# 换用清华源 并且更新证书
COPY ./sources.list /etc/apt/
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

# 设置时区（避免交互式设置）
ENV DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Shanghai
RUN apt-get update && apt-get install -y tzdata && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装基础软件 python3 nano
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y nano \
    python3 python3-pip \
    git

# 设置 Python3 为默认 Python 版本
RUN ln -s /usr/bin/python3 /usr/bin/python

# 确保 pip 最新
RUN pip3 install --no-cache-dir --upgrade pip

WORKDIR /root

# 复制所需文件并且安装 Anconda3
COPY Anaconda3-2024.10-1-Linux-x86_64.sh .

RUN chmod 777 Anaconda3-2024.10-1-Linux-x86_64.sh \
    && printf "\nq\nyes\n\nyes\n" | ./Anaconda3-2024.10-1-Linux-x86_64.sh \
    && rm Anaconda3-2024.10-1-Linux-x86_64.sh 

ENV PATH="/root/anaconda3/bin:$PATH"

# 拉取EfficientPose 并且安装 EfficientPose 和python依赖
RUN git clone https://github.com/Demonmasterlqx/EfficientPose.git

WORKDIR /root/EfficientPose

RUN source /root/anaconda3/etc/profile.d/conda.sh \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && printf "y\ny\n" | conda create -n EfficientPose python==3.7 \
    && conda init && conda activate EfficientPose \
    && printf "y\n" | conda install tensorflow-gpu==1.15.0 \
    && pip install -r requirements.txt && python setup.py build_ext --inplace \
    && apt-get install -y libglib2.0-0 libsm6 libxrender1