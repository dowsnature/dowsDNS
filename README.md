
# dowsDNS


快速翻越中国防火墙

![](https://img.shields.io/badge/Platform-Windows%20Mac%20linux-blue.svg)
![dnslib 0.9.7](https://img.shields.io/badge/Dependency-dnslib%200.9.7-blue.svg)
![](https://img.shields.io/badge/Environment-Python2.7%20%7C%20Python3.4-blue.svg)

# 测试

![](https://img.shields.io/badge/Python2.7-测试通过-brightgreen.svg)
![](https://img.shields.io/badge/Python3.4-测试通过-brightgreen.svg)
![](https://img.shields.io/badge/Python3.5-测试通过-brightgreen.svg)
![](https://img.shields.io/badge/Python3.6-测试通过-brightgreen.svg)

# Linux 

## 本机使用
### 更改 DNS 域名服务器
1. 将 conf/config.json 中的 Local_dns_server 的值改为电脑的 127.0.0.1
2. 在 /etc/resolvconf/resolv.conf.d/base 里添加 nameserver 127.0.0.1
3. sudo resolvconf -u
4. sudo systemctl restart network-manager.service

### 启动
* sudo ./start.py

### 更新
* ./update.py

## 局域网共享使用
1. 将 conf/config.json 中的 Local_dns_server 的值改为电脑的 ip
2. firewall-cmd –add-port=53/udp      –permanent
3. sudo ./start.py
4. 同一局域网下，把其他设备 DNS 改为 运行程序的电脑本地 IP 即可

## 通用方法
1. 将 conf/config.json 中的 Local_dns_server 的值改为电脑的 0.0.0.0
2. firewall-cmd –add-port=53/udp      –permanent
3. 在 /etc/NetworkManager/NetworkManager.conf 中的 dns=dnsmasq 前面加 #
4. 在 /etc/resolvconf/resolv.conf.d/base 里添加 nameserver 127.0.0.1
5. sudo resolvconf -u
6. sudo systemctl restart network-manager.service
7. 重启电脑
8. 同一局域网下，把其他设备或本机的 DNS 改为 运行程序的电脑本地 IP 即可

# Mac 
1. sudo ./start.py 
2. 将DNS服务器改为 127.0.0.1
3. 重启网络服务和浏览器即可

* 更新hosts：./update.py

# Windows
## 启动
1. 将命令行切换到当前目录
2. python start.py

## 更新
* python update.py

# 数据引用
* https://pypi.python.org/pypi/dnslib
* https://github.com/racaljk/hosts

