from utils import myfnmatch

from perm_acl_config import *

def permcheck(f, user, group, session, operation):
    accesslist = {}
    #f = session.v2fs(f)
    for i in acllist:
        if (   myfnmatch(user, i[0]) and
               myfnmatch(group, i[1]) and
               myfnmatch(session.ip, i[2]) and
               myfnmatch(f, i[3]+"*")
            ):
            for j in i[4]: # append allowed operations
                accesslist[j] = 1
            for j in i[5]: # and then remove denied ones
                if accesslist.has_key(j):
                    del(accesslist[j])
    if accesslist.has_key(operation):
        return 1, 1
    else:
        return 0, 1
    
