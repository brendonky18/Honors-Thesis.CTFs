MODULE NAME
    limit_module - limit maximum numbers of connections for users

OPTIONS
    none

DESCRIPTION
    Configure list of users, corresponding number of maximum number of
    users connected simultaneously.
    You can use * to match all users, or as mask, e.g. ab* matches all users
    beginning with ab. Order is important, first use most general patterns, 
    then specific ones (in other words, put limit for * (all users) at the 
    first line)
    Unlike iplimit_module, this module limits the total number of logged 
    in users.

SEE ALSO
    iplimit_module
    