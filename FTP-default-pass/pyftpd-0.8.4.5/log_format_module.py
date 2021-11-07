import time, sys

import log_simple_module

class Log(log_simple_module.Log):

    def log(self, t, user, ip, command, boe): # time, who, ip, command, beginning=0 or end=1
        if command[:4] == "PASS" and user not in ("anonymous", "ftp"):
            command = "PASS (hidden)"
        event = {'t':time.ctime(t),
                 'user': user,
                 'cmd': command,
                 'ip': ip
                 }
        if boe == 0: #begin
            line = '%(t)s:start "%(cmd)s" from %(user)s@%(ip)s ' % event
        elif boe == 1: #end
            line = '%(t)s:stop  "%(cmd)s" from %(user)s@%(ip)s ' % event
        else:
            line = '%(t)s:      "%(cmd)s" from %(user)s@%(ip)s ' % event
        self.logfile.write(line+"\n")
        self.logfile.flush()


