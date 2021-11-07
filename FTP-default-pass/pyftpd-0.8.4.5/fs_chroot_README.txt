MODULE NAME
    fs_chroot_module - access to filesystem, with the
        ability of per user configuration of virtual directories

OPTIONS
    slave_fs - slave filesystem module, upon which this module operates.
               Usually fs_real_module.

DESCRIPTION
    if user matches the pattern, the value of the second field is 
    preppended to all file operations. As a result, the user will see only
    subdirectories, without a chance to escape out (with the exception of
    following symlinks). You can use * to match all users, or as mask, e.g.
    ab* matches all users beginning with ab. Order is important, first use
    most general patterns, then specific ones (in other words, put default
    chroot directory for * (all not  explicitly mentioned users) at the
    first line).  
    
SEE ALSO
    fs_real_module
        