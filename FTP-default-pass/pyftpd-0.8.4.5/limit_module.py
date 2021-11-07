from limit_config import *

from utils import myfnmatch

def got_user(username, session, sessions):
    for i in limitlist:
        if myfnmatch(username, i[0]):
            cnt = 0
            for j in sessions.keys(): # [1]
                try:
                    cs = sessions[j] # [2]
                    if myfnmatch(username, cs.user):
                        cnt = cnt+1
                except KeyError: # if session was deleted between [1] and [2]
                    pass
            if cnt >= i[1]:
                return 530, "Only %i users allowed" % i[1] , "", "", 0, 0
    return 331, "Give me password", "", "", -1, 1

def got_pass(username, password, session, sessions):
    return 530, "Sorry", -1, 1
