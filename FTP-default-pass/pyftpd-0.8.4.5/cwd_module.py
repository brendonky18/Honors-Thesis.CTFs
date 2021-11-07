from cwd_config import *

from utils import myfnmatch

def got_user(username, session, sessions):
    return 331, "Give me password", "", "", -1, 1

def got_pass(username, password, session, sessions):
    for i in cwdlist:
        if myfnmatch(username, i[0]):
            session.cwd = i[1]
    return 530, "Sorry", -1, 1
