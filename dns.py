# -*- coding:utf-8 -*-
import dnslib.dnsfucation as dns
import socket, sys
import threading
import json
import base64

dict_data = {}
dict_config = {}
Remote_dns_server='114.114.114.114'
Remote_dns_port=53
Local_dns_server='127.0.0.1'
Local_dns_port=53

def Load_config():
	global dict_data
	global dict_config
	global Remote_dns_server
	global Remote_dns_port
	global Local_dns_server
	global Local_dns_port
	dict_wdata={}
	with open ("config.json",'r') as d:
		dict_config = json.load(d)
	
	with open (dict_config['Rpz_json_path'],'r') as c:
		dict_data = json.load(c)

	with open("./wrcd.base64",'r') as f:
		data  = base64.b64decode(f.read())
		dict_wdata = json.loads(data)
	dict_data.update(dict_wdata)


	Remote_dns_server 	= 	dict_config['Remote_dns_server']
	Remote_dns_port		=	dict_config['Remote_dns_port']
	Local_dns_server		=	dict_config['Local_dns_server']
	Local_dns_port		= 	dict_config['Local_dns_port']

def Tthreading(data,s,addr,):
	
	t = threading.Thread(target=SendDnsData,args=(data,s,addr,))
	t.setDaemon(True)
	t.start()

def SendDnsData(data,s,addr):
	global Remote_dns_server
	global Remote_dns_port
	global dict_data
	
	local,data = dns.analysis2(data,dict_data)
	if local ==1:
		s.sendto(data ,addr)
	else:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(data, (Remote_dns_server,Remote_dns_port))
		sock.settimeout(5)
		while True:
			try:
				rspdata = sock.recv(4096)
			except Exception as e:
				print "sock.recv info:",e
				break
			s.sendto(rspdata ,addr)
			break

def main(s):
	try:
		while 1:
			data, addr = s.recvfrom(2048)
			Tthreading(data,s,addr)
	except Exception as e:
		print "Unknow error :\t",e

if __name__ == '__main__':

	Load_config()
	print "==========Config==========="
	print "Local_dns_server:",Local_dns_server
	print "Local_dns_port:",Local_dns_port
	print "Remote_dns_server:",Remote_dns_server
	print "Remote_dns_port:",Remote_dns_port
	print "===========Config=========="
	print "Trying start bind local IP and port ..."
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.bind((Local_dns_server,Local_dns_port))
	except Exception as e:
		print "\nBinding failed! Please run as administrator，\n\nAnd check the local IP address and port is correct?\n"
		print "==========Error message=========="
		raise e
	print "Bind successfully! Running ..."
	main(s)
