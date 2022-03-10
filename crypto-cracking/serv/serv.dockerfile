FROM python:3

RUN useradd -ms /bin/bash servadmin
RUN mkdir /srv/RSA

USER servadmin

WORKDIR /srv/RSA

COPY . /srv/RSA
# TODO: won't be necessary later,
# networking will be handled over docker network instead of bridge network
EXPOSE 26220
EXPOSE 26221
EXPOSE 26222

# TODO: make generic container with installed python dependencies
#       will make buildin containers faster
RUN export PYTHONPATH=/usr/bin/python && \
    pip install --upgrade pip && \
    # pip install threading && \
    # pip install import argparse && \
    pip install sympy 

ENTRYPOINT [ "python", "init_servs.py" ]
