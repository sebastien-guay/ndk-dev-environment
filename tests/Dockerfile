FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -U pip
RUN pip3 install setuptools
WORKDIR /mnt
COPY requirements.txt /root
RUN cd /root && pip3 install -r requirements.txt
