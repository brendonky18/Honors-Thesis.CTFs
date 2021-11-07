#!/usr/bin/python

from utils import isdir
limitlist = []
try:
    from limit_config import *
except:
    pass

from Tkinter import *
import string, pprint, os, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

config_file = "limit_config.py"

class App(TkinterConfigList.App):

    def askval(self, initval=("anonymous", 10)):
        "ask for the user and path"
        u = tkSimpleDialog.askstring("username", "username", initialvalue=initval[0])
        if u == None:
            return None
        val = tkSimpleDialog.askinteger("limit", "Maximum number of connections:", initialvalue=initval[1])
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
        return "limitlist = "+s+"\n"

TkinterConfigList.go(Frame=App, title="configure limits", list=limitlist,
                default_config_file=config_file, hf="limit_README.txt")
