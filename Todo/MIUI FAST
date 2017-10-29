# MIUI FAST 信息化平台:  

## 目的:  
MIUI SRE 的一个约2-3个季度的项目，目的是更好的让 SRE 掌握自己负责的产品线  

## 实现阶段:    

  1. 存储日志，以 nginx 日志为主，本地 log -> lcs -> Hive  
  2. 构建数据分析平台，分析挖掘高价值数据并长期存储，Hive -> Apache Kylin  
  3. 高价值数据展示，Apache Kylin -> TSDB -> Grafana  
  4. 机器学习预测报警 + 预估资源配置  
  
## 具体步骤:    
  
### 17 Q4:  

  1. td-agent -> lcs  如何替换现有的 Scribe  
  2. Hive -> Kylin 搭建  
  3. 定义 Python/Go 的 httpclient 方式调用 Kylin Resetful API  
  4. Kylin 根据时间提取到 TSDB  
  5. 决定挖掘什么数据，判定需要聚合并存储哪些数据  
  
