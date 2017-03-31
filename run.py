import sys
import os

os.system("data/update");

if len(sys.argv) > 1:
	if sys.argv[1] == 'update':
		os.system('python2 bin/update.py')
	else:
		print("Sorry,%s is not support"%sys.argv[1])
else:
	os.system('python2 bin/dns.py')

