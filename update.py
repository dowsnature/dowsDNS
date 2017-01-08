# -*- coding:utf-8 -*-
import  urllib2
import json
import base64
def  Get_host():
	list1 = []
	list2 = []
	url = 'https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts'
	data = urllib2.urlopen(url) .read()
	with open("./tmp",'w') as f:
		f.write(data)
	with open("./tmp",'r') as f:
		for line in f:
			if len(line)>4 and line[0:1] != '#' and '\n' and '\r' and '\r\n':
				linedata  = (' '.join(line.split())).split(' ')
				list1.append(linedata[1])
				list2.append(linedata[0])
	dict_data =   dict(zip(list1,list2))
	return  dict_data

def Update_record():
	print "Start [ 1 ]  updating..."
	data = Get_host()
	with open("./rpz.json",'w') as f:
		json.dump(data, f)
		print "[ 1 ] have done ! "
def GetWildcardsrcd():
	url = 'https://raw.githubusercontent.com/dowsnature/dowsDNS/master/wrcd.base64'
	print "Start [ 2 ]  updating..."
	data = urllib2.urlopen(url) .read()
	with open("./wrcd.base64",'w') as f:
		f.write(data)
	print "[ 2 ] have done ! "

if __name__ == '__main__':
	try:
		Update_record()
		GetWildcardsrcd()
	except Exception as e:
		raise e