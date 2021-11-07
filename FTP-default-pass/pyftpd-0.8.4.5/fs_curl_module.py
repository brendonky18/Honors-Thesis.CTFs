import ftplib, os, posixpath
import fs_base_module

class FileObject(fs_base_module.FileObject):

    def __init__(self, name, mode="r"):
        self.name = name[1:]
        self.fo = os.popen("curl -s %s" % self.name)
        
    def close(self):
        self.fo.close()
        
    def read(self, size=None):
        if size==None:
            return self.fo.read()
        else:
            return self.fo.read(size)

    def write(self, s):
        return 0

    def seek(self, offset, whence=0):
        self.fo.close()
        assert whence == 0
        self.fo = os.popen("curl -s -C %i %s" % (offset, self.name))
        
        

class FileSystem(fs_base_module.FileSystem):

    def __init__(self, session):
        global ftp
        self.pardir = ".."

    def isdir(self, d):
        return 0

    def islink(self, d):
        return 0

    def isfile(self, f):
        return 1

    def readlink(self, d):
        return ""

    def isexec(self, d):
        return 1

    def chdir(self, p):
        return 0
        
    def stat(self, f):
        return 10*(0,)

    def listdir(self, p):
        return []

    def open(self, f, mode="r"):
        return FileObject(self.v2fs(f), mode)

    def rmdir(self, d):
        return 0

    def mkdir(self, d):
        return 0

    def unlink(self, p):
        return 0


class Session:
    def cmd_size(self, f):
        self.reply("500 Not available here")
                    