from utils import myfnmatch
from ban_config import *

def got_user(username, session, sessions):
    for i in banlist:
        if myfnmatch(session.ip, i):
            return 530, banmsg, "", "", 0, 0
    return 331, "Give me password", "", "", -1, 1

def got_pass(username, password, session, sessions):
    return 530, "Sorry", -1, 1

