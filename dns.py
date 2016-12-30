#-*- coding:utf-8 -*-
import socket, sys
import threading
import json

dict_data = {}
dict_config = {}

with open ("config.json",'r') as d:
	dict_config = json.load(d)
	
with open (dict_config['Rpz_json_path'],'r') as c:
	dict_data = json.load(c)
	
#@profile
def Search_key_ip(string):
	if string[0:1] != "*":
		string = "*." + string
	string = string[:-1]
	a = string.split(".")
	while a:
		if len(a) >=3:
			a = a[1:]
			domain = '.'.join(a)
			if domain in dict_data.keys():
				return dict_data[domain]
		else:
			return None
	return None


#@profile
def hex2ascii(string):
	Int = int(string,16)
	return  chr(Int)
#@profile
def hex2str_dec(string):
	return str(int(string,16))
#@profile
def hexiptodecip(string) :
	return hex2str_dec(string[0:2]) +"."+hex2str_dec(string[2:4]) +"."+hex2str_dec(string[4:6])+"."+hex2str_dec(string[6:8])
#@profile
def Message2QUESTION_Domain(string,start=24,end=26):
	dom 		= []

	while string[start:end] != "00" and string[start:end] != "c0":
		n =0
		i = int(string[start:end],16)
		while n<i:
			start = end
			end +=2
			dom.append(hex2ascii(string[start:end]))
			n+=1
		dom.append(".")
		start = end
		end +=2
	return ''.join(dom),end
#@profile
def dnshextotext(data):
	'''分析DNS数据'''
	data = data.encode('hex')
	try:
		iptext= []
		retype = int(bin(int(data[4:5],16)).replace('0b','')[0:1])
		ANCOUNT = int(data[12:16])
		text,end = Message2QUESTION_Domain(data)
		iptext.append(str(text))
		start = end +8
		if retype and ANCOUNT:
			'''获取ANCOUNT中的所有记录，保存至iptext'''
			n = 0
			while n< ANCOUNT :
				start = start
				end  = start+4
				a = int(data[end-2:end],16)
				start = end
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
		return []
#@profile
def analysis(data):
	'''对DNS数据包进行分析修正'''
	iplist = dnshextotext(data)
	ip = None
	if len(iplist) >0:
		domain =iplist[0]
		ip = Search_key_ip(domain)
	if ip :
		for i,j in enumerate(iplist):
			if i > 0:
				dnsip =  '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip.split('.'))).lower()
				print iplist[0] ,"\t\t--修正->\t\t",ip
				data = data.encode('hex').replace(iplist[i],dnsip).decode('hex')
	return data
#@profile
def Ssend(data,s,addr):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	sock.sendto(data, (dict_config['Remote_dns_server'],dict_config['Remote_dns_port']))
	sock.settimeout(5)
	while True:
		try:
			rspdata = sock.recv(4096)
			rspdata = analysis(rspdata)
			s.sendto(rspdata,addr)
			break
		except Exception as e:
			print e
			break
			#print dnshextotext(data.encode('hex'))[0],"查询错误：",e
#@profile
def Tthreading(data,s,addr,):
	
	t = threading.Thread(target=Ssend,args=(data,s,addr,))
	t.setDaemon(True)
	t.start()
	#print "当前进程：" ,threading.activeCount()

#@profile
def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((dict_config['Local_dns_server'],dict_config['Local_dns_port']))
	try:
		while 1:
			data, addr = s.recvfrom(2048)
			Tthreading(data,s,addr)
			
	except KeyboardInterrupt:
		s.close()
		sys.exit(0)
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print e

'''
def dnshextotext(data):
	try:
		iptext= []
		#print "-----------------------------------------"
		#print "标志ID：",data[0:4]
		#print "标志字段：",data[4:8]
		retype = int(bin(int(data[4:5],16)).replace('0b','')[0:1])
		#print "请求类型：",retype
		#print "问题记录数：",data[8:12]
		ANCOUNT = int(data[12:16])
		#print "资源记录数：",ANCOUNT,data[12:16]
		#print "授权资源记录数：",data[16:20]
		#print "额外资源记录数：",data[20:24]
		text,end = Message2QUESTION_Domain(data)
		#print "查询域名：",text
		iptext.append(str(text))
		#print "响应类型：",int(data[end:end+4],16)
		#print "响应类：",data[end+4:end+8]
		start = end +8
		#print "-----------------------------------------\n\n"
		if retype and ANCOUNT:
			n = 0
			#print "循环次数：",ANCOUNT
			while n< ANCOUNT :
				start = start
				end  = start+4
				#print "指针：",data[start:end]
				a = int(data[end-2:end],16)
				start = end
				end  = start + 4
				dnstype = int(data[start:end],16)
				#print "响应类型：",dnstype
				start = end
				end = start + 4
				#print "响应类：",data[start:end]
				start = end
				end = start + 8
				#print "资源生存时间：",data[start:end]
				start = end
				end = start + 4
				length = int(data[start:end],16)
				#print "数据长度：",length
				start = end+length*2
				if dnstype == 1:
					iptext.append(data[end:start])
					#iptext.append(hexiptodecip(data[end:start]))
					#print "IP地址：",iptext
				elif dnstype == 5:
					pass
					#print "CName：",Message2QUESTION_Domain(data[end:start],0,2)[0]
				else :
					pass
					#print data[end:start]
				#print "====================================="
				n +=1
		return iptext
	except Exception as e:
		print e
		return []

		print "指针：",data[start:start+4]
		a = int(data[start+2:start+4],16)
		text,end = Message2QUESTION_Domain(data[a*2:],0,2)
		print text
		print "响应类型：",data[start+4:start+8]
		print "响应类：",data[start+8:start+12]
		print "资源生存时间：",data[start+12:start+20]
		length = int(data[start+20:start+24],16)
		print "数据长度：",data[start+20:start+24],length
		print data[start+24:start+24+length*2]

'''
