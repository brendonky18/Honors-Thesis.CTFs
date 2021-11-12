# Solution
There are three accounts with vulnerable passwords created by default in this application: "user", "test", and "roxon". You can crack these passwords in order to gain priviliged access, and then retrive the flag file from the root directory of the server. 

## Approach
There are a number of ways which the passwords could be cracked. The simplest approach is to try and brute-force some obvious passwords, however that's no fun. The intended solution is to get the password through reverse engineering the code.

Looking through the files, you will see that `pyftpd.py` contains the main execution loop, so this is where most people should be expected to start from. Afterwards, the students should be pointed towards five files:
1. `perm_acl_module.py`
    - This file checks which users have permission to execute certain commands
2. `perm_acl_config.py`
    - This file defines which commands are allowed to be used by each user or user group, and in which directories. 
3. `auth_db_config.py`
    - This file contains the stored login info for each account. In this file, you will discover that there are 3 user accounts created by default: "user", "test", and  "roxon". 
    - Furthermore, each of these accounts has a string associated with them which might be the password, however attempting to use them will reveal otherwise. 
4. `auth_db_README.txt`
    - This file reveals that those strings are in fact MD5 hashes, and that the file is created with `auth_db_module.py`.
5. `auth_db_module.py`
    - This file contains the python code which defines how users are authenticated when entering the `user` and `pass` commands.
    - This shows that the `auth_db_config.py` file stores the MD5 hashes in a base64 encoding.

Once you have gathered this, it should be fairly straightforward to log in, find, and retrive the flag. Looking at `perm_acl_config.py` tells us that any logged in user will be able to execute the `cwd`, `list`, and `retr`, commands from the root directory. So pick any user and then attempt to crack their password. To do this, take their hashed string from `auth_db_config.py`. First [reverse](https://base64.guru/converter/decode/hex) the base64 encoding in order to retrive the hash in it's original hexadecimal, afterwards you can lookup the hash to reveal the password. Since the passwords are all very commonly used, and their hashes are not salted, they can easily be [cracked](https://md5.gromweb.com/?md5=098f6bcd4621d373cade4e832627b4f6) by performing basic dictionary attack. 

Once the password has been revealed, we must retrive the flag file from the root directory. In order to get information from the FTP server, we must open a port on our machine to which the information can be sent. The simplest approach to do this is to use `netcat` to listen on some port, and then on the ftp server, use the `port` command to tell the FTP server to send the data to that port. After the connection has been estabished, we can perform the `list` command to see which files are in our dictionary. Doing this from the root directory will reveal that the `FLAG` file can be found here. To get the file we use the `retr` command.

Once this has been done, the CTF has been completed.