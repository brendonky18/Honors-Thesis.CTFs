MODULE NAME
    fs_url_module - access to URL

OPTIONS
    none

DESCRIPTION
    This module is an example of fs modules flexibility.
    It provides access to general URL naming scheme, e.g.
    you can do:
        get /http://www.playboy.com/babe.jpg
    from your ftp client, and pyftpd will fetch babe.jpg
    from www.playboy.com and tranfer it to your client
    as if it were an ordinary file.
    Leading / in URL schemes is necessary in order to persuade 
    some over-intelligent ftp clients that it is really a file.

    This module provides just bare minumum, no directory listing,
    no transfer resume, no error checking, no nothing.
    
SEE ALSO
    fs_curl_module
    