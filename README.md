# CTFs
## Part 1
The solution can be found [here](/FTP-default-pass/SOLUTION.md)

Pull the container by running `docker pull brendonky18/ctfs/ftp-default-pass`

The name should provide you quite a substantial hint, it involves the default password on an FTP server, the source code for which can be found [here](http://kassiopeia.juls.savba.sk/~garabik/software/pyftpd/). The vulnerbality is disclosed in [CVE-2010-2073](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2010-2073).

*Warning*: the files are only accessible through an unsecure http connection. They are also available on the github respoitory [here](https://github.com/brendonky18/CTFs/tree/main/FTP-default-pass/pyftpd-0.8.4.5).
