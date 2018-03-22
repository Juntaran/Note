# Go 连接 kafka

[Sarama](https://github.com/Shopify/sarama) 支持 Kafka 0.8 及以上版本  

Kafka 0.8.2 和以前的版本，可以参考 [wvanbergen/kafka](https://github.com/wvanbergen/kafka) 基于 Sarama 的实现  
Kafka 0.9 和以上的版本，可以参考 [bsm/sarama-cluster](https://github.com/bsm/sarama-cluster) 基于 Sarama 的实现


``` go
/** 
  * Author: Juntaran 
  * Email:  Jacinthmail@gmail.com 
  * Date:   2018/3/22 17:11
  */

package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"strconv"
	"strings"

	"github.com/Shopify/sarama"
)

const BrockerList = "localhost:9092"

// 消费者
func Consumer(topic, offset string, partition int) {

	var logger = log.New(os.Stderr, "", log.LstdFlags)

	var (
		initialOffset int64
		offsetError   error
	)
	switch offset {
	case "oldest":
		initialOffset = sarama.OffsetOldest
	case "newest":
		initialOffset = sarama.OffsetNewest
	default:
		initialOffset, offsetError = strconv.ParseInt(offset, 10, 64)
	}

	if offsetError != nil {
		logger.Fatalln("Invalid initial offset:", offset)
	}

	c, err := sarama.NewConsumer(strings.Split(BrockerList, ","), nil)
	if err != nil {
		logger.Fatalln(err)
	}

	pc, err := c.ConsumePartition(topic, int32(partition), initialOffset)
	if err != nil {
		logger.Fatalln(err)
	}

	go func() {
		signals := make(chan os.Signal, 1)
		signal.Notify(signals, os.Kill, os.Interrupt)
		<-signals
		pc.AsyncClose()
	}()

	for msg := range pc.Messages() {
		fmt.Printf("Partation: %d\n", partition)
		fmt.Printf("Offset:    %d\n", msg.Offset)
		fmt.Printf("Key:       %s\n", string(msg.Key))
		fmt.Printf("Value:     %s\n", string(msg.Value))
		fmt.Println()
	}

	if err := c.Close(); err != nil {
		fmt.Println("Failed to close consumer: ", err)
	}
}

func main() {
	var endChan = make(chan struct{}, 1)
	for i := 0; i < 16; i++ {
		go Consumer("test", "newest", i)
	}
	<- endChan
}
```

