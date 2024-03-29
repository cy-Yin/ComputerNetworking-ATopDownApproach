# 计算机网络——自顶向下方法 7th

中国科学技术大学 郑烇教授 2020年秋季 自动化系

## 6. 链路层和局域网

网络层解决了一个网络如何到达另外一个网络的路由问题。在**一个网络内部**如何**由一个节点（主机或者路由器）到达另外一个相邻节点**则需要用到链路层的**点到点**传输层功能

目标：
- 理解数据链路层服务的原理：
    - 检错和纠错
    - 共享广播信道：多点接入（多路访问）
    - 链路层寻址
    - LAN:以太网、WLAN、VLANs
    - 可靠数据传输，流控制：解决！
- 实例和各种链路层技术的实现

网络节点的连接方式：一个子网中的若干节点是如何连接到一起的？
- 点到点连接（广域），只有封装/解封装的功能
- 多点连接：（局域），“一发全收”，有寻址和MAC问题，链路层的功能更加复杂，有两种方式实现：
    - 通过共享型介质，如同轴电缆
    - 通过网络交换机

数据链路层和局域网
- WAN：网络形式采用点到点链路
    - 带宽大、距离远（延迟大）
    - 带宽延迟积大
    - 如果采用多点连接方式
        - 竞争方式：一旦冲突代价大
        - 令牌等协调方式：在其中协调节点的发送代价大
- 点到点链路的链路层服务实现非常简单，封装和解封装
- LAN一般采用多点连接方式
    - 连接节点非常方便
    - 接到共享型介质上（或网络交换机），就可以连接所有其他节点
- 多点连接方式网络的链路层功能实现相当复杂
    - 多点接入：协调各节点对共享性介质的访问和使用
    - 竞争方式：冲突之后的协调；
    - 令牌方式：令牌产生，占有和释放等

### 6.1 引论和服务

链路层：导论
- 一些术语：
    - 主机和路由器是**节点**（网桥和交换机也是）：**nodes**
    - 沿着通信路径，连接个相邻节点通信信道的是**链路**：**links**
        - 有线链路
        - 无线链路
        - 局域网，共享性链路
    - 第二层协议数据单元**帧frame**，封装数据报

数据链路层负责从一个节点通过链路将（**帧**中的）数据报发送到相邻的物理节点（一个子网内部的2节点）

链路层：点到点，传输帧        
网络层：端到端        
传输层：进程到进程，不可靠-->可靠       
应用层：交换报文，实现网络应用       

链路层：上下文
- 数据报（分组）在不同的链路上以不同的链路协议传送：
    - 第一跳链路：以太网
    - 中间链路：帧中继链路
    - 最后一跳802.11：
- 不同的链路协议提供不同的服务
    - e.g., 比如在链路层上提供（或没有）可靠数据传送

> 传输类比
> - 从Princeton到Lausanne
>     - 轿车：Princeton to JFK
>     - 飞机：JFK to Geneva
>     - 火车：Geneva to Lausanne
> - 旅行者 = 数据报 datagram
> - 交通段 = 通信链路 communication link
> - 交通模式 = 链路层协议：数据链路层和局域网protocol
> - 票务代理 = 路由算法 routing algorithm

链路层服务（一般化的链路层服务，不是所有的链路层都提供这些服务一个特定的链路层只是提供其中一部分的服务（子集））
- 成帧，链路接入：
    - 将数据报封装在帧中，加上帧头、帧尾部
    - 如果采用的是共享性介质，信道接入获得信道访问权
    - 在帧头部使用“MAC”（物理）地址来标示源和目的
        - 不同于IP地址
- 在（一个网络内）相邻两个节点完成可靠数据传递
    - 已经学过了（传输层）
    - 在低出错率的链路上（光纤和双绞线电缆）很少使用
    - 在无线链路经常使用：出错率高
        - Q：为什么在链路层和传输层都实现了可靠性
- 在相邻节点间（一个子网内）进行可靠的转发
    - 已经学习过（传输层）
    - 在低差错链路上很少使用（光纤，一些双绞线）
        - 出错率低，没有必要在每一个帧中做差错控制的工作，协议复杂
            - 发送端对每一帧进行差错控制编码，根据反馈做相应的动作
            - 接收端进行差错控制解码，反馈给发送端（ACK，NAK）
        - 在本层放弃可靠控制的工作，在网络层或者是传输层做可靠控制的工作，或者根本就不做可靠控制的工作
    - 在高差错链路上需要进行可靠的数据传送
        - 高差错链路：无线链路：
        - Q：为什么要在采用无线链路的网络上，链路层做可靠数据传输工作；还要在传输层做端到端的可靠性工作？
        - 原因：出错率高，如果在链路层不做差错控制工作，漏出去的错误比较高；到了上层如果需要可靠控制的数据传输代价会很大
            - 如不做local recovery工作，总体代价大
- 流量控制：
    - 使得相邻的发送和接收方节点的速度匹配
- 错误检测：
    - 差错由信号衰减和噪声引起
    - 接收方检测出的错误： 
        - 通知发送端进行重传或丢弃帧
- 差错纠正：
    - 错误不太严重时，接收端检查和根据网络编码纠正bit错误，不通过重传来纠正错误
- 半双工和全双工：
    - 半双工：链路可以双向传输，但一次只有一个方向

链路层在哪里实现？
- 在每一个主机上，网卡实现链路层和物理层的功能
    - 也在每个路由器上，插多个网卡，实现链路层和相应物理层的功能
    - 交换机的每个端口上
- 链路层功能在“适配器”上实现(也叫 network interface card, NIC) 或者在一个芯片组上
    - 以太网卡，802.11网卡；以太网芯片组
    - 实现链路层和相应的物理层功能
- 接到主机的系统总线上
- 硬件、软件和固件的综合体

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211002224550874.png" style="zoom:60%" />

适配器（网卡）通信
- 发送方：
    - 在帧中封装数据报
    - 加上差错控制编码，实现RDT和流量控制功能等
    - 交给物理层打出
- 接收方
    - 从物理层接收bit
    - 检查有无出错，执行rdt和流量控制功能等
    - 解封装数据报，将帧交给上层

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211002224607535.png" style="zoom:60%"/>

适配器是半自治的，实现了链路和物理层功能

### 6.2 差错检测和纠正

错误检测
- EDC = 差错检测和纠正位（冗余位）
- D = 数据由差错检测保护，可以包含头部字段
- 错误检测不是100%可靠的！
    - 协议会漏检一些错误，但是很少
    - 更长的EDC字段可以得到更好的检测和纠正效果

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211002224745844.png" style="zoom:60%"/>

奇偶校验
- 加一个校验位，使得整个出现的1的个数是奇数还是偶数，是奇数->奇校验，是偶数->偶校验

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211002224811357.png" style="zoom:60%"/>

Internet校验和
- 目标：检测在传输报文段时的错误（如位翻转），（注：仅仅用在传输层）
- 发送方：
    - 将报文段看成16-bit整数
    - 报文段的校验和：和（1’的补码和）
    - 发送方将checksum的值放在“UDP校验和”字段
- 接收方：
    - 计算接收到的报文段的校验和
    - 检查是否与携带校验和字段值一致：
        - 不一致：检出错误
        - 一致：没有检出错误，但可能还是有错误
- 有更简单的检查方法 —— 全部加起来看是不是全1

检验和：CRC（循环冗余校验）
1. 模2运算（加法不进位，减法不借位，位和位之间没有关系）：同0异1，异或运算
2. 位串的两种表示：位串 or 多项式 的表示方式
    $$1011 \iff 1 * x^3 + 0 * x^2 + 1 * x^1 + 1 * x^0 = x^3 + x + 1$$
3. 生成多项式：r次方（r+1位）
4. 约定：在发送方发送的D位数据比特后附上r位的冗余位R（R是余数，具体见下），使得序列正好被生成多项式整除，则没有出错
- 强大的差错检测码
- 将数据比特D，看成是二进制的数据
- 生成多项式G：双方协商r+1位模式（r次方）
- 生成和检查所使用的位模式
- 目标：选择r位CRC附加位R，使得
    - <D,R> 正好被G整除 (mod 2) 
- 接收方知道G，将<D,R>除以G。如果非0余数：检查出错误！
- 能检出所有少于r+1位的突发错误
- 实际中广泛使用（以太网、802.11 WiFi、ATM）

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211002225357330.png" style="zoom:60%"/>

CRC例子
- 需要： $\text{D} * 2^r \text{ XOR R} = n\text{G}$
- 等价于： $\text{D} * 2^r = n\text{G } \text{XOR R} $
- 等价于：两边同除G，得到余数R
    $$R = \text{remainder}[\frac{\text{D} * 2^r}{\text{G}}]$$
    其中 remainder 表示余数运算，当余数R不足r位时进行补0

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211002230858718.png" style="zoom:60%"/>

RC性能分析
- 突发错误和突发长度
- CRC检错性能描述
- 能够检查出所有的1bit错误
- 能够检查出所有的双bits的错误
- 能够检查出所有长度小于等于r位的错误
- 出现长度为r+1的突发错误，检查不出的概率是 $\frac{1}{2^{r-1}}$
- 出现长度大于r+1的突发错误，检查不出的概率是 $\frac{1}{2^r}$

### 6.3 多点访问协议

点到点不存在多点访问的问题（两个访问端都确定好了），多点连接则需要考虑。

多路访问链路和协议
- 两种类型的链路（一个子网内部链路连接形式）：
    - 点对点
        - 拨号访问的PPP
        - 以太网交换机和主机之间的点对点链路
    - 广播（共享线路或媒体），也称为多点连接的网络
        - 传统以太网（同轴电缆连接所有节点，所有节点通过比较MAC地址确认帧发送的目标地址）
        - HFC上行链路
        - 802.11无线局域网

多路访问协议（介质访问控制协议：MAC）
- 单个共享的广播型链路
- 2个或更多站点同时传送：冲突(collision)
    - 多个节点在同一个时刻发送，则会收到2个或多个信号叠加
- 分布式算法-决定节点如何使用共享信道，即：决定节点什么时候可以发送？
- 关于共享控制的通信必须用借助信道本身传输！
    - 没有带外的信道，只有这一个信道，各节点使用其协调信道使用
    - 用于传输控制信息

理想的多路访问协议
- 给定：Rbps的广播信道
- 必要条件：
    1. 当一个节点要发送时，可以R速率发送 —— 满速。
    2. 当M个节点要发送，每个可以以R/M的平均速率发送 —— 公平、均分
    3. 完全分布的：
          - 没有特殊节点协调发送
          - 没有时钟和时隙的同步
    4. 简单

MAC(媒体访问控制)协议：分类：3大类：
- 信道划分(partition)
    - 把信道划分成小片（时间、频率、编码）
    - 分配片给每个节点专用
- 随机访问(random)：“想用就用”
    - 信道不划分，允许冲突/碰撞
    - 检测冲突，冲突后恢复
- 依次轮流：分为 完全分布式的（令牌方式） 和 主节点协调式的（主节点轮流询问）
    - 节点依次轮流
    - 但是有很多数据传输的节点可以获得较长的信道使用权

a. 信道划分MAC协议
- TDMA(time division multiple access)分时复用
    - 轮流使用信道，信道的时间分为周期
    - 每个站点使用每周期中固定的时隙（长度=帧传输时间）传输帧
    - 如果站点无帧传输，时隙空闲->浪费
    - 如：6站LAN，1、3、4有数据报，时隙2、5、6空闲
- FDMA(frequency division multiple access)频分复用
    - 信道的有效频率范围被分成一个个小的频段
    - 每个站点被分配一个固定的频段
    - 分配给站点的频段如果没有被使用，则空闲
    - 例如：6站LAN，1、3、4有数据报，频段2、5、6空闲
- CDMA(code division multiple access)码分复用
    - 有站点在整个频段上同时进行传输，采用编码原理加以区分
    - 完全无冲突
    - 假定：信号同步很好，线性叠加
- 比方
    - TDM：不同的人在不同的时刻讲话
    - FDM：不同的组在不同的小房间里通信
    - CDMA：不同的人使用不同的语言讲话

b. 随机存取协议
- 当节点有帧要发送时
    - 以信道带宽的全部Rbps发送
    - 没有节点间的预先协调
- 两个或更多节点同时传输，会发生->冲突“collision”
- 随机存取协议规定: 
    - 如何检测冲突
    - 如何从冲突中恢复（如：通过稍后的重传）
    - 随机MAC协议：
        - 时隙ALOHA
        - 纯ALOHA（非时隙）
        - CSMA, CSMA/CD, CSMA/CA

b.1 时隙ALOHA
- 假设
    - 所有帧是等长的，能够持续一个时隙
    - 时间被划分成相等的时隙/时槽，每个时隙可发送一帧
    - 节点只在时隙开始时发送帧
    - 共享信道的所有节点在时钟上是同步的
    - 如果两个或多个节点在一个时隙传输，所有的站点都能检测到冲突
- 运行
    - 当节点获取新的帧，在下一个时隙传输
    - 传输时没有检测到冲突（可从信道内的信息能量的幅度判断），成功
        - 节点能够在下一时隙发送新帧
    - 检测时如果检测到冲突，失败
        - 节点在每一个随后的时隙以概率p重传帧直到成功（可能仍然发生冲突，但是时间越长，冲突概率越低）
- 优点
    - 节点可以以信道带宽全速连续传输
    - 高度分布：仅需要节点之间在时隙上的同步
    - 简单
- 缺点
    - 存在冲突，浪费时隙
    - 即使有帧要发送，仍然有可能存在空闲的时隙
    - 节点检测冲突的时间 小于 帧传输的时间
        - 必须传完
    - 需要时钟上同步

时隙ALOHA的效率(Efficiency)      
注：效率：当有很多节点，每个节点有很多帧要发送时，x%的时隙是成功传输帧的时隙    
- 假设N个节点，每个节点都有很多帧要发送，在每个时隙中的传输概率是 $p$
- 一个节点成功传输概率是 $p(1-p)^{N-1}$
- 任何一个节点的成功概率是 $N * p(1-p)^{N-1}$
- $N$ 个节点的最大效率：求出使 $f(P) = N * p(1-p)^{N-1}$ 最大的 $p^{ * }$
- 代入 $p^{ * }$ 得到最大 $f(p^{ * }) = N * p^{ * }(1-p^{ * })^{N-1}$ 
- $N$ 为无穷大时的极限为 $1/e=0.37$ ，即最好情况：信道利用率 $37$ %

b.2 纯ALOHA（非时隙）：数据帧一形成立即发送
- 无时隙ALOHA：简单、无须节点间在时间上同步
- 当有帧需要传输：马上传输
- 冲突的概率增加:
    - 帧在 $t_0$发送，和其它在 $[t_0-1, t_0+1]$ 区间内开始发送的帧冲突
    - 和当前帧冲突的区间（其他帧在此区间开始传输）增大了一倍

纯ALOHA的效率

$$
\begin{split}
P(\text{指定节点成功}) &= P(\text{节点传输}) \times \\ 
&\quad P(\text{其它节点在 $[t_0-1, t_0]$ 不传}) \times \\ 
&\quad P(\text{其它节点在 $[t_0, t_0+1\text{不传}]$ }) \\ 
&= p(1-p)^{N-1}(1-p)^{N-1} \\ 
&= p(1-p)^{2(N-1)}
\end{split}
$$

选择最佳的 $p$ 且 $N$ 趋向无穷大时，效率为 $1/(2e) = 17.5$ %，效率比时隙ALOHA更差了！

如何提升 纯ALOHA 的效率？CSMA

b.3 CSMA(载波侦听多路访问) —— “说之前听”
- Aloha：如何提高ALOHA的效率
    - 发之前不管有无其他节点在传输
- CSMA：在传输前先侦听信道：
    - 如果侦听到信道空闲，传送整个帧
    - 如果侦听到信道忙，推迟传送
    - 人类类比：不要打断别人正在进行的说话！

CSMA冲突
- 冲突仍然可能发生：
    - 由传播延迟造成：两个节点可能侦听不到正在进行的传输
- 冲突：
    - 整个冲突帧的传输时间都被浪费了，是无效的传输
- 注意：
    - 传播延迟（距离）决定了冲突的概率

本质上是节点依据本地的信道使用情况来判断全部信道的使用情况。         
距离越远，延时越大，发生冲突的可能性就越大

可以改进CSMA --> CSMA/CD（目前有形介质的局域网如“以太网”采用的方式

b.4 CSMA/CD(冲突检测) —— “边说边听” 
- 载波侦听CSMA：和在CSMA中一样发送前侦听信道
- 没有传完一个帧就可以在短时间内检测到冲突
- 冲突发生时则传输终止，减少对信道的浪费
- 冲突检测CD技术，有线局域网中容易实现：
    - 检测信号强度，比较传输与接收到的信号是否相同
    - 通过周期的过零点检测
- 人类类比：礼貌的对话人

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003010859719.png" style="zoom:80%"/>

以太网CSMA/CD算法
1. 适配器获取数据报，创建帧
2. 发送前：侦听信道CS
    - 闲：开始传送帧
    - 忙：一直等到闲再发送
3. 发送过程中，冲突检测CD
    - 没有冲突：成功
    - 检测到冲突：放弃，之后尝试重发
4. 发送方适配器检测到冲突，除放弃外，还发送一个Jam信号，所有听到冲突的适配器也是如此
    - 强化冲突：让所有站点都知道冲突（如何实现：信号强度大，持续时间长） 强化冲突的原因：放弃的信号可能持续时间很短，其他节点可能会接收不到，认为没有发生冲突，导致接受失败
5. 如果放弃，适配器进入指数退避状态 *exponential backoff 二进制指数退避算法*
    - 在第m次失败后，适配器随机选择一个{ 0，1，2，……，2^m-1}中的K，等待K*512位时，然后转到步骤2
    - 此时若两个站点继续选择了同一个K，则在K*512位时两者又同时重发，又会产生冲突
    - 随着m的增大，成功的概率越来越大，但是平均等待时间会变长
    - 注：指数退避：
        - 目标：适配器试图适应当前负载（自适应算法），在一个变化的碰撞窗口中随机选择时间点尝试重发
            - 高负载（重传节点多）：重传窗口时间大，减少冲突，但等待时间长
            - 低负载（重传节点少）：使得各站点等待时间少，但冲突概率大

CSMA/CD效率
- $t_{prop}$ 为LAN上2个节点的最大传播延迟
- $t_{trans}$ 为传输最大帧的时间
- 则：     
    
    $$ efficiency = \frac{1}{1 + 5 * t_{prop} / t_{trans}} $$

- 效率变为 $1$ ：
    - 当 $t_{prop}$ 变成 $0$ 时
    - 当 $t_{trans}$ 变成无穷大时
- 比ALOHA更好的性能，而且简单，廉价，分布式！

b.5 无线局域网CSMA/CA

WLAN由于是无线形式，更加倾向于选择CSMA/CA

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003011006144.png" style="zoom:70%"/>

无线局域网中的 MAC：CSMA/CA —— 冲突控制
- 冲突： $2^+$ 站点（AP或者站点）在同一个时刻发送
- 802.11：CSMA —— 发送前侦听信道，实现事先避免冲突
    - 不会和其它节点正在进行的传输发生冲突
- 802.11：没有冲突检测！
    - 无法检测冲突：自身信号远远大于其他节点信号（无线情况下，电磁波信号成平方反比衰减）
    - 即使能CD：不冲突 $\neq$ 成功 （有 隐藏终端 的问题：A的电磁波信号到达B时，C与A的距离比B与A的距离远，故此时电磁波到达不了C，即检测不到冲突，但是B周边会有A、C的电磁波的叠加干扰），同时 冲突 $\neq$ 不成功
    - 目标：avoid collisions：CSMA/C(ollision)A(voidance)
        - 无法CD，一旦发送一股脑全部发送完毕，不CD
        - 为了避免无CD带来的信道利用率低的问题，事前进行冲突避免

无线局域网：CSMA/CA
- 发送方
    - 如果站点侦测到信道空闲持续DIFS长，则传输整个帧 (no CD)
    - 如果侦测到信道忙碌，那么 选择一个随机回退值，并在信道空闲时递减该值；如果信道忙碌，回退值不会变化；到数到0时（只生在信道闲时）发送整个帧。如果没有收到ACK，增加回退值，重复这段的整个过程
- 802.11 接收方
    - 如果帧正确，则在SIFS后发送ACK

（无线链路特性，需要每帧确认（有线网由于边发边确认，不需要接收ACK信息就可以知道是否发送成功）；例如：由于隐藏终端问题，在接收端可能形成干扰，接收方没有正确地收到。链路层可靠机制）

IEEE 802.11 MAC 协议: CSMA/CA
- 在count down时，侦听到了信道空闲为什么不发送，而要等到0时在发送？以下例子可以很好地说明这一点
    - 2个站点有数据帧需要发送，第三个节点正在发送
    - LAN CD：让2者听完第三个节点发完，立即发送
        - 冲突：放弃当前的发送，避免了信道的浪费于无用冲突帧的发送
        - 代价不昂贵
    - WLAN：CA
        - 无法CD，一旦发送就必须发完，如冲突信道浪费严重，代价高昂
        - 思想：尽量事先避免冲突，而不是在发生冲突时放弃然后重发
        - 听到发送的站点，分别选择随机值，回退到0发送
            - 不同的随机值，一个站点会胜利
            - 失败站点会冻结计数器，当胜利节点发完再发
- 无法完全避免冲突
    - 两个站点相互隐藏：
        - A,B 相互隐藏，C在传输
        - A,B选择了随机回退值
        - 一个节点如A胜利了，发送
        - 而B节点收不到，顺利count down到0 发送
        - A,B的发送在C附近形成了干扰
    - 选择了非常靠近的随机回退值：
        - A,B选择的值非常近
        - A到0后发送
        - 但是这个信号还没到达B时
        - B也到0了，发送
        - 冲突

冲突避免：RTS-CTS交换 —— 对长帧的可选项
- 思想：允许发送方“预约”信道，而不是随机访问该信道：避免长数据帧的冲突（可选项）
- 发送方首先使用CSMA向BS发送一个小的RTS分组
    - RTS可能会冲突（但是由于比较短，浪费信道较少）
- BS广播 clear-to-send CTS，作为RTS的响应
- CTS能够被所有涉及到的节点听到
    - 发送方发送数据帧
    - 其它节点抑制发送

采用小的预约分组，可以完全避免数据帧的冲突

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003011156385.png" style="zoom:70%"/>

b.6 线缆接入网络 —— 有线电视公司提供

- 多个40Mbps下行（广播）信道，FDM
    - 下行：通过FDM分成若干信道，互联网、数字电视等
    - 互联网信道：只有1个用户（不存在竞争） —— CMTS在其上传输，将数据往下放
- 多个30Mbps上行的信道，FDM
    - 多路访问：所有用户使用；接着TDM分成微时隙
    - 部分时隙：分配（预约）；部分时隙：竞争；

DOCSIS：data over cable service interface spec 
- 采用FDM进行信道的划分：若干上行、下行信道
- 下行信道：
    - 在下行MAP帧中：CMTS告诉各节点微时隙分配方案，分配给各站点的上行微时隙
    - 另外：头端传输下行数据（给各个用户）
- TDM上行信道
    - 采用TDM的方式将上行信道分成若干微时隙：MAP指定
    - 站点采用分配给它的微时隙上行数据传输：分配
    - 在特殊的上行微时隙中，各站点请求上行微时隙：竞争
        - 各站点对于该时隙的使用是随机访问的
        - 一旦碰撞（请求不成功，结果是：在下行的MAP中没有为它分配，则二进制退避）选择时隙上传输

c. 轮流(Taking Turns)MAC协议
- 信道划分MAC协议：固定分配、平分
    - 共享信道在高负载时是有效和公平的
    - 在低负载时效率低下
        - 只能等到自己的时隙开始发送或者利用1/N的信道频率发送
        - 当只有一个节点有帧传时，也只能够得到1/N个带宽分配
- 随机访问MAC协议
    - 在低负载时效率高：单个节点可以完全利用信道全部带宽
    - 高负载时：冲突开销较大，效率极低，时间很多浪费在冲突中
- 轮流协议
    - 有2者的优点
    - 缺点：复杂

轮流MAC协议
- 轮询：（本身有一个主节点）
    - 主节点邀请从节点依次传送
    - 从节点一般比较“dumb”
    - 缺点：
        - 轮询开销：轮询本身消耗信道带宽
        - 等待时间：每个节点需等到主节点轮询后开始传输，即使只有一个节点，也需要等到轮询一周后才能够发送
        - 单点故障 <-- 本身可靠性差：主节点失效时造成整个系统无法工作
- 令牌传递：（没有主节点）
    - 控制令牌(token)循环从一个节点到下一个节点传递 （“击鼓传花”）。如果令牌到达的节点需要发送信息，就将令牌位置位为0，将令牌帧变为数据帧，发送的数据绕行一周后再由自己收下（为什么不是由目标节点收下？“一发多收”，目标节点有多个，如果由目标节点收下会导致后面的目标节点收不到，所以需要轮转一圈，确认经过了所有节点后由自己收下）
    - 令牌报文：特殊的帧
    - 缺点：
        - 令牌开销：本身消耗带宽
        - 延迟：只有等到抓住令牌，才可传输
        - 单点故障(token)：
            - 令牌丢失系统级故障，整个系统无法传输
            - 复杂机制重新生成令牌

MAC协议总结
- 多点接入问题：对于一个共享型介质，各个节点如何协调对它的访问和使用？
    - 信道划分：按时间、频率或者编码
        - TDMA、FDMA、CDMA
    - 随机访问（动态）
        - ALOHA, S-ALOHA, CSMA, CSMA/CD
        - 载波侦听：在有些介质上很容易（wire：有线介质），但在有些介质上比较困难（wireless：无线）
        - CSMA/CD：802.3 Ethernet网中使用
        - CSMA/CA：802.11WLAN中使用
    - 依次轮流协议
        - 集中：由一个中心节点轮询；分布：通过令牌控制
        - 蓝牙、FDDI、令牌环

### 6.4 LANS

#### 6.4.1 addressing, ARP

- MAC地址和ARP
    - 32bit IP地址：
        - 网络层地址
        - 前n-1跳：用于使数据报到达目的IP子网 —— IP地址的网络号部分
        - 最后一跳：到达子网中的目标节点 —— IP地址的主机号部分
    - LAN（MAC/物理/以太网）地址：
        - 用于使帧从一个网卡传递到与其物理连接的另一个网卡（在同一个物理网络中）
        - 48bit MAC地址固化在适配器的ROM，有时也可以通过软件设定
        - 理论上全球任何2个网卡的MAC地址都不相同
        - e.g., 1A-2F-BB-76-09-AD <-- 16进制表示（每一位代表4个bits）

网络地址和mac地址分离
- IP地址和MAC地址的作用不同
    - a) IP地址是分层的
        - 一个子网所有站点网络号一致，路由聚集，减少路由表
            - 需要一个网络中的站点地址网络号一致，如果捆绑需要定制网卡非常麻烦
        - 希望网络层地址是配置的；IP地址完成网络到网络的交付
    - b) mac地址是一个平面的
        - 网卡在生产时不知道被用于哪个网络，因此给网卡一个唯一的标示，用于区分一个网络内部不同的网卡即可
        - 可以完成一个物理网络内部的节点到节点的数据交付网络地址和mac地址分离
- 分离好处
    - a) 网卡坏了，ip不变，可以捆绑到另外一个网卡的mac上
    - b) 物理网络还可以除IP之外支持其他网络层协议，链路协议为任意上层网络协议，如IPX等
- 捆绑的问题
    - a) 如果仅仅使用IP地址，不用mac地址，那么它仅支持IP协议
    - b) 每次上电都要重新写入网卡IP地址；
    - c) 另外一个选择就是不使用任何地址；不用MAC地址，则每到来一个帧都要上传到IP层次，由它判断是不是需要接受，干扰一次

> 假设网络上要将一个数据包（名为PAC）由北京的一台主机（名称为A，IP地址为IP_A，MAC地址为MAC_A）发送到华盛顿的一台主机（名称为B，IP地址为IP_B，MAC地址为MAC_B）。       
> 这两台主机之间不可能是直接连接起来的，因而数据包在传递时必然要经过许多中间节点（如路由器，服务器等等），我们假定在传输过程中要经过C1、C2、C3（其MAC地址分别为M1，M2，M3）三个节点。          
> A在将PAC发出之前，先发送一个ARP请求，找到其要到达IP_B所必须经历的第一个中间节点C1的MAC地址M1，然后在其数据包中封装（Encapsulation）这些地址：IP_A、IP_B，MAC_A和M1。当PAC传到C1后，再由ARP根据其目的IP地址IP_B，找到其要经历的第二个中间节点C2的MAC地址M2，然后再将带有M2的数据包传送到C2。如此类推，直到最后找到带有IP地址为IP_B的B主机的地址MAC_B，最终传送给主机B。

LAN地址和ARP
- 局域网上每个适配器都有一个唯一的LAN地址

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003091929111.png" style="zoom:80%"/>

- MAC地址由IEEE管理和分配
- 制造商购入MAC地址空间（保证唯一性）
- 类比：
    - (a)MAC地址：社会安全号、身份证号码
    - (b)IP地址：通讯地址、住址
- MAC平面地址 --> 支持移动
    - 可以将网卡到接到其它网络
- IP地址有层次 --> 不能移动
    - 依赖于节点连接的IP子网，与子网的网络号相同（有与其相连的子网相同的网络前缀）

ARP(Address Resolution Protocol)
- 问题：已知B的IP地址，如何确定B的MAC地址？ARP协议
    - 在LAN上的每个IP节点都有一个ARP表
    - ARP表：包括一些LAN节点IP/MAC地址的映射
        `<IP address; MAC address; TTL>`
        - TTL时间是指地址映射失效的时间，典型是20min。20min内直接使用缓存 —— 高效；20min后删除 —— 保持最新

ARP协议：在同一个LAN (网络)
- A要发送帧给B（B的IP地址已知），但B的MAC地址不在A的ARP表中
- A广播包含B的IP地址的ARP查询包
    - Destination MAC address = FF-FF-FF-FF-FF-FF
    - LAN上的所有节点都会收到该查询包
- B接收到ARP包，回复A自己的MAC地址
    - 帧发送给A
    - 用A的MAC地址（单播）
- A在自己的ARP表中，缓存IP-to-MAC地址映射关系，直到信息超时
    - 软状态：靠定期刷新维持的系统状态
    - 定期刷新周期之间维护的状态信息可能和原有系统不一致
- ARP是即插即用的
    - 节点自己创建ARP的表项
    - 无需网络管理员的干预、配置和操作

> 例：路由到其他LAN
> - Walkthrough：发送数据报：由A通过R到B，假设A知道B的IP地址
> - 在R上有两个ARP表，分别对应两个LAN
> - 在源主机的路由表中，发现到目标主机的下一跳时111.111.111.110
> - 在源主机的ARP表中，发现其MAC地址是E6-E9-00-17-BB-4B, etc
> 
> <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003092755106.png" style="zoom:60%"/>
> 
> - 编址：
>     - A创建数据报，源IP地址：A；目标IP地址：B 
>     - A创建一个链路层的帧，目标MAC地址是R，该帧包含A到B的IP数据报
>     - 帧从A发送到R
>     - 帧被R接收到，从中提取出IP分组，交给上层IP协议实体
>     - R转发数据报，数据报源IP地址为A，目标IP地址为B
>     - R创建一个链路层的帧，目标MAC地址为B，帧中包含A到B的IP数据报

#### 6.4.2 Ethernet

以太网
- 目前最主流的LAN技术：98%占有率
- 廉价：30元RMB 100Mbps！
- 最早广泛应用的LAN技术
- 比令牌网和ATM网络简单、廉价
- 带宽不断提升：10M, 100M, 1G, 10G

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003093457375.png" style="zoom:60%"/>

以太网：物理拓扑
- 总线：在上个世纪90年代中期很流行
    - 所有节点在一个碰撞域内，一次只允许一个节点发送
    - 可靠性差，如果介质破损（总线长，破损概率大），截面形成信号的反射，发送节点误认为是冲突，总是冲突 —— 需要中继器吸收电磁能量
- 星型：目前最主流
    - 连接选择：hub 或者 switch 
    - 现在一般是交换机在中心
    - 每个节点以及相连的交换机端口使用（独立的）以太网协议（不会和其他节点的发送产生碰撞）

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003093613325.png" style="zoom:60%" />

以太帧结构
- 发送方适配器在以太网帧中封装IP数据报，或其他网络层协议数据单元

|preamble|destination address|source address|type|data(payload)|CRC|
|:---:|:---:|:---:|:---:|:---:|:---:|

- 前导码：
- 7B 10101010 + 1B 10101011
- 用来同步接收方和发送方的时钟速率
    - 使得接收方将自己的时钟调到发送端的时钟
    - 从而可以按照发送端的时钟来接收所发送的帧
- 地址：6字节源MAC地址，目标MAC地址
    - 如：帧目标地址=本站MAC地址，或是广播地址，接收，递交帧中的数据到网络层
    - 否则，适配器忽略该帧
- 类型：指出高层协（大多情况下是IP，但也支持其它网络层协议Novell IPX和AppleTalk）
- CRC：在接收方校验
    - 如果没有通过校验，丢弃错误帧

以太网：无连接、不可靠的服务（有形介质，出错概率较低）
- 无连接：帧传输前，发送方和接收方之间没有握手
- 不可靠：接收方适配器不发送ACKs或NAKs给发送方
    - 递交给网络层的数据报流可能有gap
    - 如上层使用像传输层TCP协议这样的rdt，gap会被补上（源主机，TCP实体）
    - 否则，应用层就会看到gap
- 以太网的MAC协议：采用二进制退避的CSMA/CD介质访问控制形式

802.3 以太网标准：链路和物理层
- 很多不同的以太网标准
    - 相同的MAC协议（介质访问控制）和帧结构
    - 不同的速率：2Mbps、10Mbps 、100Mbps 、1Gbps、10Gbps
    - 不同的物理层标准
    - 不同的物理层媒介：光纤，同轴电缆和双绞线

以太网使用CSMA/CD
- 没有时隙
- NIC如果侦听到其它NIC在发送就不发送：载波侦听(carrier sense)
- 发送时，适配器当侦听到其它适配器在发送就放弃对当前帧的发送，冲突检测(collision detection)
- 冲突后尝试重传，重传前适配器等待一个随机时间，随机访问(random access)

*具体看上面的CSMA/CD部分*

以太网在低负载和高负载的情况下都较好。低负载时好是由于CDMA/CD，高负载时好是由于引入了交换机，端口可以并发

10BaseT and 100BaseT
- 100Mbps速率也被称之为“fast ethernet”
- T代表双绞线
- 节点连接到HUB上：“star topology”物理上星型
- 逻辑上总线型，盒中总线
- 节点和HUB间的最大距离是100m

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003095952932.png" style="zoom:80%"/>

Hubs
- Hubs本质上是物理层的中继器：
    - 从一个端口收，转发到所有其他端口
    - 速率一致
    - 没有帧的缓存
    - 在hub端口上没有CSMA/CD机制：适配器检测冲突
    - 提供网络管理功能

Manchester编码 —— 物理层
- 在10BaseT中使用
- 每一个bit的位时中间有一个信号跳变，传送1时信号周期的中间有一个向下的跳变，传送0时信号周期的中间有一个向上的跳变（为什么要跳变？为了在电磁波信号中将时钟信号通过一些简单的电路抽取出来）
- 允许在接收方和发送方节点之间进行时钟同步
    - 节点间不需要集中的和全局的时钟
- 10Mbps，使用20M带宽，效率50%
- Hey, this is physical-layer stuff!

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003100140814.png" style="zoom:60%"/>

100BaseT中的4b5b编码（5个bit代表4个bit）

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003102620272.png" style="zoom:60%"/>

千兆以太网
- 采用标准的以太帧格式
- 允许点对点链路和共享广播信道
- 物理编码：8b10b编码
- 在共享模式，继续使用CSMA/CD MAC技术，节点间需要较短距离以提高利用率
- 交换模式：全双工千兆可用于点对点链路
    - 站点使用专用信道，基本不会冲突，效率高
    - 除非发往同一个目标站点
- 10Gbps now!

#### 6.4.3 switches 链路层交换机

Hub：集线器 （星形）
- 网段(LAN segments)：可以允许一个站点发送的网络范围
    - 在一个碰撞域，同时只允许一个站点在发送（发之前先侦听，做信道检测）
    - 如果有2个节点同时发送，则会碰撞
    - 通常拥有相同的前缀，比IP子网更详细的前缀
- HUB可以级联，所有以hub连到一起的站点处在一个网段/碰撞域（一个碰撞域内一次只能有一个节点发送，两个站点同步发送会导致碰撞，会采用CSMA/CD的方式尝试再次重发）
    - 骨干hub将所有网段连到了一起
- 通过hub可扩展节点之间的最大距离
- 通过HUB，不能将10BaseT和100BaseT的网络连接到一起

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003102803772.png" style="zoom:60%"/>

高负载情况下，由于CSMA/CD的限制，一般选择将HUB升级为交换机。（HUB“一发全收”，交换机只会存储帧并转发给确定的端口“选择性转发”，并行性强）

交换机
- 链路层设备：扮演主动角色（端口执行以太网协议）
    - 对帧进行存储和转发
    - 对于到来的帧，检查帧头，根据目标MAC地址进行选择性转发（而HUB是“一发全收”）
    - 当帧需要向某个（些）网段进行转发，需要使用CSMA/CD进行接入控制
    - 通常一个交换机端口一个独立网段，允许多个节点同时发送，并发性强
    - 交换机也可以级联，多级结构中通过自学习连接源站点和目标站点
- 透明：主机对交换机的存在可以不关心
    - 通过交换机相联的各节点好像这些站点是直接相联的一样（因为交换机处于链路层，路由节点/主机处于网络层）
    - 有MAC地址；无IP地址
- 即插即用，自学习(self learning)：
    - 交换机无需配置

交换机：多路同时传输
- 主机有一个专用和直接到交换机的连接
- 交换机缓存到来的帧
- 对每个帧进入的链路使用以太网协议，没有碰撞；全双工
    - 每条链路都是一个独立的碰撞域
    - MAC协议在其中的作用弱化了，基本上就是一个交换设备
- 交换：A-to-A' 和 B-to-B' 可以同时传输，没有碰撞

交换机转发表（转发表是自学习的，不用网络管理员配置）
- Q：交换机如何知道通过接口1到达A，通过接口5到达B'？
    - A：每个交换机都有一个交换表 switch table，每个表项：
        - （主机的MAC地址，到达该MAC经过的接口，时戳）
        - 比较像路由表！
- Q：每个表项是如何创建的？如何维护的？
    - 有点像路由协议？

交换机：自学习
- 交换机通过学习得到哪些主机（mac地址）可以通过哪些端口到达
- 当接收到帧，交换机学习到发送站点所在的端口（网段）
- 在交换表中记录发送方MAC地址/进入端口映射关系（软状态维护：通过时戳，隔一段时间就删掉这个表项）

    <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003104914637.png" style="zoom:60%"/>

交换机：过滤／转发
- 当交换机收到一个帧：
    1. 记录进入链路，发送主机的MAC地址
    2. 使用目标MAC地址对交换表进行索引
    3. ```
       if entry found for destination{   // 选择性转发
           if dest on segment from which frame arrived{
               drop the frame // 过滤
           }
           else forward the frame on interface indicated // 转发
       }
       else flood // 泛洪：除了帧到达的网段，向所有网络接口发送
       ```

> 自学习，转发的例子：
> - 帧的目标：A'，不知道其位置在哪：泛洪
> - 知道目标A对应的链路：选择性发送到那个端口
> 
> <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003105023894.png" width=300/>
> <br>
> <img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003105040787.png" width=300/>

交换机 vs. 路由器
- 都是存储转发设备，但层次不同
    - 交换机：链路层设备（检查链路层头部）
    - 路由器：网络层设备（检查网络层的头部）
- 都有转发表：
    - 交换机：维护交换表，按照MAC地址转发
        - 执行过滤、自学习和生成树算法
        - 即插即用；二层设备，速率高
        - 执行生成树算法，限制广播帧的转发
        - ARP表项随着站点数量增多而增多
    - 路由器：路由器维护路由表，执行路由算法
        - 路由算法能够避免环路，无需执行生成树算法，可以以各种拓扑构建网络
        - 对广播分组做限制
        - 不是即插即用的，配置网络地址（子网前缀）
        - 三层设备，速率低

### 6.5 链路虚拟化：MPLS

MPLS：多协议标记交换。按照标签label来交换分组，而非按照目标IP查询路由表进行存储转发，效率更高

### 6.6 数据中心网络

数万-数十万台主机构成DC网络

在交换机之间，机器阵列之间有丰富的互连措施:
- 在阵列之间增加吞吐（多个可能的路由路径）
- 通过冗余度增加可靠性

### 6.7 a day in the life of web request

回顾：页面请求的历程（以一个web页面请求的例子：综述！）
- 目标：标示、回顾和理解涉及到的协议（所有层次），以一个看似简单的场景：请求www页面
- 场景：学生在校园启动一台笔记本电脑：请求和接受 www.google.com

日常场景

<img src="http://knight777.oss-cn-beijing.aliyuncs.com/img/image-20211003110344335.png" style="zoom:90%"/>

1. 连接到互联网
- 笔记本需要一个IP地址，第一跳路由器的IP地址，DNS的地址：采用DHCP
- DHCP请求被封装在UDP中，进而封装在IP，进而封装在802.3以太网帧中
- 以太网的帧在LAN上广播(destination: FFFFFFFFFFFF)，被运行中的DHCP服务器接收到
- 以太网帧中解封装IP分组，解封装UDP，解封装DHCP
- DHCP 服务器生成DHCP ACK 包括客户端IP地址，第一跳路由器IP地址和DNS名字服务器地址
- 在DHCP服务器封装，帧通过LAN转发（交换机学习）在客户端段解封装
- 客户端接收DHCP ACK应答
- 此时：客户端便有了IP地址，知道了DNS域名服务器的名字和IP地址第一跳路由器的IP地址

2. ARP（DNS之前，HTTP之前）
- 在发送HTTP request请求之前，需要知道 www.google.com 的IP地址：DNS
- DNS查询被创建，封装在UDP段中，封装在IP数据报中，封装在以太网的帧中。将帧传递给路由器，但是需要知道路由器的接口：MAC地址：ARP
- ARP查询广播，被路由器接收，路由器用ARP应答，给出其IP地址某个端口的MAC地址
- 客户端现在知道第一跳路由器MAC地址，所以可以发送DNS查询帧了

3. 使用DNS
- 包含了DNS查询的IP数据报通过LAN交换机转发，从客户端到第一跳路由器
- IP数据报被转发，从校园到达comcast网络，路由（路由表被RIP，OSPF，IS-IS 和/或 BGP协议创建）到DNS服务器
- 被DNS服务器解封装
- DNS服务器回复给客户端： www.google.com 的IP地址

4. TCP连接携带HTTP报文
- 为了发送HTTP请求，客户端打开到达web服务器的TCP sockect
- TCP SYN 段（3次握手的第1次握手）域间路由到web服务
- web服务器用TCP SYNACK应答（3次握手的第2次握手）
- 客户端再次进行ACK确认的发送（3次握手的第3次握手）
- TCP连接建立了！

5. HTTP请求和应答
- HTTP请求发送到TCP socket中
- IP数据报包含HTTP请求，最终路由到 www.google.com
- IP数据报包含HTTP应答最后被路由到客户端
- web页面最后显示出来了！

### 6.8 总结

- 数据链路层服务背后的原理:
    - 检错、纠错
    - 共享广播式信道：多路访问
    - 链路编址
- 各种链路层技术的实例和实现
    - Ethernet
    - 交换式LANS，VLANs
    - 虚拟成链路层的网络：MPLS
- 综合：一个web页面请求的日常场景
