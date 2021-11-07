from fs_chroot_config import *

from utils import myfnmatch
import os

exec("from "+slave_fs+" import *")

slaveFileObject = FileObject
slaveFileSystem = FileSystem


class FileObject(slaveFileObject):
    pass
    

class FileSystem(slaveFileSystem):

    def __init__(self, session):
        self.slavefs = slaveFileSystem(session)
        global chrootdir
        self.chrootdir = ""
        for i in chrootlist:
            if myfnmatch(session.user, i[0]):
                self.chrootdir = i[1]

    def v2fs(self, f):
        r = self.slavefs.v2fs(self.chrootdir+f)
        return r

    def readlink(self, d):
        return "" # because the link points to real file.. ugh
        
