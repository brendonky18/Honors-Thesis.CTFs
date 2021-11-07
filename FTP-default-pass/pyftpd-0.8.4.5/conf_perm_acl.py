#!/usr/bin/python

from utils import isdir
acllist = []
try:
    from perm_acl_config import *
except:
    pass

from Tkinter import *
import string, pprint, os, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

config_file = "perm_acl_config.py"

class PermDialog(tkSimpleDialog.Dialog):

    def __init__(self, parent, title = None, initval=("", "", "", "", [], [])):

        self.initval = initval

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        Label(master, text="User:").grid(row=0, sticky=W)
        Label(master, text="Group:").grid(row=1, sticky=W)
        Label(master, text="From IP:").grid(row=2, sticky=W)

        self.euser = Entry(master, width=20)
        self.egroup = Entry(master, width=20)
        self.eip = Entry(master, width=20)

        self.euser.insert(0,self.initval[0])
        self.egroup.insert(0,self.initval[1])
        self.eip.insert(0,self.initval[2])

        self.euser.grid(row=0, column=1, columnspan=3, sticky=W)
        self.egroup.grid(row=1, column=1, columnspan=3, sticky=W)
        self.eip.grid(row=2, column=1, columnspan=3, sticky=W)


        self.pathb = Button(master, 
                        text="path:", 
                        relief=FLAT,
                        command=self.pickpath)
        self.pathb.grid(row=3, sticky=W)

        self.pathv = StringVar()
        self.pathv.set(self.initval[3])
        self.epathb = Button(master, 
                        textvariable=self.pathv,
                        #relief=FLAT,
                        command=self.pickpath)
        self.epathb.grid(row=3, column=1, columnspan=4, sticky=W)


        Label(master, text="Allow these commands:").grid(row=4, sticky=W, columnspan=4)
        
        LIST = ["cwd", "list", "nlst"]
        GET = ["retr", "size", "mdtm"]
        READ = LIST+GET
        self.READ=READ

        PUT = ["stor", "appe", "mkd"]
        DELETE = ["dele", "rmd"]
        
        WRITE = PUT+DELETE
        self.WRITE=WRITE
        ALL = READ+WRITE+["site"]
        self.ALL=ALL
        

        keys = ALL
        self.allowed = {}
        for i in range(len(keys)):
            v = IntVar()
            c = Checkbutton(master,
                            text=keys[i],
                            anchor=W,
                            variable=v,
                            indicatoron=1)
            c.grid(row=i/4+6, column=i%4, sticky=W)
            v.set(keys[i] in self.initval[4])
            self.allowed[keys[i]] = c, v

        lastrow = len(keys)/4+7

        self.bra = Button(master,
                   text="READ",
                   command=self.setREADallowed
                   )
        self.bra.grid(row=lastrow, column=0)

        self.bwa = Button(master,
                   text="WRITE",
                   command=self.setWRITEallowed
                   )
        self.bwa.grid(row=lastrow, column=1)

        self.bca = Button(master,
                   text="CLEAR",
                   command=self.setCLEARallowed
                   )
        self.bca.grid(row=lastrow, column=2)

        lastrow = lastrow+1
        Label(master, text="----").grid(row=lastrow, sticky=W)
        lastrow = lastrow+1
        Label(master, text="Deny these commands:").grid(row=lastrow, sticky=W, columnspan=4)


        self.denied = {}
        for i in range(len(keys)):
            v = IntVar()
            c = Checkbutton(master,
                            text=keys[i],
                            anchor=W,
                            variable=v)
            c.grid(row=i/4+lastrow+1, column=i%4, sticky=W)
            v.set(keys[i] in self.initval[5])
            self.denied[keys[i]] = c, v

        lastrow = len(keys)/4+lastrow+1

        self.brd = Button(master,
                   text="READ",
                   command=self.setREADdenied
                   )
        self.brd.grid(row=lastrow, column=0)

        self.bwd = Button(master,
                   text="WRITE",
                   command=self.setWRITEdenied
                   )
        self.bwd.grid(row=lastrow, column=1)

        self.bcd = Button(master,
                   text="CLEAR",
                   command=self.setCLEARdenied
                   )
        self.bcd.grid(row=lastrow, column=2)

    def setREADallowed(self):
        for i in self.READ:
            self.allowed[i][1].set(1)

    def setWRITEallowed(self):
        for i in self.WRITE:
            self.allowed[i][1].set(1)

    def setCLEARallowed(self):
        for i in self.ALL:
            self.allowed[i][1].set(0)

    def setREADdenied(self):
        for i in self.READ:
            self.denied[i][1].set(1)

    def setWRITEdenied(self):
        for i in self.WRITE:
            self.denied[i][1].set(1)

    def setCLEARdenied(self):
        for i in self.ALL:
            self.denied[i][1].set(0)


    def validate(self):
        allowed = []
        for i in self.allowed.keys():
            if self.allowed[i][1].get():
                allowed.append(i)
        denied = []
        for i in self.denied.keys():
            if self.denied[i][1].get():
                denied.append(i)
        self.result = (self.euser.get(), self.egroup.get(), self.eip.get(), 
                       self.pathv.get(), allowed, denied)
        return 1
        
    def pickpath(self):
        pd = FileDialog.FileDialog(self.parent, title="Path")
        path = pd.go(dir_or_file="")
        if path:
            self.pathv.set(path)


class App(TkinterConfigList.App):

    def askval(self, initval=("*", "*", "*", "/", [], [])):
        d = PermDialog(self.frame,
                    title="permissions",
                    initval=initval)
        allowed = []
        for i in d.allowed.keys():
            if d.allowed[i][1].get():
                allowed.append(i)
        denied = []
        for i in d.denied.keys():
            if d.denied[i][1].get():
                denied.append(i)
        return d.result
    
    def stringify(self, tup):
        return tup[0]+":"+tup[1]+":"+tup[2]+":"+tup[3]

    def prepare_for_save(self):
        stream = StringIO.StringIO()
        pprint.pprint(self.list, stream)
        s = stream.getvalue()
        stream.close()
        return """
LIST = [ "cwd", "list", "nlst"]
GET = ["retr", "size", "mdtm"]
READ = LIST+GET

PUT = ["stor", "appe", "mkd"]
DELETE = ["dele", "rmd"]
WRITE = PUT+DELETE
ALL = READ+WRITE+["site"]

acllist = %s\n
""" % s

TkinterConfigList.go(Frame=App, title="configure access", list=acllist,
                default_config_file=config_file, hf="perm_acl_README.txt")
