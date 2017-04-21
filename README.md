
# dowsDNS

快速翻越中国防火墙

# 本机使用方法

仅支持Linux/Windows/Mac

## Linux ----- 已测试 ubuntu 16.04 python 测试版本 3.5
### 启动
1. sudo ./start.py
2. 将DNS服务器改为 127.0.0.1
3. 重启网络服务和浏览器即可

### 更新
* ./update.py

## Mac ---- 未测试 --- 欢迎有测试的同学提意见
1. sudo ./start.py 
2. 将DNS服务器改为 127.0.0.1
3. 重启网络服务和浏览器即可

* 更新hosts：./update.py

## Windows ---- 已测试 --- xp -- python 3.4
### 启动
1. 将命令行切换到当前目录
2. python start.py

### 更新
* python update.py


# 局域网共享使用

## ubuntu ---- 已测试
1. firewall-cmd –add-port=53/udp      –permanent
2. 同一局域网下，把其他设备 DNS 改为 运行程序的电脑本地 IP 即可

# 数据引用
* https://pypi.python.org/pypi/dnslib
* https://github.com/racaljk/hosts


# 更多请参阅

* http://www.codedev.cn/forum.php?mod=viewthread&tid=10
