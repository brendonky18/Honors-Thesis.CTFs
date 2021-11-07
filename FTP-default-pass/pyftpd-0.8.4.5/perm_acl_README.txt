MODULE NAME
    perm_acl_module - access control list
    
OPTIONS
    none

DESCRIPTION
    Configure list of users, groups, IP numbers they are logged from and 
    directories/files they are allowed to access.
    You can use * to match all users, or as mask, e.g. ab* matches all users
    beginning with ab. The same goes for groups and IP numbers. Order is
    important, access list is inherited from previous entries, and also from
    parent directories.
    Not checked commands are inherited (either from previous matching entry
    or from parent subdirectory), checked buttons (commands) are alllowed
    or denied explicitly.
    
    First use most general patterns, then specific ones (in other words,
    put default access for all users, groups, ip numbers and paths at 
    the first line)
    
NOTICE
    Slash (/) at the end of paths is important. If you allow something
    for path /home/ftp/, /home/ftp itself is not covered by this.
    For example, disabling everything for / and enabling LIST for
    /home/ftp/ will _not_ give you permission to do LIST in /home/ftp.
    You must enable LIST for /home/ftp (without trailing slash) to 
    achieve what is probably desired behaviour.

SEE ALSO
    perm_dummy_module
    