from socket import *

serverName = input('Please enter the hostname of server: ') # 提供服务器的地址或主机名的字符串（若使用主机名将自动执行DNS lookup得到IP地址）。
serverPort = 12000 # 指定服务器端口

# 创建UDP套接字。
# 第一个参数使用地址簇，特别地，AF_INET指示底层网络使用IPv4协议；
# 第二个参数指示变量是一个UDP套接字。
clientSocket = socket(AF_INET, SOCK_DGRAM) 

message = input('Input lowercase sentence:') # 用户输入信息

# 通过该套接字向目的主机发送报文
# 先用encode()方式将字符串转换为字节类型
clientSocket.sendto(message.encode(), (serverName, serverPort)) 

# 当分组到达套接字时，数据存放在modifiedMessage中，源地址存放在serverAddress中
modifiedMessage, serverAddress = clientSocket.recvfrom(2048) # 设置缓存长度为2048

print(modifiedMessage.decode()) # 显示服务器返回的信息

clientSocket.close() # 关闭套接字，然后关闭该进程