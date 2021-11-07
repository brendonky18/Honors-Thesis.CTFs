from iplimit_config import *

from utils import myfnmatch

def got_user(username, session, sessions):
    for i in limitlist:
        if myfnmatch(username, i[0]):
            cnt = 0
            for j in sessions.keys():
                cs = sessions[j]
                if not username: 
                    print "AAAA", `username`, `cs.user`
                if cs.ip == session.ip and myfnmatch(username, cs.user):
                    cnt = cnt+1
            if cnt >= i[1]: # >= because we counted ourselves in
                return 530, "Only %i users from one IP address allowed" % i[1] , "", "", 0, 0
    return 331, "Give me password", "", "", -1, 1

def got_pass(username, password, session, sessions):
    return 530, "Sorry", -1, 1
