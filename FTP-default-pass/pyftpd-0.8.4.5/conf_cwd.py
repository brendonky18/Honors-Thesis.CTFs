#!/usr/bin/python

from utils import isdir, defaultdir
cwdlist = []
try:
    from cwd_config import *
except:
    pass

from Tkinter import *
import string, pprint, os, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

config_file = "cwd_config.py"

class App(TkinterConfigList.App):

    def askval(self, initval=("anonymous", defaultdir)):
        "ask for the user and path"
        u = tkSimpleDialog.askstring("username", "username", initialvalue=initval[0])
        if u == None:
            return None
        pd = FileDialog.FileDialog(master=self.frame, title="Initial working directory")
        path = pd.go(dir_or_file=initval[1])
        #path = tkSimpleDialog.askstring("initial cwd", "initial directory", initialvalue=initval[1])
        if path == None:
            return None
        if os.path.exists(path) and not isdir(path):
            path = os.path.dirname(path)
        return u, path


    def stringify(self, tup):
        return tup[0]+" : "+tup[1]

    def prepare_for_save(self):
        stream = StringIO.StringIO()
        pprint.pprint(self.list, stream)
        s = stream.getvalue()
        stream.close()
        return "cwdlist = "+s+"\n"
        

TkinterConfigList.go(Frame=App, title="configure cwd", list=cwdlist,
                default_config_file=config_file, hf="cwd_README.txt")
