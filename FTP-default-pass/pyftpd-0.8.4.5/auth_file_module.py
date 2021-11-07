
# autentificate from file  user:group:password

import string

from auth_file_config import *
        
def got_user(username, session, sessions):
        f = open(file, "r")
        group = None
        for i in f.readlines():
            s = string.split(i, ':', 2)
            if s[0] == username:
                group = s[1]
                return 331, "Password? Password?? Password!!!", username, group, 0, 1
        return 530, "No such user", "", "", -1, 1
        # return "message", username, groupname, X, Y
        # X == 0: deny access
        # X == 1: grant access
        # X == -1: does not concern this module
        # Y == 1: continue with other modules
        # Y == 0: definitive answer

def got_pass(username, password, session, sessions):
        if not username:
            return 503, "Login with USER first.", 0, 0
        f = open(file, "r")
        for i in f.readlines():
            s = string.split(i, ':', 2)
            if s[0] == username:
                if password == s[2][:-1]:
                    return 230, "Proceed, dear "+username, 1, 1
                else:
                    return 530, "Bad password", 0, 0
        return 530, "Uh oh, I am sorry...", -1, 1

