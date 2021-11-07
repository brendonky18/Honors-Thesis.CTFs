#!/usr/bin/python

banlist = []
banmsg = "You are banned"
try:
    from ban_config import *
except:
    pass

from Tkinter import *
import string, pprint, os, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

config_file = "ban_config.py"

class App(TkinterConfigList.App):

    def askval(self, initval="256.257.258.259"):
        "ask for the ip number"
        u = tkSimpleDialog.askstring("IP number", "IP number:", initialvalue=initval)
        if u == None:
            return None
        return u

    def opt(self):
        global banmsg
        r = tkSimpleDialog.askstring("banmsg", "Message for the banned ones:", initialvalue=banmsg)
        if r:
            banmsg = r

    def stringify(self, entry):
        return entry

    def prepare_for_save(self):
        stream = StringIO.StringIO()
        pprint.pprint(self.list, stream)
        s = stream.getvalue()
        stream.close()
        return "# list of banned ip's \nbanlist = "+s+"\n"+ \
                "banmsg = "+repr(banmsg)+"\n"

TkinterConfigList.go(Frame=App, title="configure banlist", list=banlist,
                default_config_file=config_file, hf="ban_README.txt")
