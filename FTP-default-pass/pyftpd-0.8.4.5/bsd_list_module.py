import string
from stat import *
import time, socket

class Session:
    def cmd_list(self, args):

        args = string.split(args or "")
        if not self.create_datasock():
            return
        paths = []
        opts = ""
        for i in args:
            if i[0] == "-":
                opts = opts+i[1:]
            else:
                paths.append(i)
        if not paths:
            paths = [self.cwd]
           
        for path in paths:
            path = self.joinpath(self.cwd, path)
            perm = self.logged and self.permcheck(path, self.user, self.group, self, "list")
            if not perm:
                self.reply("550 Sorry")
                return
            cwd = self.cwd
            try:
                isf = self.filesys.isfile(path)
                isd = self.filesys.isdir(path)
            except OSError:
                self.reply("550 I cannot")
                return
            if isf or (isd and 'd' in opts):
                lp = [path]
            elif isd:
                try:
                    self.filesys.chdir(path)
                    cwd = path
                    lp = self.filesys.listdir(path)
                except OSError:
                    self.reply("550 I cannot")
                    return
                #if "a" in opts:
                #    lp.append(self.filesys.curdir)
                #    lp.append(self.filesys.pardir)
            else:
                self.reply("550 Uh, what?")
                return
            if not '1' in opts: # long format
                r = []
                for l in lp:
                    i = self.joinpath(cwd, l)
                    try:
                        appendix = ""
                        if self.filesys.islink(i) and not "L" in opts:
                            dirflag = "l"
                            appendix = " -> "+self.filesys.readlink(i)
                        elif self.filesys.isdir(i):
                            dirflag = "d"
                        else:
                            dirflag = "-"
                        status = self.filesys.stat(i)
                        size = status[ST_SIZE]
                        user = str(status[ST_UID])
                        group = str(status[ST_GID])
                        t = status[ST_CTIME]
                        if t == -1:
                            t = 0
                        ctime = time.strftime("%b %d  %Y",time.gmtime(t))
                        if self.filesys.isexec(i):
                            perm = "rwx"
                        else:
                            perm = "rw-"
                        rl = "%s%s%s%s  1 %-10s  %-10s %10i %s %s%s\r\n" % \
                             (dirflag, perm,perm,perm, user, group, size, ctime, l, appendix)
                        r.append(rl)
                    except OSError:
                        pass
            else:
                r = map(lambda x: "%s\r\n" % x, lp)
            try:
                for i in r:
                    self.sock.send(i)
            except socket.error:
                break
        try:
            self.close_datasock()
        except socket.error:
            pass

        del r # to save memory
        self.reply("226 Wow, listing done")

        
