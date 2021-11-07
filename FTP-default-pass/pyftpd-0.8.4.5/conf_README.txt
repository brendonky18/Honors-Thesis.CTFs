NAME
    conf_configure.py - global pyftpd configuration
    
OPTIONS
    Debug messages - if this option is selected, all the 
        communication betweed clients and server is
        logged, using syslog(3) if available, or standard output
        if not.
        
    Initial message - welcome message to be displayed when client
        connects to the server.

    Send/Recieve buffer size - size of network buffer used when
        sendding/receiving files. The bigger it is, the better
        performance, but it takes that much memory for one
        connections. If you are on LAN, use value a bit smaller than
        you network card buffer (to accomodate for the size of
        TCP/IP and ethernet headers)
        
    Timeout data - the maximum time in seconds a data connection 
        can stall for before it is terminated.

    Timeout session - the maximum time in seconds a control 
        connection can take. In other words, if client is idle 
        for this time, it is disconnected (up- or down-loading a 
        file does not count as being idle)
                
    Initial dir - initial directory when users log in. This option
        is overriden if you use auth_cwd_module. This is 
        virtual directory, e.g. use posix-like path even on
        Windows if you turn on posix emulation.
        
    Port - no comment
    
    Emulate posix - on Windows, paths have form drive:\path\file, 
        e.g. c:\temp\file.ext
        This can be confusing to some ftp clients, so you if you
        turn this option on, visible paths will look like
        /drive:/path/file, e.g. /c:/temp/file.ext
        If you change this option, be sure to change directories
        in auth_cwd_module and Initial dir above to appropriate
        forms. Paths in perm_acl_module are always real filesystem
        paths and are not affected by this.
        This has no effect on UNIX machines, since those are
        posix anyway.
        
    
DESCRIPTION
    Configure list of pluggable modules. See relevant *_README.txt files
    for each module, and run configure_*.py for each module, or edit
    *_config.py configuration file. Include authentification and permition
    modules.
    Permission modules - modules responsible for deciding which users
        have access to which files. Use perm_dummy_module to allow
        everybody everything, or perm_acl_module for 
        sophisticated access control list.
    