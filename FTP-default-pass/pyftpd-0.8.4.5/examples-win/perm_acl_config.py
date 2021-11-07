
LIST = [ "cwd", "list", "nlst"]
GET = ["retr", "size", "mdtm"]
READ = LIST+GET

PUT = ["stor", "appe", "mkd"]
DELETE = ["dele", "rmd"]
WRITE = PUT+DELETE
ALL = READ+WRITE

acllist = [('*',
  '*',
  '*',
  '*',
  [ 'cwd', 'list', 'nlst', 'retr', 'size', 'mdtm'],
  []),
 ('*', '*', '*', 'c:\\ftp\\upload', ['stor', 'appe', 'mkd', 'dele', 'rmd'], []),
 ('anonymous',
  '*',
  '*',
  '*',
  [],
  [
   'cwd',
   'list',
   'nlst',
   'retr',
   'size',
   'mdtm',
   'stor',
   'appe',
   'mkd',
   'dele',
   'rmd']),
 ('anonymous',
  '*',
  '*',
  'c:\\ftp',
  [ 'cwd', 'list', 'nlst', 'retr', 'size', 'mdtm'],
  []),
 ('anonymous', '*', '*', 'c:\\ftp\\upload', ['stor', 'appe', 'mkd'], [])]



