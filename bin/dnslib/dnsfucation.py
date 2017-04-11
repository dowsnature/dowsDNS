# -*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.INFO)
def Search_key_ip(string,dict_data):
	string = string[:-1]
	if string in dict_data.keys():
		return dict_data[string]
	else:
		domain  = string.split('.')
		while  len(domain) >2:
			domain = domain[1:]
			b = '*.'+'.'.join(domain)
			if b in dict_data.keys():
				return dict_data[b]
		return None

def Hex2Ascii(string):
	try:
		Int = int(string,16)
		return  chr(Int)
	except Exception as e:
		logging.warn("Hex2Ascii info:\t%s"%e)

def Hex2Str_dec(string):
	try:
		return str(int(string,16))
	except Exception as e:
		logging.warn("Hex2Str_dec info:\t%s"%e)

def HexIP2DecIP(string) :
	string = string.replace('\t','').replace('\n','').replace(' ','')
	try:
		if len(string)  == 8:
			return Hex2Str_dec(string[0:2]) +"."+Hex2Str_dec(string[2:4]) +"."+Hex2Str_dec(string[4:6])+"." \
			+Hex2Str_dec(string[6:8]).replace('\t','').replace('\n','').replace(' ','')
		else:
			return "?.?.?.?"
	except Exception as e:
		logging("HexIP2DecIP  info:\t%s"%e)

def DnshextoDomain(string,start=24,end=26):
	'''原始数据：域名指针默认在12个字节位置，
	若不是完整的原始数据，请指定域名指针的位置'''

	try:
		Domain = []
		while string[start:end] != "00" and string[start:end] != "c0":
			n =0
			i = int(string[start:end],16)
			while n<i:
				start = end
				end +=2
				Domain.append(Hex2Ascii(string[start:end]))
				n+=1
			Domain.append(".")
			start = end
			end +=2
		return ''.join(Domain),end
	except Exception as e:
		logging.warn("DnshextoDomain info:\t%s"%e)

def GetDnsDomainIP(data):
	'''提取域名和IP
	成功返回列表，失败返回空列表
	列表格式：["域名"，"十六进制表示的IP1","十六进制表示的IP2",...,"十六进制表示的IPn"]'''
	data = data.encode('hex')

	try:
		iptext= []
		'''retype 值：查询 = 0 ,应答=1'''
		retype = int(bin(int(data[4:5],16)).replace('0b','')[0:1])
		'''ANCOUNT 值：DNS的ANCOUNT区域记录总数'''
		ANCOUNT = int(data[12:16],16)
		text,end = DnshextoDomain(data)
		iptext.append(str(text))
		start = end + 8
		if retype and ANCOUNT:
			'''获取ANCOUNT中的所有记录，保存至iptext'''
			n = 0
			while n< ANCOUNT :
				'''不断移动start和end指针，直至获取所有记录'''
				start = start+4
				end  = start + 4
				dnstype = int(data[start:end],16)
				start = start +16
				end = end+16
				length = int(data[start:end],16)
				start = end+length*2
				if dnstype == 1:
					iptext.append(data[end:start])
				n +=1
		
		return iptext
	except Exception as e:
		logging("GetDnsDomainIP info:\t%s"%e)
		return []

def analysis(data,dict_data):
	'''对DNS数据包进行分析修正'''
	iplist = GetDnsDomainIP(data)
	ip = None
	if len(iplist) >0:
		domain =iplist[0]
		print "Query:\t",domain
		ip = Search_key_ip(domain,dict_data)
	if ip :
		for i,j in enumerate(iplist):
			if i > 0:
				#十进制表示的IP变为十六进制表示的IP
				dnsip =  '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip.split('.'))).lower()
				print "Revise:\t",iplist[0]
				data = data.encode('hex').replace(iplist[i],dnsip).decode('hex')
	return data

def IP2HEX(ip):
	zone = ip.split(".")
	HEX = ''
	for i in zone:
		i = hex(int(i)).replace("0x",'')
		if len(i) < 2:
			i = '0' + i
		HEX += i
	return HEX

def analysis2(data,dict_data):
	'''构造DNS报文'''
	data = data.encode('hex')
	domain,end = DnshextoDomain(data)

	ip = None
	if len(domain) >0:
		ip = Search_key_ip(domain,dict_data)
		logging.info("Query domain:%s\tip:%s", domain, ip)
	if ip  :
		if  data[end+2:end+4] == '1c':
			'''屏蔽IPv6'''
			data = data[0:4] + '81800001000000000000'+data[24:end]+'001c0001'
			return 1,data.decode('hex')

		data = data[0:4] + '81800001000100000000'+data[24:end]+'00010001c00c000100010000003f0004'
		#十进制表示的IP变为十六进制表示的IP
		#dnsip =  '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip.split('.'))).lower()
		dnsip = IP2HEX(ip)
		data =  data + dnsip
		return 1,data.decode('hex')
	return 0,data.decode('hex')
