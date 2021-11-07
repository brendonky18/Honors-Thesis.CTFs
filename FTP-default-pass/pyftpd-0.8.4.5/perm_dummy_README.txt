MODULE NAME
    perm_dummy_module - dummy permissions, always allow acces
    
OPTIONS
    none

DESCRIPTION
    always allow access to files. This means that the normal OS permissions
    apply (everything allowed in Windows 95/98, standard permissions under UNIX)
    While this module can be sufficient for operating systems with UNIX-like
    permissions, it is strongly recommended to use perm_acl_module.
    
SEE ALSO
    perm_acl_module
    