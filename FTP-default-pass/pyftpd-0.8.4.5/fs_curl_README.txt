MODULE NAME
    fs_curl_module - access to URL via curl program

OPTIONS
    none

DESCRIPTION
    This module is an example of fs modules flexibility.
    It provides access to general URL naming scheme, e.g.
    you can do:
        get /http://www.sex.com/teen.jpg
    from your ftp client, and pyftpd will fetch teen.jpg
    from www.sex.com and tranfer it to your client
    as if it were an ordinary file.
    Leading / in URL schemes is necessary in order to persuade 
    some over-intelligent ftp clients that it is really a file.

    Unlike fs_url_module, this module uses external program
    curl (http://curl.haxx.se/) to fetch files, and can resume 
    transfers, as long as curl can do it.
    
SEE ALSO
    fs_url_module
    