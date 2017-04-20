
# dowsDNS

快速翻越中国防火墙

# 本机使用方法

仅支持Linux/Windows/Mac

## Linux ----- 已测试 python 测试版本 3.5
1. sudo sudo ./start.py
2. 将DNS服务器改为 127.0.0.1
3. 重启网络服务和浏览器即可

## Mac ---- 未测试
1. sudo ./start.sh 
2. 将DNS服务器改为 127.0.0.1
3. 重启网络服务和浏览器即可

* 更新hosts：./update.sh

## Windows ---- 未测试

* 右键管理员身份运行 start.bat或update.bat(更新hosts)


# 局域网共享使用

# ubuntu ---- 已测试
1. firewall-cmd –add-port=53/udp      –permanent
2. 同一局域网下，把其他设备 DNS 改为 运行程序的电脑本地 IP 即可

# 数据引用
* https://raw.githubusercontent.com/vokins/yhosts/master/hosts
* https://raw.githubusercontent.com/aoccin/adaway/master/hosts
* https://github.com/racaljk/hosts


# 更多请参阅

* http://www.codedev.cn/forum.php?mod=viewthread&tid=10
