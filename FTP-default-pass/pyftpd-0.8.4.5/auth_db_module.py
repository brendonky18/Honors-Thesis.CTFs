
# autentificate from internal database, passwords are md5-hashed

import string, md5, binascii
from auth_db_config import *

def md5hash(s):
    m = md5.new()
    m.update(s)
    return string.strip(binascii.b2a_base64(m.digest()))
        
def got_user(username, session, sessions):
        group = None
        for i in passwd:
            if i[0] == username:
                group = i[1]
                return 331, "Password? Password?? Password!!!", username, group, 0, 1
        return 331, "Password? Password?? Password!!! (will be bad anyway)", "", "", -1, 1
        # return "message", username, groupname, X, Y
        # X == 0: deny access
        # X == 1: grant access
        # X == -1: does not concern this module
        # Y == 1: continue with other modules
        # Y == 0: definitive answer

def got_pass(username, password, session, sessions):
        if not username:
            #return 503, "Login with USER first.", 0, 0
            return 530, "Bad password.", 0, 0
        for i in passwd:
            if i[0] == username:
                if md5hash(password) == i[2]:
                    return 230, "Proceed, dear "+username, 1, 1
                else:
                    return 530, "Bad password", 0, 0
        return 530, "Uh oh, I am sorry...", -1, 1

