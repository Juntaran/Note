# Druid 部署

## 部署准备

> Java 8 or higher  
> Linux, Mac OS X, or other Unix-like OS (Windows is not supported)  
> 8G of RAM  
> 2 vCPUs  

## 安装

``` sh
curl -O http://static.druid.io/artifacts/releases/druid-0.11.0-bin.tar.gz
tar -xzf druid-0.11.0-bin.tar.gz
cd druid-0.11.0
```

- LICENSE - the license files  
- bin/ - scripts useful for this quickstart  
- conf/* - template configurations for a clustered setup  
- conf-quickstart/* - configurations for this quickstart  
- extensions/* - all Druid extensions  
- hadoop-dependencies/* - Druid Hadoop dependencies  
- lib/* - all included software packages for core Druid  
- quickstart/* - files useful for this quickstart  


## 开启 druid 服务

开启 Zookeeper  

``` sh
curl http://www.gtlib.gatech.edu/pub/apache/zookeeper/zookeeper-3.4.10/zookeeper-3.4.10.tar.gz -o zookeeper-3.4.10.tar.gz
tar -xzf zookeeper-3.4.10.tar.gz
cd zookeeper-3.4.10
cp conf/zoo_sample.cfg conf/zoo.cfg
./bin/zkServer.sh start
```

``` sh
cd druid-0.11.0
bin/init

java `cat conf-quickstart/druid/historical/jvm.config | xargs` -cp "conf-quickstart/druid/_common:conf-quickstart/druid/historical:lib/*" io.druid.cli.Main server historical

java `cat conf-quickstart/druid/broker/jvm.config | xargs` -cp "conf-quickstart/druid/_common:conf-quickstart/druid/broker:lib/*" io.druid.cli.Main server broker

java `cat conf-quickstart/druid/coordinator/jvm.config | xargs` -cp "conf-quickstart/druid/_common:conf-quickstart/druid/coordinator:lib/*" io.druid.cli.Main server coordinator

java `cat conf-quickstart/druid/overlord/jvm.config | xargs` -cp "conf-quickstart/druid/_common:conf-quickstart/druid/overlord:lib/*" io.druid.cli.Main server overlord

java `cat conf-quickstart/druid/middleManager/jvm.config | xargs` -cp "conf-quickstart/druid/_common:conf-quickstart/druid/middleManager:lib/*" io.druid.cli.Main server middleManager
```

## 加载 demo 数据

``` sh
curl -X 'POST' -H 'Content-Type:application/json' -d @quickstart/wikiticker-index.json localhost:8090/druid/indexer/v1/task
```

可以去 `http://localhost:8090/console.html` 查看进度  

完成之后可以进行查询操作

``` sh
curl -L -H'Content-Type: application/json' -XPOST --data-binary @quickstart/wikiticker-top-pages.json http://localhost:8082/druid/v2/?pretty
```


## kafka 打入 druid

``` sh
curl -O http://www.us.apache.org/dist/kafka/0.9.0.0/kafka_2.11-0.9.0.0.tgz
tar -xzf kafka_2.11-0.9.0.0.tgz
cd kafka_2.11-0.9.0.0

# 启动 kafka
./bin/kafka-server-start.sh config/server.properties

# 创建 topic
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic pageviews
```

待输入格式  

``` json
{"time": "2000-01-01T00:00:00Z", "url": "/foo/bar", "user": "alice", "latencyMs": 32}
```

``` sh
vim conf-quickstart/tranquility/kafka.json
```

``` json
{
    "dataSources" : {
      "pageviews-kafka" : {
        "spec" : {
          "dataSchema" : {
            "dataSource" : "pageviews-kafka",
            "parser" : {
              "type" : "string",
              "parseSpec" : {
                "timestampSpec" : {
                  "format": "auto",
                  "column": "time"
                },
                "dimensionsSpec" : {
                  "dimensions" : ["url", "user"]
                },
                "format" : "json"
              }
            },
            "granularitySpec" : {
              "type" : "uniform",
              "segmentGranularity" : "hour",
              "queryGranularity" : "none"
            },
            "metricsSpec" : [
              {
                "name": "views",
                "type": "count"
              },
             {
                "name": "latencyMs", 
                "type": "doubleSum",
                "fieldName": "latencyMs"
              }
            ]
          },
          "ioConfig" : {
            "type" : "realtime"
          },
          "tuningConfig" : {
            "type" : "realtime",
            "maxRowsInMemory" : "100000",
            "intermediatePersistPeriod" : "PT10M",
            "windowPeriod" : "PT10M"
          }
        },
        "properties" : {
          "task.partitions" : "1",
          "task.replicants" : "1",
          "topicPattern" : "pageviews2"
        }
      }
    },
    "properties" : {
      "zookeeper.connect" : "localhost",
      "druid.discovery.curator.path" : "/druid/discovery",
      "druid.selectors.indexing.serviceName" : "druid/overlord",
      "commit.periodMillis" : "15000",
      "consumer.numThreads" : "2",
      "kafka.zookeeper.connect" : "localhost",
      "kafka.group.id" : "tranquility-kafka"
    }
  }
```

启动 tranquility 实现 Druid kafka 对接

``` sh
cd ~/workspace/druid/tranquility-distribution-0.8.0
bin/tranquility kafka -configFile ../druid-0.11.0/conf-quickstart/tranquility/kafka.json
```

``` sh
./bin/kafka-server-start.sh config/server.properties
```

待发送的数据

``` json
{"time": "2000-01-01T00:00:00Z", "url": "/foo/bar", "user": "alice", "latencyMs": 32}
{"time": "2000-01-01T00:00:00Z", "url": "/", "user": "bob", "latencyMs": 11}
{"time": "2000-01-01T00:00:00Z", "url": "/foo/bar", "user": "bob", "latencyMs": 45}
```

需要对数据时间进行替换

``` sh
python -c 'import datetime; print(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))'
```

向 kafka 发送数据

```
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic pageviews
```

查询数据

```
curl -L -H'Content-Type: application/json' -XPOST --data-binary @conf-quickstart/tranquility/kafka-query.json http://localhost:8082/druid/v2/\?pretty
```

kafka-query.json

``` json
{
  "queryType" : "topN",
  "dataSource" : "pageviews-kafka",
  "intervals" : ["2018-03-07/2018-03-09"],
  "granularity" : "all",
  "dimension" : "url",
  "metric" : "latencyMs",
  "threshold" : 2,
  "aggregations" : [
    {
      "name": "latencyMs", 
      "type": "doubleSum",
      "fieldName": "latencyMs"
    }
  ]
}
```

## HTTP 打入 druid

创建 json 文件指定 http json 格式  

``` json
{
  "dataSources" : {
    "pageviews" : {
      "spec" : {
        "dataSchema" : {
         
          "dataSource" : "pageviews",
          "parser" : {
            "type" : "string",
            "parseSpec" : {
             
              "timestampSpec" : {
                "column" : "time",
                "format" : "auto"
              },
              "dimensionsSpec" : {
          
                "dimensions" : ["url", "user"],
                "dimensionExclusions" : [
                  "timestamp",
                  "value"
                ]
              },
              "format" : "json"
            }
          },
          "granularitySpec" : {
            "type" : "uniform",
            "segmentGranularity" : "hour",
            "queryGranularity" : "none"
          },
        
          "metricsSpec" : [
            {
              "name": "views",
              "type": "count"
            },
            {
              "name": "latencyMs", 
              "type": "doubleSum", 
              "fieldName": "latencyMs"
            }
          ]
        },
        "ioConfig" : {
          "type" : "realtime"
        },
        "tuningConfig" : {
          "type" : "realtime",
          "maxRowsInMemory" : "100000",
          "intermediatePersistPeriod" : "PT10M",
          "windowPeriod" : "PT10M"
        }
      },
      "properties" : {
        "task.partitions" : "1",
        "task.replicants" : "1"
      }
    }
  },
  "properties" : {
    "zookeeper.connect" : "localhost",
    "druid.discovery.curator.path" : "/druid/discovery",
    "druid.selectors.indexing.serviceName" : "druid/overlord",
    "http.port" : "8200",
    "http.threads" : "8"
  }
}
```

启动 tranquility

``` sh
cd ~/workspace/druid/tranquility-distribution-0.8.0
bin/tranquility server -configFile ./conf/pageviews.json
```

向 tranquility 使用 `POST` 发送数据  http://localhost:8200/v1/post/pageviews  

``` json
{"time": 1522147671, "url": "/foo/bar", "user": "alice", "latencyMs": 32}
```

结果:  

``` json
{
    "result": {
        "received": 1,
        "sent": 0
    }
}
```

- 注意时间戳必须是 10 分钟以内  