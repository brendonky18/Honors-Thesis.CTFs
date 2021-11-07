#!/usr/bin/python

from utils import isdir
passwd = []
try:
    from auth_db_config import *
except:
    pass

from auth_db_module import md5hash

import Tkinter
from Tkinter import *
import string, pprint, os, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

class _QueryDialog(tkSimpleDialog._QueryDialog):
    def body(self, master):

        w = Label(master, text=self.prompt, justify=LEFT)
        w.grid(row=0, padx=5, sticky=W)

        self.entry = Entry(master, name="entry", show="*")
        self.entry.grid(row=1, padx=5, sticky=W+E)

        if self.initialvalue:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, END)

        return self.entry

class _QueryString(_QueryDialog):
    def getresult(self):
        return self.entry.get()

def askpass(title, prompt, **kw):
    d = apply(_QueryString, (title, prompt), kw)
    return d.result


    
config_file = "auth_db_config.py"

class App(TkinterConfigList.App):

    def askval(self, initval=("user", "users", "")):
        "ask for the user, group and password"
        u = tkSimpleDialog.askstring("username", "username", initialvalue=initval[0])
        if u == None:
            return None
        g = tkSimpleDialog.askstring("group", "group", initialvalue=initval[1])
        if g == None:
            return None
        p = askpass("password", "password", initialvalue="")
        if p == None:
            return None
        return u, g, md5hash(p)


    def stringify(self, tup):
        return tup[0]+":"+tup[1]+":x"

    def prepare_for_save(self):
        stream = StringIO.StringIO()
        pprint.pprint(self.list, stream)
        s = stream.getvalue()
        stream.close()
        return "passwd = "+s+"\n"

TkinterConfigList.go(Frame=App, title="configure users", list=passwd,
                default_config_file=config_file, hf="auth_db_README.txt")
