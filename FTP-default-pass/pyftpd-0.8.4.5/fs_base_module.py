class FileObject:

    def __init__(self, name, mode="r"):
        pass
        
    def close(self):
        pass
        
    def read(self, size=None):
        return ""

    def write(self, s):
        return 0

    def seek(self, offset, whence=0):
        return 0
        

class FileSystem:

    def __init__(self, session):
        pass

    def isdir(self, d):
        return 0

    def isfile(self, f):
        return 0

    def isexec(self, d):
        return 0

    def islink(self, d):
        return 0

    def readlink(self, d):
        return ""

    def chdir(self, p):
        return
        
    def stat(self, f):
        return 10*(0,)

    def listdir(self, p):
        return []

    def open(self, f, mode="r"):
        return FileObject(f, mode)

    def rmdir(self, d):
        return

    def mkdir(self, d):
        return

    def unlink(self, p):
        return

    def v2fs(self, v):
        return v
        
