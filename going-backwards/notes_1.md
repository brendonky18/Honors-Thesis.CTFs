## *Additional Notes*
This challenge is about reverse engineering. You must trace through the program's execution in order to figure out how it works. It may be helpful to familiarize yourself with some basic FTP commands as well. 

[Here](https://kb.iu.edu/d/aenq) is a list of basic commands.

[Here](https://en.wikipedia.org/wiki/List_of_FTP_commands) is a full list of FTP commands.

[Here](https://www.serv-u.com/resource/tutorial/pasv-response-epsv-port-pbsz-rein-ftp-command#fac52a38-7ddb-4815-a9dc-72cc03c0a8e6) is a link explaining how to establish a connection in FTP.

You should start by looking in the file `pyftpd.py`, and tracing the execution path. You should also look at the `BasicSession` class. In this class, there is a function which defines what the server does to execute each FTP command. Think about what commands you would need to execute in the server in order to find and then get the `FLAG.txt` file. 

You will need some way of navigating the file system, and listing the files available. You will also need some way of establishing a secondary connection over which the file can be transmitted. Furthermore, to do all of this, you must be able to log in to the server as a user. 

***As a final reminder, please do not look at the other instructions.***