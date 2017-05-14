#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket, sys
import threading
import json
import logging
import dnslib
from binascii import unhexlify

url = 'http://ip.6655.com/ip.aspx'

if sys.version_info < (3,4):
	import urllib2 as urlR
	Myip = urlR.urlopen(url).read()
else:
	import urllib.request as urlR
	Myip = urlR.urlopen(url).read().decode()

logging.basicConfig(level=logging.INFO)
dict_data = {}
dict_config = {}
Remote_dns_server='114.114.114.114'
Remote_dns_port=53
Local_dns_server='127.0.0.1'
Local_dns_port=53
Public_Server=False

def Load_config():
	global dict_data
	global dict_config
	global Remote_dns_server
	global Remote_dns_port
	global Local_dns_server
	global Local_dns_port
	global Public_Server
	dict_wdata={}
	with open ("./conf/config.json",'r') as d:
		dict_config = json.load(d)

	with open (dict_config['Rpz_json_path'],'r') as c:
		dict_data = json.load(c)

	with open("./data/wrcd.json",'r') as f:
		dict_wdata = json.load(f)

	if dict_config['sni_proxy_on']:
		for key in dict_wdata:
			dict_wdata[key] = dict_config['sni_proxy_ip']
	dict_data.update(dict_wdata)

	Remote_dns_server 	= 	dict_config['Remote_dns_server']
	Remote_dns_port		=	dict_config['Remote_dns_port']
	Local_dns_server	=	dict_config['Local_dns_server']
	Local_dns_port		= 	dict_config['Local_dns_port']
	Public_Server		= 	dict_config['Public_Server']

def Tthreading(data,s,addr):
	t = threading.Thread(target=SendDnsData,args=(data,s,addr,))
	t.setDaemon(True)
	t.start()

def Search_key_ip(string):
	global dict_data
	string = string[:-1]
	if string in list(dict_data.keys()):
		return dict_data[string]
	else:
		domain  = string.split('.')
		while  len(domain) > 2:
			domain = domain[1:]
			b = '*.'+'.'.join(domain)
			if b in list(dict_data.keys()):
				return dict_data[b]
		return None


def AddEDNSOption(data,clientip):
	'''构造edns报文'''
	if not Public_Server:
		 clientip = Myip

	if len(data)==28:
		ip = clientip.split(".")
		ip = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip)).lower()
		a = b"000029100000000000000c0008000800012000" + ip.encode('utf-8')
		data = data[:11] + unhexlify(b'01') + data[12:]
		return data + unhexlify(a)
	else:
		return  data

def SendDnsData(data,s,addr):
	global Remote_dns_server
	global Remote_dns_port

	'''dns请求报文'''
	request_packet = dnslib.DNSRecord.parse(data)
	'''dns请求报文的域名'''
	domain = request_packet.get_q().get_qname()
	'''dns响应报文'''
	response_packet = request_packet.reply()
	ip = Search_key_ip(str(domain))
	if ip != None:
		print(domain, ':', ip)
		response_packet.add_answer(dnslib.RR(domain, dnslib.QTYPE.A, rdata=dnslib.A(ip), ttl=60))
		s.sendto(response_packet.pack(), addr)
	else:
		data = AddEDNSOption(data,addr[0])
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(5)
		sock.sendto(data, (Remote_dns_server,Remote_dns_port))
		while True:
			try:
				rspdata = sock.recv(4096)
			except Exception as e:
				logging.warn("Recv:\t%s"%e)
				break
			s.sendto(rspdata ,addr)
			break

def main(s):

	while 1:
		try:
			data, addr = s.recvfrom(2048)
			Tthreading(data,s,addr)
		except Exception as e:
			logging.warn("Unknow error:\t%s"%e)

if __name__ == '__main__':
	Load_config()
	print("==========Config===========")
	print("Local_dns_server:",Local_dns_server)
	print("Local_dns_port:",Local_dns_port)
	print("Remote_dns_server:",Remote_dns_server)
	print("Remote_dns_port:",Remote_dns_port)
	print("Public_Server:",Public_Server)
	print("===========Config==========")
	print("Trying start bind local IP and port ...")
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.bind((Local_dns_server,Local_dns_port))
	except Exception as e:
		print("\nBinding failed! Please run as administrator，\n\nAnd check the local IP address and port is correct?\n")
		print("==========Error message==========")
		logging.critical(e)
		sys.exit(-1)
	print("Bind successfully! Running ...")
	main(s)
