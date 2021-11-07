#!/usr/bin/python
# maybe you need to change the above line


import sys, socket, string, time, types
from stat import *
import timeout_socket
import SocketServer
import posixpath
#import new

from utils import *
from config import *

from debug import *

# characters which must not appear in filenames
filename_deniedchars = map(chr, range(32))

class BasicSession:

    def __init__(self, rfile, wfile, client_address):
    
        self.user = ""
        self.group = ""
        self.logged = 0
        self.curcmd = "just connected"
        self.exit_immediately = 0
        self.pendingconn = 0 # if there is an open data connection - for ABOR
        self.last_cmd_time = self.session_create_time = time.time()
        self.rfile = rfile
        self.wfile = wfile
        self.restpos = 0
        self.passive = 0
        self.create_datasock = self.create_nonpasv_datasock
        self.ip = client_address[0]
        self.dataport = None
        opendebug("pyftpd["+self.ip+"]")
        self.replymessage(220, initial_msg)
        self.cwd = initial_wd
        self.limit_retr_speed = 0.
        self.limit_stor_speed = 0.

        self.permcheck = permcheck        
        log.log(time.time(), "", self.ip, "CONNECT", -1)
        
        self.cmddict = {
            "quit": self.cmd_quit,
            "syst": self.cmd_syst,
            "user": self.cmd_user,
            "pass": self.cmd_pass,
            "port": self.cmd_port,
            "stor": self.cmd_stor,
            "appe": self.cmd_appe,
            "dele": self.cmd_dele,
            "mkd" : self.cmd_mkd,
            "rmd" : self.cmd_rmd,
            "retr": self.cmd_retr,
            "rest": self.cmd_rest,
            "size": self.cmd_size,
            "list": self.cmd_list,
            "nlst": self.cmd_nlst,
            "pasv": self.cmd_pasv,
            "pwd" : self.cmd_pwd,
            "cwd" : self.cmd_cwd,
            "cdup": self.cmd_cdup,
            "site": self.cmd_site,
            "abor": self.cmd_abor,
            "type": self.cmd_dummy
            }
    
    def joinpath(self, b, a):
        # join b and a, if a is absolute path, return just a
        r = posixpath.normpath(posixpath.join(b, a))
        # make sure nobody can cheat with leading ..
        if r[0]<>"/": # something wrong
            return ""
        r = string.replace(r, "/../", "")
        return r
            
    def reply(self, x):
        self.wfile.write(x + "\r\n")
        self.wfile.flush()
        debug("---> "+repr(x))
            
    def replymessage(self, n, x): # reply to the client, x is possibly tuple of lines
        if type(x) == types.StringType:
            self.reply(`n`+" "+x)
        else:
            for i in x[:-1]:
                self.reply(`n`+"-"+i)
            self.reply(`n`+" "+x[-1])

    def create_nonpasv_datasock(self):
        if not self.dataport:
            self.reply("425 what about a PORT command?")
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = t_socket(sock=sock, timeout=timeout_data)
            self.sock.connect((self.ip, self.dataport))
            self.reply("150 dataconnection is up!")
            return 1
        except socket.error:
            try:
                print "IP:"
                print self.ip
                print "port"
                print self.dataport
                self.reply("425 your dataport sucks big time!")
                return None
            except:
                pass
                return None
        except timeout_socket.Timeout:
            return None

    def create_pasv_datasock(self):
        try:
            self.sock = t_socket(sock=self.sock, timeout=timeout_data)
            conn, addr = self.sock.accept()
            self.sock = t_socket(sock=conn, timeout=timeout_data)
            self.reply("150 dataconnection is up!")
            self.create_datasock = self.create_nonpasv_datasock
            return 1
        except "socket.error":
            self.reply("425 cannot create socket")
            return None

    def close_datasock(self):
        self.sock.close()

    def cmd_quit(self,_):
        self.reply("221 Have a good one!")
        raise "session_exit"

    def cmd_abor(self,_):
        if self.pendingconn and threading:
            self.abort_received = 1
            while self.pendingconn:
                time.sleep(0.1) # prevent from taking up 100% CPU
        self.reply("226 Aborted")
        return

    def cmd_user(self, username):
        n, r, self.user, self.group, self.logged = got_user(username, self, sessions)
        self.replymessage(n, r)
        if self.logged:
            self.filesys = FileSystem(self)

    def cmd_pass(self, password):
        n, r, self.logged = got_pass(self.user, password, self, sessions)
        self.replymessage(n, r)
        if self.logged:
            self.filesys = FileSystem(self)


    def cmd_dummy(self, _):
        self.reply("200 OK (in other words: ignored)")

    def cmd_syst(self, _):
        self.reply("215 UNIX Type: L8")

    def cmd_pwd(self, _):
        self.reply('257 "%s" is where you are' % (self.cwd))

    def cmd_cdup(self,_):
        self.cmd_cwd("..")

    def cmd_cwd(self, path):
        if path:
            path = self.joinpath(self.cwd, path)
            perm = self.logged and permcheck(path, self.user, self.group, self, "cwd") 
            if not perm:
                self.reply("550 You are not allowed to")
                return
            try:
                self.filesys.chdir(path)
            except OSError:
                self.reply("550 You are not allowed to")
                return
            self.cwd = path
        self.reply("250 Ok, going there")

    def cmd_site(self, command):
        perm = self.logged and permcheck(command, self.user, self.group, self, "site") 
        if not perm:
            self.reply("550 You are not allowed to")
            return
        c = string.split(command)
        cmd, arg =  string.lower(c[0]), c[1:]
        if cmd == "ps":
            sl = []
            for i in sessions.keys():
                cs = sessions[i]
                sl.append(" %i %s[%s]@%s %% %s" % (i, cs.user, cs.group, cs.ip, cs.curcmd))
            sl.append("TOTAL %i" % len(sessions))
            self.replymessage(250,sl)
            return
        elif cmd == "shutdown": # does not work
            self.reply("250 Oh dear, shutting down server")
            sys.exit(0)
        elif cmd == "kill":
            try:
                pid2kill = int(arg[0])
            except:
                self.reply("400 PID error")
                return
            if sessions.has_key(pid2kill):
                sessions[pid2kill].exit_immediately=1
            else:
                self.reply("400 No such PID")
                return
        else:
            self.reply("500 Unknown SITE command")
            return
        self.reply("250 Ok, done.")

    def cmd_noop(self,_):
        self.reply("200 NOOPing")

    def cmd_pasv(self, _):
        FTP_DATA_BOTTOM = 40000
        FTP_DATA_TOP    = 44999
        
        for port in xrange(FTP_DATA_BOTTOM, FTP_DATA_TOP):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind(('', port))
                break
            except socket.error:
                pass
        else:
            self.reply("425 Cannot be passive")
            return
            
        self.sock.listen(1)
        adr, self.dataport = self.sock.getsockname()
        #if not adr or adr == '0.0.0.0':
        #    adr = socket.gethostname()
        adr = socket.gethostbyname(socket.gethostname())
        adr = string.replace(adr, ".", ",")
        porthi, portlo = self.dataport/256, self.dataport%256
        self.passive = 1
        self.create_datasock = self.create_pasv_datasock
        self.reply("227 Entering Passive Mode (%s,%i,%i)" % (adr, porthi, portlo))

    def cmd_port(self, port_id):
        numstr = filter(lambda x: x in "0123456789,", port_id)
        parts = string.split(numstr,",")

        try:
            hi = int(parts[-2])
            lo = int(parts[-1])
            for v in [hi,lo]:
                if v < 0 or v > 255:
                    raise ValueError
        except IndexError:    
            self.reply("501 are you a hacker?")
            return
        except ValueError:
            self.reply("501 looks like nonsense to me...")
            return

        self.dataport = (hi << 8) + lo
        self.reply("230 Port is " + str(self.dataport)+ " (am ignoring specified IP for security)")

    def stor_or_appe(self, filename, comm, mode):
        #if filename[0] == ".":
        #    self.reply("553 No dot files please!")
        #    return
        if filter(lambda x: x in filename_deniedchars, filename):
            self.reply("553 Bad characters in filename")
            return
        path = self.joinpath(self.cwd, filename)
        perm = self.logged and permcheck(path, self.user, self.group, self, comm)
        if not perm:
            self.reply("530 Permission denied")
            return
        r = "226 Phew, upload successfully completed"
        try:
            f = self.filesys.open(path, mode)
        except IOError:
            self.reply("553 File creation failed!")
            return

        if not self.create_datasock():
            f.close()
            return

        self.abort_received = 0
        self.pendingconn = 1
        try:
            while 1:
                if self.abort_received:
                    r = "426 Aborted"
                    break

                if self.limit_stor_speed:
                    timer = time.time()
                    s = self.sock.recv(rbufsize)
                    if len(s) == 0:
                        break
                    dur = time.time()-timer
                    #speed = len(s)/dur
                    #if speed>self.limit_stor_speed:
                    if dur*self.limit_stor_speed<len(s): # to avoid division
                        time.sleep(len(s)/self.limit_stor_speed-dur)
                else:
                    s = self.sock.recv(rbufsize)
                    if len(s) == 0:
                        break
                f.write(s)
        except socket.error:
            r = "425 Socket error"
        except IOError:
            r = "553 Upload error"
        except timeout_socket.Timeout:
            r = "425 Timeout while uploading"
        try:
            self.close_datasock()
        except socket.error:
            r = "425 Socket error"
        f.close()
        try:
            self.reply(r)
        except:
            pass
        self.pendingconn = 0

    def cmd_stor(self, filename):
        if threading:
            thread.start_new_thread(self.stor_or_appe, (filename, "stor", "wb"))
        else:
            self.stor_or_appe(filename, "stor", "wb")

    def cmd_appe(self, filename):
        if threading:
            thread.start_new_thread(self.stor_or_appe, (filename, "appe", "ab"))
        else:
            self.stor_or_appe(filename, "appe", "ab")

    def cmd_dele(self, filename):
        path = self.joinpath(self.cwd, filename)
        perm = self.logged and permcheck(path, self.user, self.group, self, "dele")
        if not perm:
            self.reply("550 NO!")
            return
        try:
            self.filesys.unlink(path)
        except OSError:
            self.reply("550 I cannot")
            return
        self.reply("250 File eliminated")

    def cmd_mkd(self, path):
        path = self.joinpath(self.cwd, path)
        perm = self.logged and permcheck(path, self.user, self.group, self, "mkd")
        if not perm:
            self.reply("550 Permission denied.")
            return
        try:
            self.filesys.mkdir(path)
        except OSError:
            self.reply("550 I cannot")
            return
        self.reply('257 "%s" Directory created' % path)

    def cmd_rmd(self, path):
        path = self.joinpath(self.cwd, path)
        perm = self.logged and permcheck(path, self.user, self.group, self, "rmd")
        if not perm:
            self.reply("550 Permission denied.")
            return
        try:
            self.filesys.rmdir(path)
        except OSError:
            self.reply("550 I cannot")
            return
        self.reply("250 Directory removed")

    def cmd_rest(self, pos):
        try:
            self.restpos = long(pos)
            self.reply("350 Restarting. Are you happy?")
            return
        except ValueError:
            self.reply("530 Sorry.")

    def cmd_retr(self, filename):
        if threading:
            thread.start_new_thread(self.cmd_retr1, (filename,))
        else:
            self.cmd_retr1(filename)

    def cmd_retr1(self, path):
        path = self.joinpath(self.cwd, path)
        perm = self.logged and permcheck(path, self.user, self.group, self, "retr")
        if not perm:
            self.reply("530 Permission denied")
            return
        if self.filesys.isdir(path):
            self.reply("550 You cannot RETR a directory, what are you?")
            return
        try:
            f = self.filesys.open(path,"rb")
            if self.restpos:
                f.seek(self.restpos)
        except (IOError, OSError):
            self.restpos = 0
            self.reply("553 File read failed!")
            return
        self.restpos = 0

        r = "226 Enjoy the file"
        if not self.create_datasock():
            f.close()
            return
        self.abort_received = 0
        self.pendingconn = 1
        try:
            while 1:
                if self.abort_received:
                    r = "426 Aborted"
                    break
                s = f.read(sbufsize)
                if not s:
                    break
                if self.limit_retr_speed:
                    timer = time.time()
                    self.sock.send(s)
                    dur = time.time()-timer
                    #speed = len(s)/dur
                    #if speed>self.limit_retr_speed:
                    if dur*self.limit_retr_speed<len(s): # to avoid division
                        time.sleep(len(s)/self.limit_retr_speed-dur)
                else:
                    self.sock.send(s)
        except socket.error:
            r = "425 Socket error"
        except (IOError, OSError):
            r = "421 File read error"
        except timeout_socket.Timeout:
            r = "425 Timeout while RETRieving"
        try:
            self.close_datasock()
        except socket.error:
            r = "425 Socket error"
        f.close()
        try:
            self.reply(r)
        except:
            pass
        self.pendingconn = 0


    def cmd_size(self, path):
        path = self.joinpath(self.cwd, path)
        perm = self.logged and permcheck(path, self.user, self.group, self, "size")
        if not perm:
            self.reply("530 Permission denied")
            return
        if self.filesys.isdir(path):
            self.reply("550 You cannot SIZE a directory, what are you?")
            #in fact, you could, but we need it to make netscape happy...
            return
        try:
            size = self.filesys.stat(path)[ST_SIZE]
        except (OSError, IOError):
            self.reply("553 File read failed!")
            return
        self.reply("213 %s" % size)


    def cmd_nlst(self, path):
        if not self.create_datasock():
            return
        if not path:
            path = self.cwd
        else:
            path = self.joinpath(self.cwd, path)
        perm = self.logged and permcheck(path, self.user, self.group, self, "nlst")
        if not perm:
            self.reply("550 Sorry")
            return
        if self.filesys.isdir(path):
            try:
                self.filesys.chdir(path)
                lp = self.filesys.listdir(path)
            except OSError:
                self.reply("550 I cannot")
                return
        else:
            self.reply("550 You should NLST only a directory")
            return
        r = map(lambda x: "%s\r\n" % x, lp)
        try:
            for i in r:
                self.sock.send(i)
        except socket.error:
            pass
        try:
            self.close_datasock()
        except socket.error:
            pass

        del r # to save memory
        self.reply("226 Wow, listing done")


    def cmd_list(self, path):
        # this is dumb
        # real listing will be provided via additional modules
        if not self.create_datasock():
            return
        if not path:
            path = self.cwd
        else:
            path = self.joinpath(self.cwd, path)
        perm = self.logged and permcheck(path, self.user, self.group, self, "list")
        if not perm:
            self.reply("550 Sorry")
            return
        if self.filesys.isdir(path):
            try:
                self.filesys.chdir(path)
                lp = self.filesys.listdir(path)
            except OSError:
                self.reply("550 I cannot")
                return
        else:
            lp = [path]
        r = map(lambda x: "%s\r\n" % x, lp)
        try:
            for i in r:
                self.sock.send(i)
        except socket.error:
            pass
        try:
            self.close_datasock()
        except socket.error:
            pass

        del r # to save memory
        self.reply("226 Wow, listing done")


    # parses the command and eventually calls the appropriate routine
    def docmd(self, cmd):
        debug("<--- "+repr(cmd))
        # if the connection has broken... we have to shut down:
        if cmd == "":
            raise "session_exit"
        # filter suspicious chars first
        cmd2 = filter(lambda x: ord(x) >= 32 and x not in "\377\364\362",cmd)
        lcmd2 = string.split(cmd2, None, 1) or [""]
        command = string.lower(lcmd2[0])
        if len(lcmd2) > 1:
            args = string.strip(lcmd2[1])
        else:
            args = "" # was None, but it was breaking some commands

        u = self.user or "-"
        ip = self.ip or "-"
        c = cmd2
        log.log(time.time(), u, ip, c, 0)
        if self.cmddict.has_key(command):
            self.curcmd = c
            if threading:
                while self.pendingconn and command<>"abor":
                    pass
            self.cmddict[command](args)
        else:
            self.reply("500 I'm gonna ignore this command... maybe later...")
        log.log(time.time(), u, ip, c, 1)

    def loop(self):
        while not self.exit_immediately:
            try:
                self.last_cmd_time = time.time()
                l = self.rfile.readline()
            except timeout_socket.Timeout:
                if self.pendingconn: 
                    # if there is an ongoing connection, do not timeout for commands
                    # there is a subtle race here - if data connection ends while readline()
                    # is near timeout, client will get 421 Timeout as soon as the data
                    # connections finishes, not having a chance to enter control
                    # commands. But there is not much to be done about it.
                    continue # continue because we do not want to do docmd(), when 
                             # readline() timeouted, l is an old value
                else:
                    try:
                        self.reply("421 timeout")
                        break
                    except (socket.error, timeout_socket.Timeout):
                        break
            except socket.error: # but if anythin happened with control connection, go out
                break
            try:
                self.docmd(l)
            except ("session_exit", socket.error):
                break
        try:
            self.close_datasock() # close any transfers
        except:
            pass
                
        debug("Connection closed.")



authmethods = []    
permmethods = []    
sessionmethods = []



for i in modules:
    exec("import "+i)
    methods = dir(eval(i))
    if "got_user" in methods: # it is authentification module
        authmethods.append( (eval(i+".got_user"), eval(i+".got_pass")) )
    if "permcheck" in methods: # permission module
        permmethods.append(eval(i+".permcheck"))
    if "FileObject" in methods:
        FileObject = eval(i+".FileObject")
    if "FileSystem" in methods:
        FileSystem = eval(i+".FileSystem")
    if "Session" in methods:
        sessionmethods.append(i+".Session")
    if "Log" in methods:
        Log = eval(i+".Log")

sessionmethods.append("BasicSession")

#this is ugly ugly UGLY
exec("class Session("+string.join(sessionmethods,",")+"):\n    pass\n")

#sd = {}
#Session = new.classobj("Session", tuple(sessionmethods), sd)

def permcheck(f, user, group, session, operation):
    last = 0
    for i in permmethods:
        l, c = i(f, user, group, session, operation)
        if l == 0:
            last = 0
        elif l == 1:
            last = 1
        if not c:
            break
    return last
        

def got_user(username, session, sessions): # session points to Session class
    last_deny_rt = 500, "", "", "", 0, 0 
    # response code, response message, user, group, deny_or_grant, continue
    last_grant_rt = 200, "", "", "", 0, 0
    last_rt = 500, "", "", "", 0, 0
    last = -1
    for i in authmethods:
        rt = n, r, u, g, l, c = i[0](username, session, sessions)
        if l == 0:
            last_deny_rt = rt
            last = 0
        elif l == 1:
            last_grant_rt = rt
            last = 1
        else:
            last_rt = rt
        if not c:
            break
    #now last is 1 for grant access, 0 for deny
    if last == 1:
        n, r, u, g, l, c = last_grant_rt
    elif last == 0:
        n, r, u, g, l, c = last_deny_rt
    else:
        n, r, u, g, l, c = last_rt
    return n, r, u, g, l

def got_pass(username, password, session, sessions):
    last_deny_rt = 500, "", 0, 0
    last_grant_rt = 200, "", 0, 0
    last_rt = 500, "", 0, 0
    last = 0
    for i in authmethods:
        rt = n, r, l, c = i[1](username, password, session, sessions)
        if l == 0:
            last_deny_rt = rt
            last = 0
        elif l == 1:
            last_grant_rt = rt
            last = 1
        else:
            last_rt = rt
        if not c:
            break
    #now last is 1 for grant access, 0 for deny
    if last == 1:
        n, r, l, c = last_grant_rt
    elif last == 0:
        n, r, l, c = last_deny_rt
    else:
        n, r, l, c = last_rt
    return n, r, l




def watchdog():
    while 1:
        time.sleep(2)
        cur_time = time.time()
        print sessions
        for i in range(len(sessions)):
            print sessions[i].ip
        print



# the main routine
# ----------------


class NoneClass:
    pass

class DummyLock:
    def acquire(self):
        pass
    def release(self):
        pass

try:
    import thread
    threading = 1
except:
    threading = 0

forking =  hasattr(os, "fork")

sessions = {}

t_socket = timeout_socket.timeout_socket

lastpid = 1L
if threading:
    thlock = thread.allocate_lock()
else:
    thlock = DummyLock()
#thread.start_new_thread(watchdog, ())

#test if we are running from inetd
inetd = 1
inetdsock = 0
try:
    inetdsock = socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_STREAM)
    inetdsock.getsockname()
except (socket.error, AttributeError):
    inetd = 0
    del inetdsock

log = Log()
log.openlog()

if inetd:
    client_addr = inetdsock.getpeername()
    session = Session(sys.stdin, sys.stdout, client_addr)
    pid = 1L
    session.pid = pid
    sessions[pid] = session
    session.loop()
    #thlock.acquire()
    if sessions.has_key(pid):
        del sessions[pid]
    #thlock.release()
    del session
    sys.exit(0)

if threading:
    mixin = SocketServer.ThreadingMixIn
elif forking:
    mixin = SocketServer.ForkingMixIn
else:
    mixin = NoneClass


class MyStreamRequestHandler(SocketServer.StreamRequestHandler):
    def finish(self):
        self.wfile.flush()
        self.wfile.close()
        self.rfile.close()
        self.request.close()

class TCPServer(mixin, SocketServer.TCPServer):
    def server_bind(self):
        """Called by constructor to bind the socket.
        """
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def get_request(self):
        """Get the request and client address from the socket.
        """
        conn, adr = self.socket.accept()
        conn = t_socket(sock=conn, timeout=timeout_session)
        return conn, adr


class FTPServer(MyStreamRequestHandler):
    def handle(self):
        global lastpid
        session = Session(self.rfile, self.wfile, self.client_address)
        thlock.acquire()
        pid = lastpid = lastpid+1
        thlock.release()
        session.pid = pid
        sessions[pid] = session
        session.loop()
        thlock.acquire()
        if sessions.has_key(pid):
            del sessions[pid]
        thlock.release()
        del session


address = ('', port)
server = TCPServer(address, FTPServer)

server.serve_forever()
