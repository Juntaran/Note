# MIUI FAST 信息化平台:  

## 目的:  
MIUI SRE 的一个约2-3个季度的项目，目的是更好的让 SRE 掌握自己负责的产品线  

## 实现阶段:    

1. 存储日志，以 nginx 日志为主，本地 log -> LCS -> Hive／HDFS (主要解决本地日志如何调用 LCS 即可，打到 Hive/HDFS 的区别在于通过 HDFS SHELL 可以实时查询到数据，，如果使用MapReduce或者Spark程序处理HDFS文件，会有一个小时的延迟。Hive 新注册的数据流，必须要等到第二天才能使用数据工场的 Hive 进行查询)  
2. 构建数据分析集群 (Hadoop + Hive + HBase + Kylin)，分析挖掘高价值数据并长期存储，Hive -> Apache Kylin -> HBase  
3. 高价值数据展示，HBase -> OpenTSDB -> Grafana/Echarts   
4. 机器学习预测报警 + 预估资源配置  
5. 前端展示  
  
## 具体步骤:    
  
### 17 Q4:  

1. td-agent -> LCS  如何替换现有的 td-agent -> Scribe  
2. Hive -> Kylin 搭建  
3. 定义 Python/Go 的 httpclient 方式调用 Kylin Resetful API   
4. 决定挖掘什么数据，判定需要聚合并存储哪些数据  
  
## 一些问题:

1. Kylin 可不可用？ --可用，高效查询 Hive 并有完善的 RESTful API  
2. LCS 把数据打到哪里，哪里作为基础数据源？ --待解决
