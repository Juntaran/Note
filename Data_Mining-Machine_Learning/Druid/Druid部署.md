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

开启 Zookeeper  

``` sh
curl http://www.gtlib.gatech.edu/pub/apache/zookeeper/zookeeper-3.4.10/zookeeper-3.4.10.tar.gz -o zookeeper-3.4.10.tar.gz
tar -xzf zookeeper-3.4.10.tar.gz
cd zookeeper-3.4.10
cp conf/zoo_sample.cfg conf/zoo.cfg
./bin/zkServer.sh start
```

开启 Druid 服务

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
