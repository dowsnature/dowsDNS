# 注意只更改了Linux版本

## 更新hosts文件
1. 将hosts拷入data目录
2. 重新运行即可

## 使用方法
1. git clone https://github.com/liuyunbin/dowsDNS
2. cd dowsDNS/data
3. make
4. cd ..
5. sudo sudo python2 run.py
6. 将DNS服务器改为 本机ip---可使用 ip addr查看
7. 重启网络服务和浏览器即可


# 原项目README

# dowsDNS

快速翻越中国防火墙

# 使用方法

仅支持Linux/Windows/Mac

## Linux/Mac

* sudo python2 run.py

* 运行成功后再修改系统DNS为：dowsDNS/conf/config.json中的"Local_dns_server"的ip即可
* 更新：python2 run.py update 或 python2 bin/update.py

## Windows

* 下载 dowsDNS.zip，解压

 * 下载地址：https://github.com/dowsnature/dowsDNS/releases/latest/

* 右键管理员身份运行 Windows.bat


# 局域网共享使用

若想让同局域网内所有设备使用DNS翻墙功能，请

* 修改文件config.json

 "Local_dns_server" : "127.0.0.1",

 127.0.0.1 把此IP换成 电脑本地IP

* 同一局域网下，把手机DNS改为 运行程序的电脑本地IP即可

# 效果

![](http://pix.toile-libre.org/upload/original/1483170936.png)

# 数据引用


  * https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  
  * https://github.com/racaljk/hosts
  
# 更多请参阅

[ZERONET官网](https://zeronet.io/)

[ZERONET各大平台使用教程(英文)](https://github.com/HelloZeroNet/ZeroNet#user-content-how-to-join)

## 以下链接请务必以zeronet访问

[基于zeronet的博客](http://127.0.0.1:43110/1P7kEUyonzvkx6yywce2PBn7zPrngX5pgz/?Post:3:Windows+%E4%BD%BF%E7%94%A8dowDNS%E6%95%99%E7%A8%8B)

[Windows 使用dowDNS教程](http://127.0.0.1:43110/1P7kEUyonzvkx6yywce2PBn7zPrngX5pgz/?Post:3:Windows+%E4%BD%BF%E7%94%A8dowDNS%E6%95%99%E7%A8%8B)
