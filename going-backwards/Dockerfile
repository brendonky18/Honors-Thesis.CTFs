FROM shimizukawa/python-all:ubuntu-12.04
COPY /pyftpd-0.8.4.5_mirror /srv/ftp

COPY FLAG /

EXPOSE 2121

ENTRYPOINT python2.5 --version &&  python2.5 /srv/ftp/pyftpd.py