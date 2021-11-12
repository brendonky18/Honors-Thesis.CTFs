This *README* is meant as a guide for instructors who wish to use any of these modules as instructions. Do not provide students with access to this file as it contains all of the solutions for each of the problems. 

# CTF 1
## Solution
The solution to this module can be found [here](/FTP-default-pass/SOLUTION.md)

## Setup Instructions
You will need two separate machines: one to act as the server, and one which will the students will use as the client to access the server. Both machines must be in the same network, or otherwise be abbessible to each other over the internet.

### Server
The server machine can be of any OS, however it must have docker installed as you will need to run docker containers. 

Pull the docker image:
    
    docker pull brendonky18/ctfs/ftp-default-pass

Run the container, expose container port 2121 and map it to a host port, the specific number doesn't matter but we can stick with port 2121:

    docker run -p 2121:2121 brendonky18/ctfs:ftp-default-pass

The server is now ready!
### Client
The client machine can be of any OS, however it must be able to run `netcat` or some equivalent in order to connect to servers and listen on sockets. In fact, at least as of the time of writing this, you may encounter the error: `inverse host lookup failed: Unknown host` while using `netcat`. I would use `ncat` which is an otherwise identical implementation, if this is a problem you or your students encounter.

Otherwise there is no special setup required for the client machines. 

<!-- The name should provide you quite a substantial hint, it involves the default password on an FTP server, the source code for which can be found [here](http://kassiopeia.juls.savba.sk/~garabik/software/pyftpd/). The vulnerbality is disclosed in [CVE-2010-2073](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2010-2073).

*Warning*: the files are only accessible through an unsecure http connection. They are also available on the github respoitory [here](https://github.com/brendonky18/CTFs/tree/main/FTP-default-pass/pyftpd-0.8.4.5). -->

## Student Instructions
You should provide students with the following instructions:

> There is an FTP server running on port 2121 in the same network as you are. Inside this server there is a file titled `FLAG` which you must retrive and submit to complete this assignment. The ftp server running is `pyftp 0.8.4.5`, which was available on Debian Release: 5.0.4 in 2009. The original source code for this is available [here](http://kassiopeia.juls.savba.sk/~garabik/software/pyftpd/), however as this is an insecure http connection, there is also a [mirror](https://github.com/brendonky18/CTFs/tree/main/FTP-default-pass/pyftpd-0.8.4.5) of source code available. 
> 
> Your task is to *reverse engineer* this program in order to discover a vulnerability which will allow you to capture the `FLAG`. 
> 
> **Reverse Engineering** is the process of dismantling and examining a programs source code - or sometimes even the assembly or raw binaries - in order to understand what it does, and how it works. 
> 
> If you are not familiar with FTP, a list of commands you can use is available [here](https://en.wikipedia.org/wiki/List_of_FTP_commands).
> 
> Good luck!