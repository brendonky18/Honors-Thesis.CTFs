MODULE NAME
    auth_cwd_module - per user configuration of initial working directories

OPTIONS
    none

DESCRIPTION
    if user matches the pattern, his initial directory is set to the
    value of second field.
    This overrides initial_cwd in config.py.
    You can use * to match all users, or as mask, e.g. ab* matches all users
    beginning with ab. Order is important, first use most general patterns, 
    then specific ones (in other words, put default cwd for * (all not 
    explicitly mentioned users) at the first line).
    Warning: if you use fs_chroot_module, this directory is relative
    to the chrootdir.
    