# 计算机网络——自顶向下方法 7th

中国科学技术大学 郑烇教授 2020年秋季 自动化系

## 4. 网络层——数据平面

目标：
- 理解网络服务的基本原理，聚焦于其数据平面
    - 网络服务模型
    - 转发（数据平面）和路由（控制平面），各有2种方式：传统方式和SDN方式
    - 路由器工作原理
    - 通用转发
- 互联网中网络层协议的实例和实现

### 4.1 导论

网络层服务
- 在发送主机和接收主机对之间传送段(segment)
- 在发送端将段封装到数据报中
- 在接收端，将段上交给传输层实体
- 网络层协议存在于**每一个**主机和路由器（每一个都需要封装和解封装）
- 路由器检查每一个经过它的IP数据报的头部

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001100723126.png" alt="image-20211001100723126" style="zoom:80%;" />

网络层的关键功能
- 网络层功能：
    - **转发**（一个局部的概念，数据平面）：将分组从路由器的输入接口转发到合适的输出接口
    - **路由**（一个全局的功能，控制平面）：使用路由算法来决定分组从发送主机到目标接收主机的路径
        - 路由选择算法
        - 路由选择协议
- 旅行的类比：
    - 转发：通过单个路口的过程
    - 路由：从源到目的的路由路径规划过程

网络层：数据平面、控制平面
- 数据平面：分组从哪个端口输入，从哪个端口输出
    - 本地，每个路由器功能
    - 决定从路由器输入端口到达的分组如何转发到输出端口
    - 转发功能：
        - 传统方式：基于目标IP地址得知哪个端口输入 + 转发表（路由表）决定哪个端口输出
        - SDN方式：基于多个字段 + 与 流表 做匹配，通过匹配的表象进行相应的动作（如转发、阻止、泛洪、修改等）（不像传统方式只进行转发，更加灵活）
- 控制平面：决定分组在整个网络中的路径
    - 控制网络范围内的逻辑
    - 决定数据报如何在路由器之间路由，决定数据报从源到目标主机之间的端到端路径
    - 2个控制平面方法：
        - 传统的路由算法：在路由器中被实现，得到路由表
        - software-defined networking (SDN，软件定义网络)：在远程的服务器中实现，计算出流表通过南向接口交给分组交换设备，进而与分组的多个字段相匹配并根据匹配结果进行相应的动作

传统方式：每-路由器(Per-router)控制平面
- 在每一个路由器中的单独路由器算法元件，在控制平面进行交互
- 控制平面和数据平面紧耦合（集中于一台设备上实现），分布式计算路由表，难以修改路由设备的运行逻辑，模式僵化

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001102609192.png" style="zoom:60%"/>

传统方式：路由和转发的相互作用

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001102633237.png" />

SDN方式：逻辑集中的控制平面
- 一个不同的（通常是远程的）控制器与本地控制代理（CAs）交互，只用在控制器处改变流表就可以改变网络设备的行为逻辑，易修改、可编程

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001102716772.png" />

网络服务模型
- Q：从发送方主机到接收方主机传输数据报的“通道”，网络提供什么样的服务模型(service model)？服务模型有一系列的指标
    - 对于单个数据报的服务：
        - 可靠传送
        - 延迟保证，如：少于40ms的延迟
    - 对于数据报流（一系列分组的序列）的服务：
        - 保序数据报传送
        - 保证流的最小带宽
        - 分组之间的延迟差(jitter)

连接建立
- 在某些网络架构中是第三个重要的功能（继 路由、转发 之后）
    - ATM（有连接：建立连接&路径上所有主机进行维护）, frame relay, X.25
- 在分组传输之前，在两个主机之间，在通过一些路由器所构成的路径上建立一个网络层连接
    - 涉及到路由器
- 网络层和传输层连接服务区别:
    - 网络层：在2个主机之间，涉及到路径上的一些路由器，有连接
    - 传输层：在2个进程之间，很可能只体现在端系统上（TCP连接），面向连接

网络层服务模型：
|网络架构|服务模型|保证带宽|不丢失|保序|延迟保证|拥塞反馈|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|Internet|best effort “尽力而为”|none|no|no|no|no (inferred via loss)|
|ATM|CBR(恒定速率)|constant rate|yes|yes|yes|no congestion|
|ATM|VBR(变化速率)|guaranteed rate|yes|yes|yes|no congestion|
|ATM|ABR(可用比特率)|guaranteed minimum|no|yes|no|yes|
|ATM|UBR(不指名比特率)|none|no|yes|no|no|

### 4.2 路由器组成

路由器结构概况
- 高层面（非常简化的）通用路由器体系架构：输入端口 + 输出端口 + 交换结构 
    - 路由：运行路由选择算法／协议 (RIP, OSPF, BGP)-生成路由表
    - 转发：从输入到输出链路交换数据报-根据路由表进行分组的转发

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001103919273.png" />

注：输入/出端口的三个块代表网络层（红色）、链路层、物理层      
注2：输入/出端口通常是整合在一起的，分开描述是为了方便

输入端口
- 输入端口功能：物理层链路上的物理信号转换为数字信号，数据链路层封装成帧并进行一定的判断，将帧当中的数据部分取出，交给网络层实体

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001104327835.png" />

- 输入端口需要有一个队列——输入端口缓存：下层交上来的速度于与交给分组交换结构的速度可能不匹配
    -  当交换机构的速率小于输入端口的汇聚速率时，在输入端口可能要排队
          - 排队延迟以及由于输入缓存溢出造成丢失！
    - Head-of-the-Line (HOL) blocking：排在队头的数据报阻止了队列中其他数据报向前移动

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001104653702.png" />

交换结构：将分组从输入缓冲区传输到合适的输出端口
- 交换速率：分组可以按照该速率从输入传输到输出
    - 运行速度经常是输入/输出链路速率的若干倍
    - N个输入端口：交换机构的交换速度是输入线路速度的N倍比较理想，才不会成为瓶颈
- 3种典型的交换机构：memory, bus, crossbar

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001104817961.png" />

    - 通过内存交换（**memory**） —— 第一代路由器：
        - 在CPU直接控制下的交换，采用传统的计算机
        - 分组被拷贝到系统内存，CPU从分组的头部提取出目标地址，查找转发表，找到对应的输出端口，拷贝到输出端口
        - 转发速率被内存的带宽限制（数据报通过BUS两遍（进+出），系统总线本身就会成为瓶颈，速率低）
        - 一次只能转发一个分组

        <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001104907438.png" style="zoom:80%"/>

    - 通过总线交换（**bus**） —— 第二代路由器
        - 数据报通过共享总线，从输入端口转发到输出端口
        - 虽然相比于memory方式，只经过bus一次，交换速率大大提升，但是还是有问题 —— 总线竞争：交换速度受限于总线带宽
        - 1次处理一个分组
        - 1 Gbps bus, Cisco 1900； 32 Gbps bus, Cisco 5600；对于接入或企业级路由器，速度足够（但不适合区域或骨干网络）

        <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001104959142.png" />

    - 通过互联网络（**crossbar**等）的交换
        - 同时并发转发多个分组，克服总线带宽限制
        - Banyan(榕树)网络，crossbar(纵横)和其它的互联网络被开发，将多个处理器连接成多处理器
        - 当分组从端口A到达，转给端口Y；控制器短接相应的两个总线
        - 高级设计：将数据报分片为固定长度的信元，通过交换网络交换
        - Cisco12000：以60Gbps的交换速率通过互联网络

        <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001105151671.png" />

输出端口

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001105403564.png" />

- 当数据报从交换机构的到达速度比传输速率快就需要输出端口缓存（输出端口排队）
    - 假设交换速率 $R_{switch}$ 是 $R_{line}$ 的N倍（N：输入端口的数量）
    - 当多个输入端口同时向输出端口发送时，缓冲该分组（当通过交换网络到达的速率超过输出速率则缓存）
    - 排队带来延迟，由于输出端口缓存溢出则丢弃数据报

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001105440439.png" >

- 由**调度规则**选择排队的数据报进行传输（先来的不一定先传）
    - 调度：选择下一个要通过链路传输的分组
    - 调度策略：
        - FIFO (first in first out) scheduling：按照分组到来的次序发送（先到先服务）
            - 现实例子？
            - 丢弃策略：如果分组到达一个满的队列，哪个分组将会被抛弃？
                - tail drop：丢弃刚到达的分组（抛尾部）
                - priority：根据优先权丢失/移除分组
                - random：随机地丢弃/移除
        - 优先权调度：发送最高优先权的分组
            - 多类，不同类别有不同的优先权
                - 类别可能依赖于标记或者其他的头部字段，e.g. IP source/dest, port numbers, ds, etc.
                - 先传高优先级的队列中的分组，除非没有
                - 高（低）优先权中的分组传输次序：FIFO
                - 现实生活中的例子？

            <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001110210112.png" style="zoom:70%"/>

            如上图：只要有红的就不传绿的，直到红色传完才开始传绿的

        - Round Robin (RR) scheduling:
            - 多类
            - 循环扫描不同类型的队列，发送完一类的一个分组，再发送下一个类的一个分组，循环所有类
            - 现实例子？

            <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001111117490.png" style="zoom:70%"/>

            如上图：第一轮传完红的传绿的，第二轮传完绿的传红的，如此往复
        
        - Weighted Fair Queuing (WFQ): 
            - 一般化的Round Robin
            - 在一段时间内，每个队列得到的服务时间是： $(W_i/\sum{W_i}) * t$ ，和权重成正比
            - 每个类在每一个循环中获得不同权重的服务量
            - 现实例子？

            <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001111153165.png" style="zoom:70%"/>

            如上图：一个传输周期内，蓝色传输时间占 $40\%$ ，红色传输时间占 $40\%$ ，绿色传输时间占 $20\%$

### 4.3 IP：Internet Protocol

IP协议主要实现数据平面的转发功能

#### 4.3.1 数据报格式

主机，路由器中的网络层功能：

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001111457486.png" style="zoom:80%"/>

ICMP协议：信令协议（如Ping命令等）

IP数据报格式

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001111652067.png" />

#### 4.3.2 IP分片和重组(Fragmentation & Reassembly)

IP 分片和重组
- 网络链路有MTU（最大传输单元） —— 链路层帧所携带的最大数据长度
    - 不同的链路类型
    - 不同的MTU 
- 大的IP数据报在网络上被分片(“fragmented”)
    - 一个数据报被分割成若干个小的数据报
        - 相同的ID，知道属于同一个数据报
        - 不同的偏移量(offset)：小数据报的第一个字节在字节流中的位置除以8
        - 最后一个分片标记为0（fragflag标识位），其他分片的fragflag标识位标记为1
    - “重组”只在最终的目标主机进行（不占用路由器的资源）
    - IP头部的信息被用于标识，排序相关分片
    - 若某一片丢失，整个全部丢弃

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001133625648.png" style="zoom:60%"/>

> 例：
> 
> - $4000$ 字节数据报
>     - $20$ 字节头部
>     - $3980$ 字节数据
> - $MTU = 1500 bytes$
> - 第一片： $20$ 字节头部 + $1480$ 字节数据
>     - 偏移量： $0$
> - 第二片： $20$ 字节头部 + $1480$ 字节数据（ $1480$ 字节应用数据）
>     - 偏移量： $1480/8=185$
> - 第三片： $20$ 字节头部 + $1020$ 字节数据（应用数据）
>     - 偏移量： $2960/8=370$

#### 4.3.3 IPv4地址

IP 编址：引论
- IP地址：32位标示，对主机或者路由器的接口编址（注：标识的是接口而非主机）
- 接口：主机/路由器和物理链路的连接处
    - 路由器通常拥有多个接口（路由器连接若干个物理网络，在多个物理网络之间进行分组转发）
    - 主机也有可能有多个接口
    - IP地址和每一个接口关联
- 一个IP地址和一个接口相关联

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001135955479.png" style="zoom:60%"/>

Q：这些接口是如何连接的？     
A：有线以太网网口链接到以太网络交换机连接       
目前：无需担心一个接口是如何接到另外一个接口（中间没有路由器，一跳可达）

子网(Subnets)
- IP地址：
    - 子网部分（高位bits）
    - 主机部分（地位bits）
- 什么是子网(subnet)？
    - 一个子网内的节点（主机或者路由器）它们的**IP地址的高位部分相同**，这些节点构成的网络的一部分叫做子网
    - **无需路由器介入**，子网内各主机可以在物理上相互直接到达，在IP层面一跳可达（但是在数据链路层可能需要借助交换机）

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001142106457.png" style="zoom:60%"/>

子网判断方法：
- 要判断一个子网，将每一个接口从主机或者路由器上分开，构成了一个个网络的孤岛
- 每一个孤岛（网络）都是一个都可以被称之为subnet。

长途链路 —— 点到点的形式   如：中国到日本的链路    
计算机局域网  ——  多点连接的方式     

子网掩码： 11111111 11111111 11111111 00000000     
Subnet mask：/24

IP地址分类
- Class A：126 networks ( $2^7-2$ , 0.0.0.0 and 1.1.1.1 not available), 16 million hosts ( $2^{24}-2$ , 0.0.0.0 and 1.1.1.1 not available)
- Class B：16382 networks ( $2^{14}-2$ , 0.0.0.0 and 1.1.1.1 not available), 64 K hosts ( $2^{16}-2$ , 0.0.0.0 and 1.1.1.1 not available)
- Class C：2 million networks, 254 host ( $2^8-2$ , 0.0.0.0 and 1.1.1.1 not available)
- Class D：multicast
- Class E：reserved for future

*注：A、B、C类称为 单播地址 （发送给单个），D类称为 主播地址 （发送给特定的组的所有人）*

互联网中的路由通过网络号进行一个个子网的计算，以网络为单位进行传输，而非具体到单个主机

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001142823822.png" style="80%"/>

特殊IP地址
- 一些约定：
    - 子网部分：全为0---本网络
    - 主机部分：全为0---本主机
    - 主机部分：全为1---广播地址，这个网络的所有主机
- 特殊IP地址

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001142922347.png" />

内网（专用）IP地址
- 专用地址：地址空间的一部份供专用地址使用
- 永远不会被当做公用地址来分配，不会与公用地址重复
    - 只在局部网络中有意义，用来区分不同的设备
- 路由器不对目标地址是专用地址的分组进行转发
- 专用地址范围
    - Class A 10.0.0.0-10.255.255.255  MASK 255.0.0.0
    - Class B 172.16.0.0-172.31.255.255  MASK 255.255.0.0
    - Class C 192.168.0.0-192.168.255.255 MASK 255.255.255.0

IP 编址：CIDR(Classless InterDomain Routing, 无类域间路由)
- 子网部分可以在任意的位置，按需划分
- 地址格式：a.b.c.d/x，其中 x 是 地址中子网号的长度（网络号的长度）

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001143934822.png" style="zoom:80%"/>

如上图，根据子网掩码，前23位为网络号，后9位为主机号

子网掩码(subnet mask)
- 32bits , 0 or 1 in each bit
    - 1：bit位置表示子网部分
    - 0：bit位置表示主机部分（主机号在查询路由表时没有意义，路由信息的计算以网络为单位）
- 原始的A、B、C类网络的子网掩码分别是
    - A：255.0.0.0：11111111 00000000 0000000 00000000
    - B：255.255.0.0：11111111 11111111 0000000 00000000
    - C：255.255.255.0：11111111 11111111 11111111 00000000
- CIDR下的子网掩码例子：
    - 11111111 11111111 11111100 00000000
- 另外的一种表示子网掩码的表达方式
    - /# ： 例如 /22 表示前面22个bit为子网部分

转发表和转发算法
|Destination Subnet Num |Mask |Next hop |Interface|
|:---:|:---:|:---:|:---:|
|202.38.73.0 |255.255.255.192 |IPx |Lan1 |
|202.38.64.0 |255.255.255.192 |IPy |Lan2 |
|...|...|...|...|
|Default |- |IPz |Lan0 |
- 获得IP数据报的目标地址
- 对于转发表中的每一个表项
- 如 (IP Des addr) & (mask)== destination，则按照表项对应的接口转发该数据报
- 如果都没有找到，则使用默认表项，通过默认端口（通常是一个网络的出口路由器所对应的IP）转发数据报

主机如何获得一个IP地址?
- 系统管理员将地址配置在一个文件中
    - Wintel: control-panel -> network -> configuration -> tcp/ip -> properties
    - UNIX: /etc/rc.config
- DHCP(Dynamic Host Configuration Protocol)：从服务器中动态获得一个IP地址（以及子网掩码Mask（ 指示地址部分的网络号和主机号）、local name server（DNS服务器的域名和IP地址）、default getaway（第一跳路由器的IP地址（默认网关）））
    - “plug-and-play”，自动配置，接上即用；且只用在用户上网时分配IP地址，其余时间该IP可以被其他上网用户使用，提高效率

DHCP(Dynamic Host Configuration Protocol, 动态主机配置协议)
- 目标：允许主机在加入网络的时候，动态地从服务器那里获得IP地址：
    - 可以更新对主机在用IP地址的租用期——租期快到了
    - 重新启动时，允许重新使用以前用过的IP地址
    - 支持移动用户加入到该网络（短期在网）
- DHCP工作概况：
    - 主机上线时广播“DHCP discover” 报文（可选）（目标IP：255.255.255.255，进行广播）
    - DHCP服务器用 “DHCP offer”提供报文响应（可选）
    - 主机请求IP地址：发送 “DHCP request” 报文（这第二次握手是因为可能有多个DHCP服务器，要确认用哪一个）
    - DHCP服务器发送地址：“DHCP ack” 报文

DHCP client-server scenario

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001144822831.png" style="zoom:80%"/>

> DHCP实例：
> 
> <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001145225819.png" style="zoom:70%"/>
> 
> - 第一次握手
>     - 联网笔记本需要获取自己的IP地址，第一跳路由器地址和DNS服务器:采用DHCP协议
>     - DHCP请求被封装在UDP段中,封装在IP数据报中，封装在以太网的帧中
>     - 以太网帧在局域网范围内广播(dest: FFFFFFFFFFFF)，被运行DHCP服务的路由器收到
>     - 以太网帧解封装成IP，IP解封装成UDP，解封装成DHCP
>     - DHCP服务器生成DHCP ACK,包含客户端的IP地址，第一跳路由器的IP地址和DNS域名服务器的IP地址
>     - DHCP服务器封装的报文所在的帧转发到客户端，在客户端解封装成DHCP报文
>     - 客户端知道它自己的IP地址，DNS服务器的名字和IP地址，第一跳路由器的IP地址
> - 第二次握手 略

如何获得一个IP地址
- Q1：如何获得一个网络的子网部分？
    - A1：从ISP获得地址块中分配一个小地址块

> 例：     
> 
> ISP's block 11001000 00010111 00010000 00000000 200.23.16.0/20       
> *前20位为网络号，后12位为主机号*        
> Organization0 11001000 00010111 00010000 00000000 200.23.16.0/23           
> Organization1 11001000 00010111 00010010 00000000 200.23.18.0/23         
> Organization2 11001000 00010111 00010100 00000000 200.23.20.0/23          
> ......       
> Organization7 11001000 00010111 00011110 00000000 200.23.30.0/23       

- Q2：一个ISP如何获得一个地址块？
    - A2：ICANN(Internet Corporation for Assigned Names and Numbers)
        - 分配地址
        - 管理DNS
        - 分配域名，解决冲突

层次编址：路由聚集(route aggregation)
- 层次编址允许路由信息的有效广播

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001145630149.png" style="zoom:80%" />

层次编址：特殊路由信息(more specific routes)
- ISPs-R-Us拥有一个对组织1更加精确的路由
- 匹配冲突时候，采取的是最长前缀匹配（匹配最精确）

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001150738412.png" style="zoom:80%"/>

下面来看内网地址。因为内网地址无法路由到，所以通过NAT技术，出去时共用一个机构的IP地址，回来时再转换为内网地址。

NAT(Network Address Translation)

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001150949929.png" />

- 动机：本地网络只有一个有效IP地址：
    - 不需要从ISP分配一块地址，可用一个IP地址用于所有的（局域网）设备 —— 省钱
    - 可以在局域网改变设备的地址情况下而无须通知外界
    - 可以改变ISP（地址变化）而不需要改变内部的设备地址
    - 局域网内部的设备没有明确的地址，对外是不可见的 —— 安全
- 实现：NAT路由器必须：
    - 数据包外出：替换源地址和端口号为NAT IP地址和新的端口号，目标IP和端口不变
        - 远端的C/S将会用NAP IP地址，新端口号作为目标地址
    - 记住每个转换替换对（在NAT转换表中）
        - 源IP，端口 vs  NAP IP ，新端口
    - 数据包进入：替换目标IP地址和端口号，采用存储在NAT表中的mapping表项，用（源IP，端口）

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001152133538.png" style="zoom:70%"/>

*实际上就是用外网的某个IP代替内网里面的网络号*     
*出去的时候替换 原来IP 和 端口号*       
*进来的时候替换 目标IP 和 端口号*       

- 16-bit端口字段：
    - 6万多个同时连接，一个局域网！
- 对NAT是有争议的：
    - 路由器只应该对第3层做信息处理，而这里对端口号（4层）作了处理
    - 违反了end-to-end 原则
        - 端到端原则：复杂性放到网络边缘
            - 无需借助中转和变换，就可以直接传送到目标主机
        - NAT可能要被一些应用设计者考虑, eg, P2P applications
        - 外网的机器无法主动连接到内网的机器上
    - 地址短缺问题可以被IPv6 解决

同时，采用NAT技术，如果客户端需要连接在NAT后面的服务器，会出现NAT穿透问题：出去没问题，可以找得到服务器，但是若外面想进来和内网的主机通信确做不到，无法找到通信主机。如客户端需要连接地址为10.0.0.1的服务器，但是服务器地址10.0.0.1是LAN本地地址（客户端不能够使用其作为目标地址），整网只有一个外部可见地址：138.76.29.7       
有以下解决方案：
- 方案1：静态配置NAT：转发进来的对服务器特定端口连接请求
    - e.g. (123.76.29.7, port 2500) 总是转发到10.0.0.1 port 25000
- 方案2：Universal Plug and Play (UPnP)Internet Gateway Device (IGD) 协议。允许NATted主机可以：
    - 获知网络的公共IP地址(138.76.29.7)
    - 列举存在的端口映射
    - 增/删端口映射（在租用时间内）
    - i.e. 自动化静态NAT端口映射配置

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001152723380.png" />

- 方案3：中继(used in Skype)
    - NAT后面的服务器建立和中继的连接
    - 外部的客户端链接到中继
    - 中继在2个连接之间桥接

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001152732177.png" style="zoom:80%"/>

#### 4.3.4 IPv6

动机
- 初始动机：32-bit地址空间将会被很快用完
- 另外的动机：
    - 头部格式改变帮助加速处理和转发
        - TTL-1
        - 头部checksum
        - 分片
    - 头部格式改变帮助QoS 

IPv6数据报格式：
- 固定的40字节头部
- 数据报传输过程中，不允许分片，而是路由器返回一个错误报告告诉源主机分组太大了，需要源主机将分组变小一点

IPv6头部(Cont)
- Priority：标示流中数据报的优先级
- Flow Label：标示数据报在一个“flow.” （“flow”的概念没有被严格的定义）
- Next header标示上层协议

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001153026504.png" style="zoom:60%" />

和IPv4的其它变化
- Checksum：被移除掉，降低在每一段中的处理速度
- Options：允许，但是在头部之外，被 “Next Header” 字段标示
- ICMPv6：ICMP的新版本
- 附加了报文类型，e.g. “Packet Too Big”（IPv6无法切片）
- 多播组管理功能

从IPv4到IPv6的平移（过渡）
- 不是所有的路由器都能够同时升级的
- 没有一个标记日 “flag days”，在那一天全部宕机升级
- 在IPv4和IPv6路由器混合时，网络如何运转？
- 隧道：在IPv4路由器之间传输的IPv4数据报中携带IPv6数据报

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001153350960.png" />

隧道(Tunneling)

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001153500951.png" width=400/>      
<br>
<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001153521591.png" width=400/>

IPv6：应用
- Google估计：8%的客户通过IPv6访问谷歌服务
- NIST估计：全美国1/3的政府域支持IPv6 
- 估计还需要很长时间进行部署 
    - 20年以上！
    - 看看过去20年来应用层面的变化：WWW, Facebook, streaming media, Skype, … 
    - 为什么？

### 4.4 通用转发和SDN

之前介绍的路由大部分都是传统方式，下面来看通用转发和SDN的方式。

传统方式：1. 每台设备上既实现控制功能，又实现数据平面 2. 控制功能分布式实现 3. 路由表-粘连
- 传统方式的缺陷：
    - 垂直集成（每台路由器或其他网络设备，包括：1.专用的硬件、私有的操作系统；2.互联网标准协议(IP, RIP, IS-IS, OSPF, BGP)的私有实现；从上到下都由一个厂商提供（代价大、被设备上“绑架”“）） --> 昂贵、不便于创新的生态
    - 分布式、固化设备功能 --> 网络设备种类繁多
        - 交换机；防火墙；NAT；IDS；负载均衡设备
        - 未来：不断增加的需求和相应的网络设备
        - 需要不同的设备去实现不同的网络功能
            - 每台设备集成了控制平面和数据平面的功能
            - 控制平面分布式地实现了各种控制平面功能
            - 升级和部署网络设备非常困难
        - 无法改变路由等工作逻辑，设备基本上只能（分布式升级困难）按照固定方式工作，控制逻辑固化，无法实现流量工程等高级特性
        - 配置错误影响全网运行；升级和维护会涉及到全网设备：管理困难
        - 要增加新的网络功能，需要设计、实现以及部署新的特定设备，设备种类繁

考虑到以上缺点，在2005年前后，开始重新思考网络控制平面的处理方式：SDN
- 集中：远程的控制器集中实现控制逻辑，通过南向接口将流表发送给每个设备中的控制代理
- 远程：数据平面和控制平面的分离

SDN：逻辑上集中的控制平面
- 一个不同的（通常是远程）控制器和CA交互，控制器决定分组转发的逻辑（可编程），CA所在设备执行逻辑

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001155320593.png" style="zoom:90%"/>

SDN的主要思路
- 网络设备数据平面和控制平面分离
- 数据平面-分组交换机
    - 将路由器、交换机和目前大多数网络设备的功能进一步抽象成：按照流表（由控制平面设置的控制逻辑）进行PDU（帧、分组）的动作（包括转发、丢弃、拷贝、泛洪、阻塞）
    - 统一化设备功能：SDN交换机（分组交换机），执行控制逻辑
- 控制平面-控制器+网络应用
    - 分离、集中
    - 计算和下发控制逻辑：流表

SDN控制平面和数据平面分离的优势
- **水平集成**控制平面的开放实现（而非私有实现），创造出好的产业生态，促进发展
    - 分组交换机、控制器和各种控制逻辑网络应用app可由不同厂商生产，专业化，引入竞争形成良好生态
- **集中式**实现控制逻辑，网络管理容易：
    - 集中式控制器了解网络状况，编程简单，传统方式困难
    - 避免路由器的误配置
- 基于流表的匹配+行动的工作方式允许“**可编程的**”分组交换机
    - 实现流量工程等高级特性
    - 在此框架下实现各种新型（未来）的网络设备

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001155703049.png" style="zoom:60%"/>

流量工程：传统路由比较困难

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001160320932.png" style="zoom:64%"/>

Q1：网管如果需要u到z的流量走uvwz，x到z的流量走xwyz，怎么办？       
A1：需要定义链路的代价，流量路由算法以此运算（IP路由面向目标，无法操作）（或者需要新的路由算法）       
*链路权重只是控制旋钮，错！*

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001160555463.png" style="zoom:60%"/>

Q2：如果网管需要将u到z的流量分成2路：uvwz和uxyz（负载均衡），怎么办？（IP路由面向目标）      
A2：无法完成（在原有体系下只有使用新的路由选择算法，而在全网部署新的路由算法是个大的事情）      

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001160622576.png" style="zoom:56%"/>

Q3：如果需要w对蓝色的和红色的流量采用不同的路由，怎么办？       
A3：无法操作（基于目标的转发，采用LS，DV路由）

SDN特点

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001160657605.png" />

SDN架构
- 数据平面交换机
    - 快速，简单，商业化交换设备采用硬件实现通用转发功能
    - 流表被控制器计算和安装
    - 基于南向API（例如OpenFlow），SDN控制器访问基于流的交换机
        - 定义了哪些可以被控制哪些不能
    - 也定义了和控制器的协议（e.g., OpenFlow）
- SDN控制器（网络OS）： 
    - 维护网络状态信息
    - 通过上面的北向API和网络控制应用交互
    - 通过下面的南向API和网络交换机交互
    - 逻辑上集中，但是在实现上通常由于性能、可扩展性、容错性以及鲁棒性在物理上采用分布式方法
- 网络控制应用：
    - 控制的大脑：采用下层提供的服务（SDN控制器提供的API），实现网络功能
        - 路由器 交换机
        - 接入控制 防火墙
        - 负载均衡
        - 其他功能
    - 非绑定：可以被第三方提供，与控制器厂商以通常上不同，与分组交换机厂商也可以不同

通用转发和SDN：每个路由器包含一个流表（被逻辑上集中的控制器计算和分发）

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001161538845.png" style="zoom:80%"/>

OpenFlow数据平面抽象
- 流：由分组（帧）头部字段所定义
- 通用转发：简单的分组处理规则
    - 模式(pattern)：将分组头部字段和流表进行匹配（路由器中的流表定义了路由器的匹配+行动规则（流表由控制器计算并下发））
    - 行动(action)：对于匹配上的分组，可以是丢弃、转发、修改、将匹配的分组发送给控制器
    - 优先权Priority：几个模式匹配了，优先采用哪个，消除歧义
    - 计数器Counters：#bytes 以及 #packets

OpenFlow: 流表的表项结构

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001161724509.png" />

OpenFlow抽象
- match + action：统一化各种网络设备提供的功能 *目前几乎所有的网络设备都可以在这个 匹配+行动 模式框架进行描述，具体化为各种网络设备包括未来的网络设备*
- 路由器
    - match：最长前缀匹配
    - action：通过一条链路转发
- 交换机
    - match：目标MAC地址
    - action：转发或者泛洪
- 防火墙
    - match：IP地址和TCP/UDP端口号
    - action：允许或者禁止
- NAT
    - match：IP地址和端口号
    - action：重写地址和端口号

> OpenFlow例子
> 
> <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211001161835426.png" style="zoom:70%"/>

### 4.5 总结

- 导论
    - 数据平面
    - 控制平面
- 路由器组成
- IP: Internet Protocol
    - 数据报格式
    - 分片
    - IPv4地址
    - NAT：网络地址转换
    - IPv6
- 通用转发和SDN
    - SDN架构
    - 匹配
    - 行动
    - OpenFLow有关“匹配+行动”的运行实例
- 问题：转发表（基于目标的转发）和流表（通用转发）是如何计算出来的？
    - 答案：通过控制平面，详见chapter5
