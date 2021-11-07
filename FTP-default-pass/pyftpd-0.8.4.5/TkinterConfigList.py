#!/usr/bin/python

from Tkinter import *
import string
import tkSimpleDialog, tkMessageBox, tkFileDialog, ScrolledText

class HelpDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        global helpfile # ugly
        text = ScrolledText.ScrolledText(master)
        text.pack({'expand': 1, 'fill': 'both'}) # Expand into available space
        for i in open(helpfile, "r").readlines():
            text.insert('end', i)

class App(Frame):
    def __init__(self, master=None, list=[], default_config_file="generic_config.py", 
                 hf="generic_README.txt"):
        global helpfile
        self.master = master
        helpfile = hf
        self.default_config_file=default_config_file
        self.list=list # list of tuples (user, cwd)
        self.frame=Frame(master)
        self.frame.pack()

        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.listbox = Listbox(self.frame, width=35, yscrollcommand=scrollbar.set)
        self.listbox.bind("<Double-Button-1>", self.edit)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=LEFT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        for i in self.list:
            self.listbox.insert(END, self.stringify(i))

        self.optb = Button(self.frame, 
                        text="Options",
                        width=7,
                        command=self.opt)
        self.optb.pack(side=TOP)

        self.saveb = Button(self.frame, 
                        text="Save", 
                        width=7,
                        command=self.save)
        self.saveb.pack(side=TOP)

        self.saveasb = Button(self.frame, 
                        text="Save As", 
                        width=7,
                        command=self.saveas)
        self.saveasb.pack(side=TOP)


        self.addb = Button(self.frame, 
                        text="Add", 
                        width=7,
                        command=self.add)
        self.addb.pack(side=TOP)

        self.copyb = Button(self.frame, 
                        text="Copy", 
                        width=7,
                        command=self.copy)
        self.copyb.pack(side=TOP)

        self.delb = Button(self.frame, 
                        text="Delete", 
                        width=7,
                        command=self.delete)
        self.delb.pack(side=TOP)

        self.editb = Button(self.frame, 
                        text="Edit", 
                        width=7,
                        command=self.edit)
        self.editb.pack(side=TOP)

        self.quitb = Button(self.frame, 
                        text="Quit", 
                        width=7,
                        cursor="pirate",
                        command=self.quit)
        self.quitb.pack(side=BOTTOM)

        self.helpb = Button(self.frame, 
                        text="Help", 
                        width=7,
                        relief=GROOVE,
                        command=self.help)
        self.helpb.pack(side=BOTTOM)

    def opt(self):
        """to be overriden
        set different options"""

    def askval(self, initval="default"):
        """to be overriden
        ask for one entry"""
        u = tkSimpleDialog.askstring("entry", "entry:", initialvalue=initval)
        return u


    def stringify(self, entry):
        """to be overriden
        change list entry to string for displaying"""
        return str(entry)
        

    def getpos(self):
        csel = self.listbox.curselection()
        if csel <> ():
            return int(csel[0])
        else:
            return None

    def delete(self):
        pos = self.getpos()
        if pos <> None:
            self.list = self.list[:pos]+self.list[pos+1:]
            self.listbox.delete(ACTIVE)

    def prepare_for_save(self):
        """to be overriden
        return asciified representation for saving"""
        return "list = " + repr(self.list)

    def save(self):
        self.do_save(fname=self.default_config_file)

    def do_save(self, fname):
        if fname:
            f = open(fname, "w")
            f.write(self.prepare_for_save())
            f.write("\n")
            f.close()

    def saveas(self):
        fname = tkFileDialog.asksaveasfilename(initialfile=self.default_config_file,
                                            title="Save as",
                                            filetypes=[("configuration files","*_config.py")])
        if fname:
            self.save(fname)

    def add(self):
        dr = self.askval()
        if dr <> None:
            self.list.append(dr)
            self.listbox.insert(END, self.stringify(dr))

    def copy(self):
        pos = self.getpos()
        if pos <> None:
            self.list.append(self.list[pos])
            self.listbox.insert(END, self.stringify(self.list[pos]))

    def edit(self, event=None):
        pos = self.getpos()
        if pos <> None:
            dr = self.askval(initval = self.list[pos])
            if dr <> None:
                self.list[pos] = dr
                self.listbox.delete(pos)
                self.listbox.insert(pos, self.stringify(self.list[pos]))

    def about(self):
        tkMessageBox.showinfo("About pyftpd", "pyftpd"
                    + "\n\nby Radovan Garabik")

    def help(self):
        h = HelpDialog(self.master)

    def quit(self):
        if tkMessageBox.askyesno("Save", "Save changes?"):
            self.save()
        self.frame.quit()

def go(Frame, title="configure generic", list=[], 
       default_config_file="generic_config.py",
       hf="generic_README.txt"):
    root = Tk()
    app = Frame(root, list, default_config_file, hf)
    root.title(title)
    root.mainloop()
