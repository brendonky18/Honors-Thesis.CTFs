import time, sys

from log_simple_config import *

class Log:

    def openlog(self):
        global logfile
        if not logfile:
            if sys.platform[:3] == 'win':
                logfile = "c:/pyftpd.log"
            else:
                logfile = "/tmp/pyftpd.log"
        self.logfile = open(logfile, "a")
        
    def log(self, t, user, ip, command, boe): # time, who, ip, command, beginning=0 or end=1
        line = "%s %s@%s %s %i\n" % (time.ctime(t), user, ip, command, boe)
        self.logfile.write(line)
        self.logfile.flush()

    def closelog(self):
        self.logfile.close()

    def __del__(self):
        self.logfile.close()
        
