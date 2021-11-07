
initial_msg = 'Welcome to pyftpd. Happy downloading.'
do_debug = 1
sbufsize = 16000 # size of send buffer
rbufsize = 16000 # size of receive buffer
modules = ['auth_db_module',
 'auth_anonymous_module',
 'ban_module',
 'cwd_module',
 'speed_module',
 'limit_module',
 'iplimit_module',
 'bsd_list_module',
 'perm_acl_module',
 'fs_real_module',
 'log_simple_module']

timeout_data = 120 # timeout for data connection
timeout_session = 300 # timeout for control connection
initial_wd = 'c:\\' # initial working directory
port = 2121 # default port

