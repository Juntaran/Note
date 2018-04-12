# Kafka

kafka bash 常用操作

``` bash
# 查询所有 topic
sh kafka-topics.sh  --list --zookeeper localhost:2181

# 根据 zk 查询指定 topic 内容
sh kafka-console-consumer.sh --topic testtopic  --from-beginning --zookeeper localhost:2181

# 根据 kafka server 查询指定 topic 内容
sh kafka-console-consumer.sh --topic testtopic --from-beginning --bootstrap-server localhost:9092

# 根据 zk 查询 group list
sh kafka-consumer-groups.sh --zookeeper localhost:2181 --list

# 创建 topic
sh kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 8 --topic testtopic

# 生产数据
sh kafka-console-producer.sh --broker-list localhost:9092 --topic testtopic
```