
LIST = [ "cwd", "list", "nlst"]
GET = ["retr", "size", "mdtm"]
READ = LIST+GET

PUT = ["stor", "appe", "mkd"]
DELETE = ["dele", "rmd"]
WRITE = PUT+DELETE
ALL = READ+WRITE+["site"]

acllist = [('*', '*', '*', '/', ['cwd', 'list', 'nlst', 'retr', 'size', 'mdtm'], []),
 ('*', '*', '*', '/etc', ['appe', 'retr'], ['size', 'mdtm', 'retr']),
 ('*', '*', '*', '/tmp', ['stor', 'appe', 'mkd', 'dele', 'rmd'], []),
 ('*', '*', '*', '/home', ['stor', 'appe', 'mkd', 'dele', 'rmd'], []),
 ('anonymous',
  '*',
  '*',
  '/',
  [],
  ['cwd',
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
  '/',
  ['cwd', 'list', 'nlst', 'retr', 'size', 'mdtm'],
  []),
 ('anonymous', '*', '*', '/home/ftp/bin', [], ['size', 'mdtm', 'retr']),
 ('anonymous', '*', '*', '', ['site'], []),
 ('anonymous', '*', '*', '/incoming', ['stor', 'appe', 'mkd'], []),
 ('roxon',
  '*',
  '*',
  '/',
  ['size', 'mdtm', 'cwd', 'nlst', 'retr', 'list'],
  ['appe', 'rmd', 'stor', 'dele', 'mkd'])]



