FROM brendonky18/ctfs:crypto-cracking-base

ARG DEBUG
ENV debug=${DEBUG}

RUN useradd -ms /bin/bash servadmin

EXPOSE 26220
EXPOSE 26221
EXPOSE 26222

COPY key_gen.py /tmp

# set up python3 server
RUN mkdir /srv/RSA
COPY . /srv/RSA
WORKDIR /srv/RSA

# set up flag mount point
RUN mkdir /mnt/.flag
RUN chmod -R u=rwx,go-rwx /mnt/.flag

ENTRYPOINT mv /tmp/key_gen.py /mnt/.share && python3 /mnt/.share/key_gen.py -g -u 3 > /mnt/.share/pass3 \
&& cp /mnt/.share/pass3 /mnt/.flag/flag.txt \
& python3 init_servs.py $debug
