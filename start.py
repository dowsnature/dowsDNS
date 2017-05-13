#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket, sys
import threading
import json
import logging
import dnslib

logging.basicConfig(level=logging.INFO)
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

def Tthreading(data,s,addr,):	
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
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(data, (Remote_dns_server,Remote_dns_port))
		sock.settimeout(5)
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

