FROM python:2.7.18

WORKDIR /srv

COPY /pyftpd-0.8.4.5 /srv/ftp

COPY FLAG /

EXPOSE 2121

ENTRYPOINT [ "python", "/srv/ftp/pyftpd.py" ]