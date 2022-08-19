# Solution of Assignment_5：ICMP Ping

## 作业描述

《计算机网络：自顶向下方法》中第四章末尾给出了此编程作业的简单描述：

> ping是一种流行的网络应用程序，用于测试位于远程的某个特定的主机是否开机和可达。它也经常用于测量客户主机和目标主机之间的时延。他的工作过程是：向目标主机发送ICMP“回显请求”分组（即ping分组），并且侦听ICMP“回显响应”应答（即pong分组）。ping测量RTT，记录分组丢失和计算多个ping-pong交换（往返时间的最小，平均，最大和标准差）的统计汇总。
>
> 在本实验中，你将用Python语言编写自己的ping应用程序。你的应用程序将使用ICMP。但为了保持程序的简单，你将不完全遵循RFC 1739中的官方规范。注意到你将仅需要写该程序的客户程序，因为服务器侧所需的功能构建在几乎所有的操作系统中。你能够在Web站点 http://www.awl.com/kurose-ross 找到本作业的全面细节，以及该Python代码的重要片段。

## 详细描述

官方文档：[Socket5_ICMPpinger(chap4).pdf](Socket5_ICMPpinger(chap4).pdf)

## 实现

使用Python中原生套接字，创建一个IP套接字，在代码中构造ICMP数据包，实现ping操作。

## 代码文件

[IcmpPing.py](IcmpPing.py)

## 运行

运行后会在终端显示：

```shell
Pinging 14.215.177.38 using Python:

Received from 14.215.177.38: byte(s)=8 delay=15ms TTL=55
Received from 14.215.177.38: byte(s)=8 delay=15ms TTL=55
Received from 14.215.177.38: byte(s)=8 delay=15ms TTL=55
Received from 14.215.177.38: byte(s)=8 delay=15ms TTL=55
Packet: sent = 4 received = 4 lost = 0
```

