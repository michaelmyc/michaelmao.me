FROM pytorch/pytorch:1.8.0-cuda11.1-cudnn8-devel
WORKDIR /workspace

RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install lightdm -y
RUN apt-get install sudo nvidia-settings ffmpeg libsm6 libxext6 git -y
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt
RUN echo "git config --global --add safe.directory '*'" >> /root/.bashrc