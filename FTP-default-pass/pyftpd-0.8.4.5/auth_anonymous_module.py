from auth_anonymous_config import *
import re

def got_user(username, session, sessions):
    if username in ("anonymous", "ftp"):
        return 331, "Give me you email NOW!", "anonymous", "anonymous", 0, 1
    return 331, "Give me password", "", "", -1, 1
    # return "message", username, groupname, X, Y
    # X == 0: deny access
    # X == 1: grant access
    # X == -1: does not concern this module
    # Y == 1: continue with other modules
    # Y == 0: definitive answer

def got_pass(username, password, session, sessions):
    if username in ("anonymous", "ftp"):
        if not '@' in password:
            return 530, "This is not a valid email", 0, 0
        if re.match("IE(..)?User@.*", password, re.I):
            return 530, "Use proper ftp client, not Internet Explorer!", 0, 0
        if password in ("mozilla@", "MOZILLA@"):
            return 530, "Use proper ftp client, not Netscape!", 0, 0
        if password in  ("NovellProxyCache@", "Squid@"):
            return 530, "Use proper ftp client, not www browser", 0, 0
        return 230, welcome_msg, 1, 1
    else:
        return 530, "Sorry", -1, 1
    # return "message", X, Y
    # X == 0: deny access
    # X == 1: grant access
    # X == -1: does not concern this module
    # Y == 1: continue with other modules
    # Y == 0: definitive answer

