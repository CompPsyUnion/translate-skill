# Project Terminology Glossary

本术语表收录软件工程与技术文档翻译中的高频专业术语，用于保障译文在专有名词与技术表达上的一致性与准确性。

---

## 1. 通用工程与项目开发 (General Engineering & Development)

| Original Term (Source) | Translated Term (Target) | Notes / Context |
| :--------------------- | :----------------------- | :-------------- |
| 仓库                   | repository               | 源码托管仓库 (Git repository) |
| 依赖项                 | dependencies             | 外部引用的库或模块 |
| 脚手架                 | scaffolding              | 项目初始化构建工具与骨架 |
| 占位符                 | placeholder              | 语法或配置模板中的填充占位 |
| 钩子                   | hooks                    | 生命周期钩子或 Git hooks |
| 最佳实践               | best practices           | 行业推荐规范与设计模式 |
| 开箱即用               | out-of-the-box           | 无需复杂配置即可直接使用 |
| 生产环境               | production environment   | 正式上线运行的环境 |
| 调试 / 排查            | debugging / troubleshooting | 代码问题诊断与故障排查 |
| 回滚                   | rollback                 | 版本或事务恢复到上一稳定状态 |

---

## 2. 架构设计与分布式系统 (Architecture & Distributed Systems)

| Original Term (Source) | Translated Term (Target) | Notes / Context |
| :--------------------- | :----------------------- | :-------------- |
| 中间件                 | middleware               | 处于操作系统与应用之间的支撑服务 |
| 负载均衡               | load balancing           | 流量分发机制 |
| 高可用                 | high availability (HA)   | 系统持续可用性保障 |
| 故障转移               | failover                 | 节点失效后的自动切换机制 |
| 服务发现               | service discovery        | 微服务动态定位与注册机制 |
| 熔断器                 | circuit breaker          | 防止级联故障的服务保护机制 |
| 降级                   | degradation / fallback   | 高负载下的功能兜底策略 |
| 限流                   | rate limiting            | 请求流量控制与频次限制 |
| 幂等性                 | idempotency              | 多次执行产生相同结果的接口特性 |
| 一致性哈希             | consistent hashing       | 分布式节点负载分配算法 |

---

## 3. 内存管理与并发编程 (Memory Management & Concurrency)

| Original Term (Source) | Translated Term (Target) | Notes / Context |
| :--------------------- | :----------------------- | :-------------- |
| 栈                     | stack                    | 线程私有、遵循先进后出的内存空间 |
| 堆                     | heap                     | 动态分配、全局共享的内存空间 |
| 内存泄漏               | memory leak              | 分配的内存在失效后未被释放 |
| 垃圾回收               | garbage collection (GC)  | 自动内存回收机制 |
| 互斥锁                 | mutex                    | 防止数据竞争的排他锁 |
| 竞态条件               | race condition           | 依赖并发执行时序的逻辑错误 |
| 死锁                   | deadlock                 | 多个线程因资源争夺而永久阻塞 |
| 线程池                 | thread pool              | 预先分配并复用线程的管理机制 |
| 上下文切换             | context switch           | CPU 暂停当前任务并恢复另一任务的过程 |
| 临界区                 | critical section         | 访问并发共享资源的代码段 |

---

## 4. 容器与云原生运维 (Containers & Cloud Native)

| Original Term (Source) | Translated Term (Target) | Notes / Context |
| :--------------------- | :----------------------- | :-------------- |
| 镜像                   | image                    | 静态的应用打包产物 (Container image) |
| 容器                   | container                | 隔离运行的实例进程 |
| 守护进程               | daemon                   | 后台持续运行的服务进程 |
| 编排                   | orchestration            | 容器与服务的集群调度机制 (如 K8s) |
| 卷挂载                 | volume mount             | 宿主机存储挂载至容器 |
| 端口映射               | port mapping / port forwarding | 宿主机端口与容器端口的网络绑定 |
| 命名空间               | namespace                | 资源隔离机制 |
| 控制组                 | cgroups (control groups) | 硬件资源限制机制 |

---

## 5. 网络传输与 API 规范 (Networking & APIs)

| Original Term (Source) | Translated Term (Target) | Notes / Context |
| :--------------------- | :----------------------- | :-------------- |
| 吞吐量                 | throughput               | 单位时间内系统处理的请求量 |
| 延迟                   | latency                  | 请求发起至收到响应的时间开销 |
| 序列化 / 反序列化      | serialization / deserialization | 数据结构与字节流之间的双向转换 |
| 握手                   | handshake                | 通信双方建立连接的协议协商过程 |
| 鉴权 / 授权            | authentication / authorization | 身份核实 (AuthN) 与权限控制 (AuthZ) |
| 负载                   | payload                  | 数据传输中的有效实体内容 |
| 报头                   | header                   | 请求或数据包的元数据头部 |
