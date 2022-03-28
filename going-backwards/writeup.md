# Solution
In the original release of this program, there are three accounts created by default: "user", "test", and "roxon". For this challenge, the 3 accounts have been replaced by a single "admin" account, and the password. Previously the passwords matched the usernames, which was very easy to guess, and defeats the purpose of the challenge. 
## Approach
### Reverse Engineering
There are a number of ways which the passwords could be cracked. The simplest approach is to try and brute-force the password as there is no lock-out mechanism, however this may take a while. The intended solution is to get the password through reverse engineering the code.

Looking through the files, you will see that `pyftpd.py` contains the main execution loop, so this is where most people should be expected to start from. Afterwards, you should be pointed towards five files:
1. `perm_acl_module.py`
    - This file checks which users have permission to execute certain commands.
2. `perm_acl_config.py`
    - This file defines which commands are allowed to be used by each user or user group, and in which directories. 
3. `auth_db_config.py`
    - This file contains the stored login info for each account. In this file, you will discover that there is one user accounts created by default: "admin". 
    - Furthermore, this account has a string associated with it which looks like it should be the password, however attempting to use it does not work. 
4. `auth_db_README.txt`
    - This file reveals that the string is in fact a MD5 hash, and that the file is created with `auth_db_module.py`.
5. `auth_db_module.py`
    - This file contains the python code which defines how users are authenticated when entering the `user` and `pass` commands.
    - This shows that the `auth_db_config.py` file stores the MD5 hashes in a base64 encoding.

Once you have gathered this, it should be fairly straightforward to log in, find, and retrieve the flag. Looking at `perm_acl_config.py` tells us that any logged in user will be able to execute the `cwd`, `list`, and `retr`, commands from the root directory, and all subdirectories, i.e. the entire computer's file system. So next we must crack the user's password. To do this, take the hashed string from `auth_db_config.py`. First reverse the base64 encoding in order to retrieve the hash in it's original hexadecimal value. This is a useful [online tool](https://base64.guru/converter/decode/hex) to help with that. Afterwards you can lookup the hash to reveal the password. Since the password is a simple string, and looking at `auth_db_module.py` tells us that the hash is not salted, it can easily be cracked by performing basic dictionary attack. Here is another [website](https://md5.gromweb.com/?md5=098f6bcd4621d373cade4e832627b4f6) which can help you with that. 

### Connecting to the server

Once the password has been revealed, we must retrieve the flag file from the root directory. To do this, we must establish a connection to the server somehow. This can be dome many ways. In this approach, I will open a port on my local machine with the utility `netcat`, and tell the FTP server to connect to this port in active mode. To do this, I run the command

    nc -lkvn 65535

 - `l` tells netcat to listen on the local port 65535
 - `k` tells it to continue listening after a connection has been closed. This means that we don't have to continually re-running this command every time we want to get some information from the FTP server.
 - `v` tells netcat to run in *verbose* mode, meaning that we will get more information
 - `n` tells netcat to ignore dns name resolution.

\* On some installations of debian, ubuntu and linux, the version of `netcat` has a bug which means this won't work. To get around this, you can use ncat, which is nearly identical except it does not have this issue. You can install it with:

    sudo apt-get install ncat

Next, connect to the server

    nc 172.20.30.128 2121

### Finding the Flag
After connecting to the server and establishing the FTP session, log in with the command

    user <username>

Enter the password with the command

    pass <password>

Now before you can get any information, you must tell the server to connect to the socket we opened with a `port` command

    port x,x,x,x,255,255

The port command in FTP is slightly different from what most people are used to. Instead of taking a socket in the typical form `127.0.0.1:65535`, it takes a comma-separated list of 6 bytes. The first 4 bytes are your ip address, and the last two bytes are the higher, and lower order bytes of the port. 

In this implementation specifically, it ignores the ip address, and will always transmit to the address which established the connection. So you can simply run

    port 255,255

However you establish the connection, once it has been established, we can perform the `list` command to see which files are in our dictionary. Doing this from the root directory will reveal that the `FLAG.txt` file can be found here. To get the file's contents we use the `retr` command. This will send the file's contents to the netcat listening socket.

Once this has been done, you have captured the flag. The CTF has been completed.