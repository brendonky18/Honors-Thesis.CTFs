# Solution
There are three accounts with vulnerable passwords created by default in this application: "user", "test", and "roxon"

## Approach
There are a number of ways which the passwords could be cracked. The simplest approach is to try and brute-force some obvious passwords. If that does not work, you can try reversing engineering the code. Careful examination should reveal that the password hashed are stored as base-64 encoded md5 hashes. There are plentiful tools which should allow you to reverse the passwords online. First by decoding the base-64 into hex to get the md5 hash, and then looking up the hash online to find the original password.

Either approach should reveal the following logins:
 - user: user
 - test: test
 - roxon: noxor

Once that has been revealed, you must retrive the flag file from the root directory. This can be done using the `retr` command. However in order to do this, you must set up some way of retriving the file. The simplest approach to do this is to use `netcat` to listen on some port, and then on the ftp server, use the `port` command. 