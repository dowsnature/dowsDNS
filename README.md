# dowsDNS
快速翻跃中国防火墙

# 使用方法

修改文件config.json

`"Local_dns_server" : "10.0.2.15",`

`10.0.2.15` 把此IP换成本地IP,或者公网IP

然后执行 `python dns.py`

修改本机的dns地址为本机ip地址即可


## 本机ip

Windows 可用 ipconfig 命令查看

Linux 可用 ifconfig 命令查看

# rpz.json 格式说明

按照JSON格式添加记录即可

如查找 123.www.google.com

先匹配 123 ,若未找到,则继续

匹配 wwww ,若未找到,则继续如此递减匹配,

直到google.com为止。

所以添加域名，务必添加一级域名



# 缺陷

* 不支持IPv6
* 查找性能有待提高
