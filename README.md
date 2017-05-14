
# dowsDNS
特性：
* 支持hosts文件（过滤广告，还有其他美好的事情）
* 支持泛解析（指向sni服务器，有美好的事情发生）
* 支持edns-client-subnet（解析到服务器与你最近）
* 可作为小型DNS公共服务器，也可以作为本机DNS服务

如果提供服务对象不同，需要修改`conf/config.json` 中的  `Public_Server`的值

`False` 代表监听的是本机局域网IP来使用

`True` 代表监听公网IP来使用

如果填写不当，会造成`edns-client-subnet`失效。


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
1. 将 `conf/config.json 中的 Local_dns_server` 的值改为电脑的 `127.0.0.1`

2. 在 `/etc/resolvconf/resolv.conf.d/base` 里添加 `nameserver 127.0.0.1`

3. `sudo resolvconf -u`

4. `sudo systemctl restart network-manager.service`

### 启动

* `sudo python start.py`

### 更新

* `python update.py`

## 局域网共享使用

1. 将 `conf/config.json` 中的 `Local_dns_server` 的值改为电脑的 ip

2. `firewall-cmd –add-port=53/udp      –permanent`

3. `sudo python start.py`

4. 同一局域网下，把其他设备 DNS 改为 运行程序的电脑本地 IP 即可

## 通用方法

1. 将 `conf/config.json` 中的 `Local_dns_server` 的值改为电脑的 `0.0.0.0`

2. `firewall-cmd –add-port=53/udp      –permanent`

3. 在 `/etc/NetworkManager/NetworkManager.conf` 中的 `dns=dnsmasq` 前面加 #

4. 在 `/etc/resolvconf/resolv.conf.d/base` 里添加 `nameserver 127.0.0.1`

5. `sudo resolvconf -u`

6. `sudo systemctl restart network-manager.service`

7. 重启电脑

8. 同一局域网下，把其他设备或本机的 DNS 改为 运行程序的电脑本地 IP 即可

# Mac 

1. `sudo python start.py`

2. 将DNS服务器改为 127.0.0.1

3. 重启网络服务和浏览器即可

* 更新hosts：`python update.py`

# Windows

## 启动

1. 将命令行切换到当前目录

2. `python start.py`

## 更新

* `python update.py`

# 数据引用

* https://pypi.python.org/pypi/dnslib

* https://github.com/racaljk/hosts

