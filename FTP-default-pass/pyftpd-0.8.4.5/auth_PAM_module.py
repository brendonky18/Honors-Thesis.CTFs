import PAM, pwd, grp, os
from utils import *
from debug import debug

from auth_PAM_config import *

def got_user(username, session, sessions):
    try:
        group = grp.getgrgid(pwd.getpwnam(username)[3])[0]
    except KeyError:
        group = ""
    return 331, "Password? Password?? Password!", username, group, 0, 1
        
def got_pass(username, password, session, sessions):
    if not username:
        return "503 Login with USER first.", 0, 0
    def pam_conv(auth, query_list, password=password):
        resp = []
        for i in range(len(query_list)):
            query, t = query_list[i]
            if t == PAM.PAM_PROMPT_ECHO_ON:
                val = password
                resp.append((val, 0))
            elif t == PAM.PAM_PROMPT_ECHO_OFF:
                val = password
                resp.append((val, 0))
            elif t == PAM.PAM_PROMPT_ERROR_MSG or t == PAM.PAM_PROMPT_TEXT_INFO:
                print query
                resp.append(('', 0));
            else:
                return None
        return resp
        
    user = username
    try:
        group = grp.getgrgid(pwd.getpwnam(username)[3])[0]
        uid, gid = user, group
    except KeyError:
        uid, gid = "nobody", "nogroup"
    auth = PAM.pam()
    auth.start(service)
    auth.set_item(PAM.PAM_USER, user)
    auth.set_item(PAM.PAM_CONV, pam_conv)
    try:
        auth.authenticate()
        auth.acct_mgmt()
    except PAM.error, resp:
        try:
            os.setgid(grp.getgrnam(gid)[2])
            os.setuid(pwd.getpwnam(uid)[2])
        except:
            debug("Setuid failed")
            return 530, "Sorry, having problems with the server...", 0, 0
        return 530, "Wrong: %s" % resp, 0, 1
    except:
        log("PAM Internal error")
        return 530, "Wrong: internal error", 0, 0
    else:
        try:
            os.setgid(grp.getgrnam(gid)[2])
            os.setuid(pwd.getpwnam(uid)[2])
        except:
            debug("Setuid failed")
            return 530, "Sorry, having problems with the server...", 0, 0
        return 230, "OK, logged in.", 1, 1
