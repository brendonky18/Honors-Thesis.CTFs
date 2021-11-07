MODULE NAME
    auth_db_module - authentificate users against internal database

OPTIONS
    none

DESCRIPTION
    Configure list of users, corresponding groups and passwords.
    Passwords are kept in md5-hashed form, to enter them use 
    configure_auth_db.py, simple editing the file auth_db_configure.py 
    is not sufficient.

SEE ALSO
    auth_anonymous_module
    auth_PAM_module
