import os, os.path, fnmatch, sys, string

from config import do_debug

try:
    import syslog1
    def opendebug(a):
        return syslog.openlog(a, 0, syslog.LOG_DAEMON)

    def debug(text):
        if do_debug:
            return syslog.syslog(text)
    closedebug = syslog.closelog
except:
    def opendebug(a):
        pass
    def debug(text):
        print text
    def closedebug():
        pass


