# Go 日志

``` go 

// 日志路径
var logFileName = "authorityAudit.log"

// 全局 logger
var Logger *log.Logger

func InitLog()  {
	var logFile *os.File
	_, err := os.Stat(logFileName)
	if err != nil {
		logFile, err = os.OpenFile(logFileName, os.O_RDWR | os.O_CREATE, 0777)
	} else {
		logFile, err = os.OpenFile(logFileName, os.O_RDWR | os.O_APPEND, 0777)
	}
	if err != nil {
		fmt.Printf("open file error=%s\n", err.Error())
		os.Exit(-1)
}

	//defer logFile.Close()
	//logger:=log.New(logFile,"\r\n", log.Ldate | log.Ltime | log.Llongfile)
	Logger = log.New(logFile,"", log.Ldate | log.Ltime)
	Logger.Println("*************************************")
	Logger.Println("INIT LOG SUCCESS")
	Logger.Println("*************************************")
}
```


改良一下  

``` go
package g

import (
	"os"
	"fmt"
	"log"
	"TempAuth/utils"
)

// 日志路径
var logFileName = "authorityAudit.log"

// 全局 logger
var Logger *log.Logger

// 日志输出
/*
	@timestamp    	long
	action			string
	info			string
	name			string
	user			string
*/

type LogStruct struct {
	Timestamp 		int64
	Action 			string			// 在 Action 中自定义 action 种类
	Info 			string
	Name 			string
	User 			string
}

var Action = []string{"init", "visit", "apply"}

func 	OutLog(info, name string, action int)  {
	var logS = LogStruct {
		Timestamp:  	utils.NowTimestamp(),
		Action: 		Action[action],
		Info: 			info,
		Name: 			name,
		User:           "juntaran",
	}
	// 格式化日志　
	Logger.Printf("{\"@timestamp\":%v, \"action\":\"%s\", \"info\":\"%s\", \"name\":\"%s\", \"user\":\"%s\"}", logS.Timestamp, logS.Action, logS.Info, logS.Name, logS.User)
}

func InitLog()  {
	var logFile *os.File
	_, err := os.Stat(logFileName)
	if err != nil {
		logFile, err = os.OpenFile(logFileName, os.O_RDWR | os.O_CREATE, 0777)
	} else {
		logFile, err = os.OpenFile(logFileName, os.O_RDWR | os.O_APPEND, 0777)
	}
	if err != nil {
		fmt.Printf("open file error=%s\n", err.Error())
		os.Exit(-1)
	}

	defer logFile.Close()
	Logger = log.New(logFile,"", 0)

	OutLog("INIT LOG SUCCESS", "sys", 0)
}
```
