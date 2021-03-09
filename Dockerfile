FROM tensorflow/tensorflow:2.4.0-gpu
MAINTAINER Akash Harijan

RUN apt-get update -y && \
    apt install software-properties-common -y && \
    apt install libgl1-mesa-glx -y &&  \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update -y && \
    apt install python3.8 -y && \
    apt install python3-pip -y && \
    apt install -y libsm6 libxext6 && \
    apt-get install nginx -y && \
    apt-get install ca-certificates && \
    apt-get install libxrender1

    # 3. Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.
RUN python --version

RUN pip install --upgrade pip

# RUN python3.8 --version
# RUN echo $PATH

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY requirements.txt /opt/program/requirements.txt

WORKDIR /opt/program
RUN pip install -r requirements.txt
COPY . /opt/program
