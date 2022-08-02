from socket import *

serverName = input('Please enter the hostname of server: ') # 提供服务器的地址或主机名的字符串
serverPort = 12000 # 指定服务器端口

# 建立客户端的套接字。
# 第二个参数SOCK_STREAM表明是TCP类型的套接字。
# 创建客户端套接字时不用指定端口号，操作系统会进行分配
clientSocket = socket(AF_INET, SOCK_STREAM) 

clientSocket.connect((serverName, serverPort)) # 客户端向服务器发起连接，执行三次握手，建立起TCP连接

sentence = input('Input lowercase sentence: ') # 用户在客户端中输入信息

# 将信息发送到服务器
# 与UDP连接不同的是，TCP socket并不显式地创建一个分组并附上目的地址，而只是将分组放入TCP连接中
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recvfrom(2048) # 从服务器接收信息

print('From server: ', modifiedSentence[0].decode()) # 显示信息

clientSocket.close() # 关闭套接字，因此关闭客户端和服务器之间的TCP连接