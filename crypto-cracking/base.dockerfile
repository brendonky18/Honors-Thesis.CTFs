FROM debian:latest
# environment vars
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="$PYTHONPATH:/usr/bin/python3"

# install packages
RUN apt update 
RUN apt install openssh-server tcpdump wireshark python3 python3-pip -y

RUN pip install sympy 

# init shared volume
RUN mkdir /mnt/.share
RUN chmod -R u=rwx,go-rwx /mnt/.share