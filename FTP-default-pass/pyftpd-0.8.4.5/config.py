
initial_msg = 'Welcome to pyftpd. Happy downloading.'
do_debug = 0
sbufsize = 16000 # size of send buffer
rbufsize = 16000 # size of receive buffer
modules = ['auth_anonymous_module',
 'auth_db_module',
 'ban_module',
 'fs_chroot_module',
# 'fs_real_module',
 'cwd_module',
 'speed_module',
 'limit_module',
 'iplimit_module',
 'bsd_list_module',
 'perm_acl_module',
 'log_format_module']

timeout_data = 120 # timeout for data connection
timeout_session = 300 # timeout for control connection
initial_wd = '/home/ftp' # initial working directory
port = 2121 # default port

