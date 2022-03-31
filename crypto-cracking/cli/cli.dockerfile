FROM brendonky18/ctfs:crypto-cracking-base

ARG USER_NUM=0
ENV user_num=${USER_NUM}
ARG DEBUG
ENV debug=${DEBUG}

EXPOSE 22

RUN mkdir /usr/share/pyshared/
RUN mkdir /run/sshd

# Wireshark config
RUN groupadd wireshark
RUN chmod +x /usr/bin/dumpcap

RUN mkfifo /run/remote_pcap

# Manage User
RUN useradd -m -u 100${USER_NUM} -s /bin/bash user${USER_NUM}
RUN if [ ! -z "$debug" ] ; then echo 'root:rootpass' | chpasswd ; fi
RUN usermod -a -G wireshark user${USER_NUM}

# Lock down ssh user permission
RUN echo "PermitTTY no\nForceCommand cat /run/remote_pcap" >> /etc/ssh/sshd_config

COPY . /usr/share/pyshared/.
WORKDIR /usr/share/pyshared/
ENTRYPOINT \
python3 /mnt/.share/key_gen.py -g -u $user_num > /mnt/.share/pass$user_num \
&& cat /mnt/.share/pass$user_num | chpasswd \
& service ssh start \
& while true; do tcpdump -s 0 -U -n -w - -i eth0 not port 22 > /run/remote_pcap; done  \
& python3 init_clis.py --host 172.20.30.200 --hostnum $user_num $debug