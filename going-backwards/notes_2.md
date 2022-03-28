## *Additional Notes*
This challenge is about reverse engineering. You must trace through the program's execution in order to figure out how it works. It may be helpful to familiarize yourself with some basic FTP commands as well. 

[Here](https://kb.iu.edu/d/aenq) is a list of basic commands.

[Here](https://en.wikipedia.org/wiki/List_of_FTP_commands) is a full list of FTP commands.

[Here](https://www.serv-u.com/resource/tutorial/pasv-response-epsv-port-pbsz-rein-ftp-command#fac52a38-7ddb-4815-a9dc-72cc03c0a8e6) is a link explaining how to establish a connection in FTP.

You should start by looking in the file `pyftpd.py`, and tracing the execution path. You should also look at the `BasicSession` class. In this class, there is a function which defines what the server does to execute each FTP command. Think about what commands you would need to execute in the server in order to find and then get the `FLAG.txt` file. 

At the very least you would need to list the files with the `list` command, and then copy the file with the `retr` command. However, in order to do these, you must be logged in, which requires the `user` and `pass` commands. Furthermore, in order to transmit the information from the `list` and `retr` commands, you must establish a second connection, using either the `port` or `pasv` command. 

Finally, as you can see on like 618 in `pyftpd`, the program imports various modules which modify how authentication and other functions are implemented. At the top of the file, we also see that it imports 3 other files: `utils.py`, `config.py` and `debug.py`. Looking inside `utils.py` reveals that it's fairly uninteresting. The same is true for `debug.py`. However, `config.py` is fairly interesting. Among other things, it imports `auth_anonymous_module`, and `auth_db_module`. 

Both of these sounds like they have to do with authentication so let's look at them more closely. Each module also imports a corresponding config file. `auth_anonymous_config.py` doesn't seem interesting, however `auth_cd_config.py` certainly does. It contains a list called `passwd`, and then some information. 

Looking back in `auth_db.py` we can see that the list `passwd` is used in the functions `got_user` and `got_pass`. It iterates over the list, and then compares the first sub-element `i` to the parameter `username`. This is a likely indication that the first element in the list ("admin") is a username. The `got_pass` function looks very similar, iterating over the `passwd` list. It compares the first element of the sub-element to the `username` parameter again, and then also compares the third element to the result of `md5hash(password)`. The comment at the top of the file also says `autentificate from internal database, passwords are md5-hashed`. From this, we have gathered that `auth_db_config.py` contains a list of user information, where the first item is the username and the third item is the md5 hash of the password. The `md5hash` function returns the result of `string.strip(binascii.b2a_base64(m.digest()))`, looking it up shows that `binascii.b2a_base64` converts binary data to base64 encoded ascii. 

***As a final reminder, please do not look at the other instructions.***