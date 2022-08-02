from socket import *

serverPort = 12000 # 服务器指定的端口
serverSocket = socket(AF_INET, SOCK_DGRAM) # 创建UDP套接字

# 将端口与该服务器的端口绑定
# 以这种方式，当向该服务器的IP地址的12000号端口发送分组时，该分组将导向该套接字
serverSocket.bind(('', serverPort))

print("The server in ready to receive")
while True: # 服务器将无限期接收UDP报文并处理来自客户端的分组
	message, clientAddress = serverSocket.recvfrom(2048) # 接收客户端信息，同时获得客户端地址
	modifiedMessage = message.decode().upper() # 将客户端发来的字节解码为字符串后变为大写
	serverSocket.sendto(modifiedMessage.encode(), clientAddress) # 通过已经获得的客户端地址，将修改后的信息发回客户端