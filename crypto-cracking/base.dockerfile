FROM debian:latest
# environment vars
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="$PYTHONPATH:/usr/bin/python3"

# install packages
RUN apt update 
RUN apt install git openssh-server tcpdump wireshark python3 python3-pip

RUN pip install sympy parse git+https://github.com/brendonky18/PyDebugger

# init shared volume
RUN mkdir /mnt/.share
RUN chmod -R u=rwx,go-rwx /mnt/.share