""" Sockets with timeouts.

Defines a "timeout_socket" class for connections that can potentially
cause the server to hang.  It uses select, and is based on code originally
from Scott Cotton.

The following people have contributed to the development of this module:

        Scott Cotton <scott@chronis.pobox.com>
        Lloyd Zusman <ljz@asfast.com
        Phil Mayes <pmayes@olivebr.com>
        Piers Lauder <piers@cs.su.oz.au>

Here are examples using smtplib.py and poplib.py by inheriting:

class timeout_POP3(poplib.POP3):
    def __init__(self, host, port = poplib.POP3_PORT):
        self.host = host
        self.port = port
        self.sock = timeout_socket.timeout_socket()
        self.sock.connect(self.host, self.port)
        self.file = self.sock.makefile('rb') # same as poplib.POP3
        self._debugging = 0
        self.welcome = self._getresp()

class timeout_SMTP(smtplib.SMTP):
    def connect(self, host='localhost', port = 0):
        '''Connect to a host on a given port.
        Override the std SMTP connect in order to use a timeout_socket.
        '''
        if not port:
            i = string.find(host, ':')
            if i >= 0:
                host, port = host[:i], host[i+1:]
                try: port = string.atoi(port)
                except string.atoi_error:
                    raise socket.error, "nonnumeric port"
        if not port: port = smtplib.SMTP_PORT
        self.sock = timeout_socket.timeout_socket()
        if self.debuglevel > 0: print 'connect:', (host, port)
        self.sock.connect(host, port)
        (code,msg)=self.getreply()
        if self.debuglevel >0 : print "connect:", msg
        return (code,msg)

This allows one to use poplib.py & smtplib.py unchanged.
"""

__version__ = "1.7"
__author__ = "Scott Cotton <scott@chronis.pobox.com>"


import socket
import errno
import select
import string
_TIMEOUT = 20.0

class Timeout(Exception):
    pass

class timeout_socket:

    """ Instantiate with:

                timeout_socket(timeout=20, sock=None)

        where `timeout' is the desired timeout in seconds (default 20),
        and `sock' is a pre-existing socket (default: one is created).
    """

    def __init__(self, timeout=_TIMEOUT, sock=None):
        self.ndups = 0
        self.timeout(timeout)
        self.inbuf = ''
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s = sock
        self.ndups = 1
        self.s.setblocking(0)

    # destructor notes: socket.socket will close when destroyed

    def __getattr__(self, name):
         return getattr(self.s, name)   # Other socket methods

    def accept(self):
        timeout = self._timeout
        s = self.s
        try:
            # Non-blocking mode
            s.setblocking(1)
            sa = s.accept()
            s.setblocking(timeout != 0)
            return sa
        except socket.error,why:
            if not timeout:
                raise
            s.setblocking(1)
            # The exception arguments can be (string) or (int,string)
            if len(why.args) == 1:
                code = 0
            else:
                code,why = why
            if code not in (errno.EAGAIN, errno.EWOULDBLOCK):
                raise
            # Ok, then wait...
            r,w,e = select.select([s],[],[],timeout)
            if r:
                try:
                    sa = s.accept()
                    return sa
                except socket.error,why:
                    # This can throw string or (int,string)
                    if len(why.args) == 1:
                        code = 0
                    else:
                        code,why = why
                    raise

        msg = 'accept timed out after %s seconds' % self._timeout
        raise Timeout(msg)

    def connect(self, *addr):
        timeout = self._timeout
        s = self.s
        try:
            # Non-blocking mode
            s.setblocking(0)
            apply(s.connect, addr)
            s.setblocking(timeout != 0)
            return 1
        except socket.error,why:
            if not timeout:
                raise
            s.setblocking(1)
            # The exception arguments can be (string) or (int,string)
            if len(why.args) == 1:
                code = 0
            else:
                code,why = why
            if code not in (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK): # WSAEWOULDBLOCK
                raise
            # Ok, then wait...
            r,w,e = select.select([],[s],[],timeout)
            if w:
                try:
                    apply(s.connect, addr)
                    return 1
                except socket.error,why:
                    # This can throw string or (int,string)
                    if len(why.args) == 1:
                        code = 0
                    else:
                        code,why = why
                    if code == errno.EISCONN:
                        return 1
                    raise

        msg = 'connect to %s timed out after %s seconds' % (str(addr), self._timeout)
        raise Timeout(msg)

    def send(self, data, flags=0):
        next = 0
        t = self._timeout
        total = len(data)
        while 1:
            try:
                r,w,e = select.select([],[self.s], [], t)
            except ValueError:
                raise Timeout("valueerror in select")
            if w:
                buf = data[next:next+8192]
                sent = self.s.send(buf, flags)
                next = next + sent
                if next == total:
                    return
            else:
                raise Timeout('timeout while sending "%.20s...": %d sec' % (data, t))

    def recv(self, amt, flags=0):
        r,w,e = select.select([self.s], [], [], self._timeout)
        if r:
            recvd = self.s.recv(amt, flags)
            return recvd
        raise Timeout("timeout while receiving from %s: %d sec" % (`self.s.getpeername()`, self._timeout))

    def makefile(self, flags="r", buffsize=-1):
        # makefile needs parameters
        # Just return ourself - watch out for multiple close(), and
        # provide read and readline methods expected by makefile result below.
        self.ndups = self.ndups+1 # nubmer or dupped descriptors
        return self


    def close(self):
        #if self.s.fileno() >= 0:
        self.ndups = self.ndups-1
        #print self.ndups
        if self.ndups == 0:
            #print "closing", self.s
            self.s.close()

    # New (non-standard socket) methods to support `makefile'.

    def read(self, amt):
        """ This only returns when amt has been read or socket times out """
        while len(self.inbuf) < amt:
            self.inbuf = self.inbuf + self.recv(4096)
        data = self.inbuf[:amt]
        self.inbuf = self.inbuf[amt:]
        return data

    def readline(self):
        """ readine for socket - buffers data """
        # Much slower than built-in method!
        while 1:
            lf = string.find(self.inbuf, '\n')
            if lf >= 0:
                break
            r = self.recv(4096)
            if not r: 
                # connection broken
                # without this readline would enter infinite loop
                break
            self.inbuf = self.inbuf + r
        lf = lf + 1
        data = self.inbuf[:lf]
        self.inbuf = self.inbuf[lf:]
        return data


    # Other new methods

    def recvpending(self, timeout=0):
        """ returns 1/0 """
        return [] != select.select([self.s], [], [], int(timeout) or self._timeout)[0]

    def timeout(self, newtimo):
        """ change socket timeout """
        self._timeout = int(newtimo)

    def flush(self):
        # TCPServer needs this
        pass

    def write(self, data):
        self.send(data)

