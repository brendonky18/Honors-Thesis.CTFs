import os, sys
import utils, string

import fs_base_module

class FileObject(fs_base_module.FileObject):

    def __init__(self, name, mode="r"):
        #check if name is valid filename
        self.fo = open(name, mode)
        
    def close(self):
        self.fo.close()
        
    def read(self, size=None):
        if size==None:
            return self.fo.read()
        else:
            return self.fo.read(size)

    def write(self, s):
        return self.fo.write(s)

    def seek(self, offset, whence=0):
        return self.fo.seek(offset, whence)
        

class FileSystem(fs_base_module.FileSystem):

    def isdir(self, f):
        return utils.isdir(self.v2fs(f))

    def isfile(self, f):
        return os.path.isfile(self.v2fs(f))

    def isexec(self, f):
        return utils.isexec(self.v2fs(f))

    def islink(self, f):
        return os.path.islink(self.v2fs(f))

    def readlink(self, f):
        return os.readlink(self.v2fs(f))

    def chdir(self, f):
        return os.chdir(self.v2fs(f))
        
    def stat(self, f):
        return os.stat(self.v2fs(f))

    def listdir(self, f):
        return os.listdir(self.v2fs(f))

    def open(self, f, mode="r"):
        return FileObject(self.v2fs(f), mode)

    def rmdir(self, f):
        return os.rmdir(self.v2fs(f))

    def mkdir(self, f):
        return os.mkdir(self.v2fs(f))

    def unlink(self, f):
        return os.unlink(self.v2fs(f))

    if sys.platform[:3] == 'win':
        def v2fs(self, v):
            print 'fasz', `v`
            if v[2] == ":" and v[1] in string.letters:
                return os.path.normpath(v[1:])
            else:
                return "" # should not happen
    else:
        def v2fs(self, v):
            return os.path.normpath(v)
        
