MODULE NAME
    iplimit_module - limit maximum numbers of connections from
    one IP number.

OPTIONS
    none

DESCRIPTION
    Configure list of users, corresponding number of maximum connections
    they are allowed to make from one IP number (which means from one
    computer, if it were not for firewalls and ftp-proxies :-))
    You can use * to match all users, or as mask, e.g. ab* matches all users
    beginning with ab. Order is important, first use most general patterns, 
    then specific ones (in other words, put limit for * (all users) at the 
    first line)
    Unlike limit_module, this module does not limit the total number
    of users.

SEE ALSO
    limit_module
        