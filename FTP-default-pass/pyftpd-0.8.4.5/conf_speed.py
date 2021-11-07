#!/usr/bin/python

from utils import isdir, defaultdir
speedlist = []
try:
    from speed_config import *
except:
    pass

from Tkinter import *
import string, pprint, os, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

config_file = "speed_config.py"

class App(TkinterConfigList.App):

    def askval(self, initval=("anonymous", 0., 0.)):
        "ask for the user and path"
        u = tkSimpleDialog.askstring("username", "username", initialvalue=initval[0])
        if u == None:
            return None
        rs = tkSimpleDialog.askfloat("RETR limit [B/s]", "RETR limit [B/s].", initialvalue=initval[1])
        if rs == None:
            return None
        ss = tkSimpleDialog.askfloat("STOR limit [B/s]", "STOR limit [B/s].", initialvalue=initval[2])
        if ss == None:
            return None
        return u, rs, ss


    def stringify(self, tup):
        return "%s : %.5g, %.5g" % tup

    def prepare_for_save(self):
        stream = StringIO.StringIO()
        pprint.pprint(self.list, stream)
        s = stream.getvalue()
        stream.close()
        return "speedlist = "+s+"\n"
        

TkinterConfigList.go(Frame=App, title="configure speed limit", list=speedlist,
                default_config_file=config_file, hf="speed_README.txt")
