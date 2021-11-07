#!/usr/bin/python

from utils import isdir
limitlist = []
try:
    from iplimit_config import *
except:
    pass

from Tkinter import *
import string, pprint, os, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

config_file = "iplimit_config.py"

class App(TkinterConfigList.App):

    def askval(self, initval=("anonymous", 1)):
        "ask for the user and value"
        u = tkSimpleDialog.askstring("username", "username", initialvalue=initval[0])
        if u == None:
            return None
        val = tkSimpleDialog.askinteger("limit", "Maximum number of connections from one IP number:", initialvalue=initval[1])
        if val == None:
            return None
        return u, val


    def stringify(self, tup):
        return tup[0]+" : "+str(tup[1])

    def prepare_for_save(self):
        stream = StringIO.StringIO()
        pprint.pprint(self.list, stream)
        s = stream.getvalue()
        stream.close()
        return "#user, max nr of connections from one ip\nlimitlist = "+s+"\n"

TkinterConfigList.go(Frame=App, title="configure limits", list=limitlist,
                default_config_file=config_file, hf="iplimit_README.txt")
