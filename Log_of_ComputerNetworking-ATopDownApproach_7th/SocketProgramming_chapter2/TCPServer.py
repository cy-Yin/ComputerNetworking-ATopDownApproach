from socket import *

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM) # 创建TCP欢迎套接字
serverSocket.bind(('',serverPort)) # 将服务器端口号serverPort与该套接字绑定起来
serverSocket.listen(10) # 服务器聆听来自客户端的TCP连接请求。最大连接数设置为10
print("The server in ready to receive")

while True:
	connectionSocket, addr = serverSocket.accept() # 接收到客户连接请求后，调用accept函数建立新的TCP连接套接字
	
	sentence = connectionSocket.recv(2048).decode() # 获取客户发送的字符串
	capitalizedSentence = sentence.upper() # 将字符串改为大写
	connectionSocket.send(capitalizedSentence.encode()) # 向用户发送修改后的字符串
	connectionSocket.close() # 关闭TCP连接套接字