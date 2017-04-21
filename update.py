#!/usr/bin/env python3

import urllib.request
import json
import os

def  Get_host(url):
	data = urllib.request.urlopen(url).read().decode()
	dict_data = {}
	with open("./data/tmp",'w') as f:
		f.write(data)
	with open("./data/tmp",'r') as f:
		for line in f:
			if len(line) > 4 and line[0:1] != '#' and '\n' and '\r' and '\r\n':
				linedata  = line.split()
				if len(linedata) >= 2:
					dict_data[linedata[1]] = linedata[0]
	os.remove("./data/tmp")	

	return  dict_data

def Update_record(data):
	print ("Starting hosts updating...")

	with open("./data/rpz.json",'w') as f:
		json.dump(data, f)
		print ("success! hosts  have done ! ")

def GetWildcardsrcd(url):
	print ("Starting  wrcd  updating...")
	data = urllib.request.urlopen(url) .read().decode()
	with open("./data/wrcd.json",'w') as f:
		f.write(data)
	print ("success!  wrcd  have done ! ")

def main():
	with open ("./conf/hosts_repository_config.json",'r') as d:
		dict_config = json.load(d)
	dict_host={}

	for key1 in dict_config:
		if key1 == "hosts":
			for key2 in dict_config[key1]:
				url = dict_config[key1][key2]
				dict_data = Get_host(url)
				dict_host.update( dict_data )
			Update_record(dict_host)
		elif key1 == "wrcd":
			url = dict_config[key1]
			GetWildcardsrcd(url)

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		raise e

