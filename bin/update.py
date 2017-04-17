import urllib.request
import json

def  Get_host(url):
	data = urllib.request.urlopen(url).read().decode()
	dict_data = {}
	with open("./data/tmp",'w') as f:
		f.write(data)
	with open("./data/tmp",'r') as f:
		for line in f:
			if len(line) > 4 and line[0:1] != '#' and '\n' and '\r' and '\r\n':
				linedata  = (' '.join(line.split())).split(' ')
				if len(linedata) >= 2:
					dict_data[linedata[1]] = linedata[0]
	return  dict_data

def Update_record(data):
	print ("Starting   [ 1 ]  updating...")

	with open("./data/rpz.json",'w') as f:
		json.dump(data, f)
		print ("success!   [ 1 ]  have done ! ")
def GetWildcardsrcd(url):
	print ("Starting   [ 2 ]  updating...")
	data = urllib.request.urlopen(url) .read().decode()
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
				dict_host.update( Get_host(url) )
	Update_record(dict_host)
	GetWildcardsrcd(dict_config['wrcd'])


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		raise e

