import os, os.path, fnmatch, sys, string

emulate_posix=0

if sys.platform[:3] == 'win':
    import posixpath
    myfnmatch = fnmatch.fnmatch
    defaultdir = "c:\\"
    def isdir(path): # kludge to recognize single drive letters as directory
        # path is already real fs path
        return os.path.isdir(path) or (len(path)==2 and path[1]==':' and path[0] in string.letters)
    def isexec(path): # see if path is executable
        return ( isdir(path) or 
                 (os.path.splitext(string.lower(path))[1] in (".exe", ".com", ".bat"))
                )
                
else:
    myfnmatch = fnmatch.fnmatchcase
    defaultdir = "/"
    isdir = os.path.isdir
    def isexec(path):
        try:
            r = os.access(path, 1)
        except:
            try:
                r = isdir(path)
            except:
                r = 0
        return r
        
