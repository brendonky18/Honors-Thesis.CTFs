import string, os
from stat import *
import time
import mp3infor 

def format_size(s):
    power = 1024
    if s == 0:
        return "0"
    units = ["KB", "MB", "GB", "TB"]
    r = `s` + "B"
    for i in range(len(units)):
        if s/power > 9:
            s = s/power
            r = `s` + units[i]
    return r

def format_seconds(sec):
    sec = long(sec)
    h = sec/3600
    m = (sec%3600)/60
    s = sec%60
    if h:
        return "%ih%im%is" % (h, m, s)
    elif m:
        return "%im%is" % (m, s)
    else:
        return "%ss" % s



def mp3info(file):
     try:
         mp3 = mp3infor.open_mp3(file)
     except IOError:
         return ""
     try:
         mp3.sync_read_header(0, 500)
         version = mp3.get_mpeg_version()
         layer = mp3.get_layer()
         protection_bit = mp3.get_protection()
         bitrate = mp3.get_bitrate()
         frequency = mp3.get_frequency()
         ch_mode = mp3.get_channel_mode()
         copyright  = mp3.get_copyright()
         original_bit = mp3.get_original()
         seconds, minutes, seconds_remain = mp3.get_length()
         frame = mp3.get_framelength()
         s = "%5sHz %6s" % (frequency, format_seconds(seconds))
     except mp3infor.NoHeaderError:
         s = ""
     return s


class Session:
    def cmd_list(self, path):

        if not self.create_datasock():
            return
        if not path:
            path = self.cwd
            
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
        print "fasz", `path`
        if isf:
            lp = [path]
        elif isd:
            try:
                self.filesys.chdir(path)
                cwd = path
                lp = self.filesys.listdir(path)
            except OSError:
                self.reply("550 I cannot")
                return
        else:
            self.reply("550 Uh, what?")
            return
        r = []
        for l in lp:
            i = self.joinpath(cwd, l)
            try:
                appendix = ""
                s = ""
                ft = "?"
                if self.filesys.islink(i):
                    dirflag = "l"
                    appendix = " -> "+self.filesys.readlink(i)
                    ft = "link"
                elif self.filesys.isdir(i):
                    dirflag = "d"
                    ft = "directory"
                else:
                    dirflag = "-"
                    s = mp3info(i)
                    if s:
                        ft = "MP3 file"
                    else:
                        ft = "file"
                status = self.filesys.stat(i)
                size = status[ST_SIZE]
                t = status[ST_CTIME]
                if t == -1:
                    t = 0
                ctime = time.strftime("%b %d",time.gmtime(t))
                rl = "%s %10s %s %7s %s %s%s\r\n" % \
                     (dirflag, ft, s ,format_size(size), ctime, l, appendix)
                r.append(rl)
            except OSError:
                pass
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

        