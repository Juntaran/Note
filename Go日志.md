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
