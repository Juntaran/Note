# Go 解析 yml



``` yml
brokers: localhost:9092,localhost:9093
topics:
- topicname: nginx_test1
  partition: 2
- topicname: nginx_test2
  partition: 4
- topicname: nginx_test3
  partition: 8
```

``` go
/** 
  * Author: Juntaran 
  * Email:  Jacinthmail@gmail.com 
  * Date:   2018/3/23 14:59
  */

package main

import (
	"io/ioutil"
	"fmt"
	"gopkg.in/yaml.v2"
)

type KafkaTopic struct {
	Brokers 	string
	Topics		[]Topic
}

type Topic struct {
	TopicName	string
	Partition 	int
}

func GetKafkaData() KafkaTopic {
	data, _ := ioutil.ReadFile("utils/kafka.yml")
	fmt.Println(string(data))

	t := KafkaTopic{}
	yaml.Unmarshal(data, &t)
	fmt.Println("初始数据:", t)

	d, _ := yaml.Marshal(&t)
    fmt.Println(string(d))
    
    return t
}

func main() {
    GetKafkaData()
}
```