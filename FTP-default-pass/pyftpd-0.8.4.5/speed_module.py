from speed_config import *

from utils import myfnmatch

def got_user(username, session, sessions):
    return 331, "Give me password", "", "", -1, 1

def got_pass(username, password, session, sessions):
    for i in speedlist:
        if myfnmatch(username, i[0]):
            session.limit_retr_speed = float(i[1])
            session.limit_stor_speed = float(i[2])
    return 530, "Sorry", -1, 1
