FROM python:3

RUN useradd -ms /bin/bash user_1
RUN mkdir /usr/share/pyshared/

USER user_1

# DEBUGGING
# RUN hostname -I

WORKDIR /usr/share/pyshared/

COPY . /usr/share/pyshared/

RUN export PYTHONPATH=/usr/bin/python && \
    pip install --upgrade pip && \
    # pip install threading && \
    # pip install import argparse && \
    pip install sympy 

# ENTRYPOINT [ "python /usr/share/pyshared/cli.py" ]
# TODO: make cmd variable?
ENTRYPOINT [ "python", "init_clis.py", "--host", "10.0.0.22" ]