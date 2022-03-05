FROM python:3

RUN mkdir /usr/share/pyshared/

WORKDIR /usr/share/pyshared/

COPY cli.py /usr/share/pyshared/
COPY init_clis.py /usr/share/pyshared/

# ENTRYPOINT [ "python /usr/share/pyshared/cli.py" ]
# TODO: add host argument later
ENTRYPOINT [ "python init_clis.py" ]