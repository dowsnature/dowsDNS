# -*- coding:utf-8 -*-
import  urllib.request,  urllib.error,  urllib.parse
import json
import base64
def  Get_host(url):
	list1 = []
	list2 = []
	data = urllib.request.urlopen(url) .read()
	with open("./data/tmp",'w') as f:
		f.write(data)
	with open("./data/tmp",'r') as f:
		for line in f:
			if len(line)>4 and line[0:1] != '#' and '\n' and '\r' and '\r\n':
				linedata  = (' '.join(line.split())).split(' ')
				list1.append(linedata[1])
				list2.append(linedata[0])
	dict_data =   dict(list(zip(list1,list2)))
	return  dict_data

def Update_record(data):
	print ("Starting   [ 1 ]  updating...")

	with open("./data/rpz.json",'w') as f:
		json.dump(data, f)
		print ("success!   [ 1 ]  have done ! ")
def GetWildcardsrcd(url):
	print ("Starting   [ 2 ]  updating...")
	data = urllib.request.urlopen(url) .read()
	with open("./data/wrcd.json",'w') as f:
		f.write(data)
	print ("success!   [ 2 ]  have done ! ")

def main():
	with open ("./conf/hosts_repository_config.json",'r') as d:
		dict_config = json.load(d)
	dict_host={}

	for key1 in dict_config:
		if key1 == "hosts":
			for key2 in dict_config[key1]:
				url = dict_config[key1][key2]
				dict1 = Get_host(url)
				dict_host.update(dict1)
		elif key1 == "wrcd":
			pass
		else:
			print(("Sorry,%s is not support"%key1))

	url = dict_config['wrcd']
	Update_record(dict_host)
	GetWildcardsrcd(url)


if __name__ == '__main__':
	try:
		main()
		#Update_record()
		#GetWildcardsrcd()
	except Exception as e:
		raise e
