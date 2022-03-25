FROM crypto-cracking:base

ARG USER_NUM
ENV user_num=${USER_NUM}

EXPOSE 22

RUN mkdir /usr/share/pyshared/
RUN mkdir /run/sshd

# Wireshark config
RUN groupadd wireshark
RUN chmod +x /usr/bin/dumpcap

RUN mkfifo /run/remote_pcap

# Manage User
RUN useradd -m -u 100${USER_NUM} -s /bin/bash user${USER_NUM}
RUN echo 'root:rootpass' | chpasswd
RUN usermod -a -G wireshark user${USER_NUM}

USER user${USER_NUM}

COPY . /usr/share/pyshared/.
WORKDIR /usr/share/pyshared/

ENTRYPOINT echo rootpass | su root -c "python3 /mnt/.share/key_gen.py -g -u $user_num > /mnt/.share/pass$user_num \
&& cat /mnt/.share/pass$user_num | chpasswd \
& service ssh start \
& python3 init_clis.py --host 10.0.0.20 --hostnum $user_num \
& tcpdump -s 0 -U -n -w - -i eth0 not port 22 > /tmp/remote_pcap" 2> \
# redirect "Password:" prompt
/dev/null 