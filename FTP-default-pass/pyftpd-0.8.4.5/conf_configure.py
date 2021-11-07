#!/usr/bin/python

from utils import isdir, defaultdir

initial_msg = "Welcome to pyftpd. Happy downloading"
do_debug = 0
sbufsize = 16000 # size of send buffer
rbufsize = 16000 # size of receive buffer
modules = ["auth_db_module", "auth_anonymous_module", "ban_module",
        "cwd_module", "limit_module", "fs_real_module", "iplimit_module",
        "perm_acl_module"]
timeout_data = 60 # timeout for data connection
timeout_session = 60 # timeout for control connection
initial_wd = defaultdir # initial working directory
port = 2121 # default port
try:
    from config import *
except:
    pass

from Tkinter import *
import string, pprint, os, os.path, StringIO
import tkSimpleDialog, tkMessageBox, tkFileDialog, FileDialog

import TkinterConfigList

config_file = "config.py"


class Opts(Toplevel):
    def __init__(self, parent=None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        self.title("set options")

        self.parent = parent

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        #self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)


    def body(self, master):

        self.frame = master
        self.bdo_debug = IntVar()
        self.bdo_debug.set(do_debug)
            
        self.do_debugb = Checkbutton(self.frame, 
                        text="Debug messages",
                        anchor=W,
                        variable=self.bdo_debug)
        self.do_debugb.grid(row=0, column=0, sticky=W)


        self.inimsgb = Button(self.frame, 
                        width=16,
                        relief=RIDGE,
                        cursor='hand2',
                        text="Initial message",
                        command=self.enterinimsg)
        self.inimsgb.grid(row=2, column=0, sticky=W)

        self.inimsgv = StringVar()
        self.inimsgv.set(initial_msg)
        self.inimsgbe = Label(self.frame,
                        textvariable=self.inimsgv,
                        #width=16,
                        #relief=RIDGE,
                        cursor='hand2')
        self.inimsgbe.grid(row=2, column=1, sticky=W)

        self.sbufb = Button(self.frame, 
                        width=16,
                        relief=RIDGE,
                        cursor='hand2',
                        text="Send buffer size",
                        command=self.entersbuf)
        self.sbufb.grid(row=4, column=0, sticky=W)

        self.sbufv = IntVar()
        self.sbufv.set(sbufsize)
        self.sbufbe = Label(self.frame,
                        textvariable=self.sbufv,
                        #width=16,
                        cursor='hand2')
        self.sbufbe.grid(row=4, column=1, sticky=W)


        self.rbufb = Button(self.frame, 
                        width=16,
                        relief=RIDGE,
                        cursor='hand2',
                        text="Receive buffer size",
                        command=self.enterrbuf)
        self.rbufb.grid(row=5, column=0, sticky=W)

        self.rbufv = IntVar()
        self.rbufv.set(rbufsize)
        self.rbufbe = Label(self.frame,
                        textvariable=self.rbufv,
                        #width=16,
                        cursor='hand2')
        self.rbufbe.grid(row=5, column=1, sticky=W)


        self.tdatab = Button(self.frame, 
                        width=16,
                        relief=RIDGE,
                        cursor='hand2',
                        text="Timeout data",
                        command=self.entertdata)
        self.tdatab.grid(row=6, column=0, sticky=W)

        self.tdatav = IntVar()
        self.tdatav.set(timeout_data)
        self.tdatabe = Label(self.frame,
                        textvariable=self.tdatav,
                        #width=16,
                        cursor='hand2')
        self.tdatabe.grid(row=6, column=1, sticky=W)

        self.tsessionb = Button(self.frame, 
                        width=16,
                        relief=RIDGE,
                        cursor='hand2',
                        text="Timeout session",
                        command=self.entertsession)
        self.tsessionb.grid(row=7, column=0, sticky=W)

        self.tsessionv = IntVar()
        self.tsessionv.set(timeout_session)
        self.tsessionbe = Label(self.frame,
                        textvariable=self.tsessionv,
                        #width=16,
                        cursor='hand2')
        self.tsessionbe.grid(row=7, column=1, sticky=W)

        self.iniwdb = Button(self.frame, 
                        width=16,
                        relief=RIDGE,
                        cursor='hand2',
                        text="Initial dir",
                        command=self.enteriniwd)
        self.iniwdb.grid(row=8, column=0, sticky=W)

        self.iniwdv = StringVar()
        self.iniwdv.set(initial_wd)
        self.iniwdbe = Label(self.frame,
                        textvariable=self.iniwdv,
                        #width=16,
                        #relief=RIDGE,
                        cursor='hand2')
        self.iniwdbe.grid(row=8, column=1, sticky=W)


        self.tportb = Button(self.frame, 
                        width=16,
                        relief=RIDGE,
                        cursor='hand2',
                        text="Port:",
                        command=self.enterport)
        self.tportb.grid(row=10, column=0, sticky=W)

        self.tportv = IntVar()
        self.tportv.set(port)
        self.tportbe = Label(self.frame,
                        textvariable=self.tportv,
                        #width=16,
                        cursor='hand2')
        self.tportbe.grid(row=10, column=1, sticky=W)

        self.aboutb = Button(self.frame, 
                        text="Help", 
                        width=16,
                        relief=GROOVE,
                        command=self.about)
        self.aboutb.grid(row=13, column=0, sticky=W)

        self.quitb = Button(self.frame, 
                        text="OK", 
                        width=7,
                        #cursor="pirate",
                        command=self.quit)
        self.quitb.grid(row=14, column=0, columnspan=2, sticky=W+E)



    def enterinimsg(self):
        global initial_msg
        m=tkSimpleDialog.askstring(
                title="initial msg", 
                prompt="Initial message:",
                initialvalue=initial_msg)
        if m <> None:
            initial_msg = m
            self.inimsgv.set(initial_msg)

    def enteriniwd(self):
        global initial_wd
        pd = FileDialog.FileDialog(master=self.frame, title="Initial working directory")
        m = pd.go(dir_or_file=initial_wd)
        if m <> None:
            if os.path.exists(m) and not isdir(m):
                m = os.path.dirname(m)
            initial_wd = m
            self.iniwdv.set(m)

    def entersbuf(self):
        global sbufsize
        m=tkSimpleDialog.askinteger(
                title="sbufsize", 
                prompt="Size of sending buffer [B]:",
                initialvalue=sbufsize)
        if m <> None:
            sbufsize = m
            self.sbufv.set(m)

    def enterrbuf(self):
        global rbufsize
        m=tkSimpleDialog.askinteger(
                title="sbufsize", 
                prompt="Size of receiving buffer [B]:",
                initialvalue=rbufsize)
        if m <> None:
            rbufsize = m
            self.rbufv.set(m)
        
    def entertdata(self):
        global timeout_data
        m=tkSimpleDialog.askinteger(
                title="timeout data", 
                prompt="Timeout for data connection [s]:",
                initialvalue=timeout_data)
        if m <> None:
            timeout_data = m
            self.tdatav.set(m)

    def entertsession(self):
        global timeout_session
        m=tkSimpleDialog.askinteger(
                title="timeout session", 
                prompt="Timeout for session connection [s]:",
                initialvalue=timeout_session)
        if m <> None:
            timeout_session = m
            self.tsessionv.set(m)

    def enterport(self):
        global port
        m=tkSimpleDialog.askinteger(
                title="port", 
                prompt="Port:",
                initialvalue=port)
        if m <> None:
            port = m
            self.tportv.set(m)

    def enterlogfile(self):
        global logfile
        "ask for the logfile"
        u = tkFileDialog.asksaveasfilename(defaultextension=".log", 
                filetypes=[("log files", "*.log")],
                initialfile="pyftpd.log"
                )
        if not u:
            return None
        logfile=u
        self.logfilev.set(u)

    def about(self):
        h = TkinterConfigList.HelpDialog(self.parent)

    def quit(self):
        global do_debug
        do_debug = self.bdo_debug.get()
        self.parent.focus_set()
        self.destroy()


class App(TkinterConfigList.App):

    def askval(self, initval="auth_dummy"):
        "ask for the module"
        u = tkFileDialog.askopenfilename(defaultextension=".py", 
                filetypes=[("modules", "*_module.py")],
                initialdir="."
                )
        if not u:
            return None
        u = os.path.splitext(os.path.split(u)[1])[0]
        return u

    def opt(self):
        #root=Toplevel(self.frame, bd=2, relief=RAISED)
        opts = Opts(self.frame)
        #opts.title("pyftpd options")
        #root.mainloop()
        return

    def stringify(self, entry):
        return entry

    def prepare_for_save(self):
        stream = StringIO.StringIO()
        pprint.pprint(self.list, stream)
        s = stream.getvalue()
        stream.close()
        return """
initial_msg = %s
do_debug = %i
sbufsize = %i # size of send buffer
rbufsize = %i # size of receive buffer
modules = %s
timeout_data = %i # timeout for data connection
timeout_session = %i # timeout for control connection
initial_wd = %s # initial working directory
port = %i # default port
""" % (repr(initial_msg), do_debug, sbufsize, rbufsize, s,
       timeout_data, timeout_session,
       repr(initial_wd), port)

    def quit(self):
        if tkMessageBox.askyesno("Save", "Save changes?"):
            self.save()
        self.frame.quit()

     
TkinterConfigList.go(Frame=App, title="configure pyftpd", list=modules,
                default_config_file=config_file, hf="configure_README.txt")
