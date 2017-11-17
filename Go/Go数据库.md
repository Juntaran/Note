# Go数据库

*2017.11.17*


## 数据库初始化

``` go
import (
	"fmt"
	"log"
	"github.com/astaxie/beego/orm"
	"github.com/astaxie/beego"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
	"database/sql"
)

type A struct {
	//gorm.Model	// gorm 会自动设置字段 ID 默认为主键自增，也会设置软删除相关字段
	Id          	int    		`gorm:"primary_key;AUTO_INCREMENT"` 				// ID 主键
	one 			bool 		`gorm:"not null"`
}



// mysql 数据库初始化
// 1. 连接数据库
// 2. 创建必须的数据库表

var conninfo string

func InitMySql(sqlurl, sqluser, sqlpass, sqldb string) (db *gorm.DB, err error) {

	// 连接数据库
	conninfo = fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=latin1&parseTime=True&loc=Local", sqluser, sqlpass, sqlurl, sqldb)
	log.Println(conninfo)

	db, err = gorm.Open("mysql", conninfo)
	//defer db.Close()
	if err != nil {
		log.Println(err)
		panic(err)
	}

	// 创建必须的数据库表
	// a 表
	if db.HasTable(A{}) == false {
		err = db.CreateTable(A{}).Error
		if err != nil {
			log.Println(err)
			panic(err)
		} else {
			log.Println("Create a table success")
		}
	} else {
		log.Println("a table exist!")
	}
}

// models 包初始化，创建3个 db 对象并且读取配置
// Db  为 gorm 对象，适合构建表
// Db2 为 sql 驱动对象，轻量一些 一些小 sql 语句直接执行即可
// Orm 为 ormer 对象，用在 json 和 update
// 没错，老子就是这么屌，三个 sql 对象轮着用
// 以后谁改这段代码你就哭吧～
var Db *gorm.DB
var Db2 *sql.DB
var Orm orm.Ormer

func InitDB()  {
	// 进入 models 包先执行 init() 读数据库配置并连接初始化
	// 从配置文件 conf/app.conf 中读取配置
	sqluser := beego.AppConfig.String("mysqluser")
	sqlpass := beego.AppConfig.String("mysqlpass")
	sqlurl  := beego.AppConfig.String("mysqlurls")
	sqldb   := beego.AppConfig.String("mysqldb")

	var err error
	Db, err = InitMySql(sqlurl, sqluser, sqlpass, sqldb)
	if err != nil {
		log.Println(err)
		panic(err)
	} else {
		log.Println("db init success")
	}

	Db2, err = sql.Open("mysql", conninfo)
	if err != nil {
		log.Println("db2 connect fail")
		log.Println(err)
		panic(err)
	} else {
		log.Println("db2 init success")
	}

	orm.RegisterDriver("mysql", orm.DRMySQL)
	conninfo := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=latin1", sqluser, sqlpass, sqlurl, sqldb)
	orm.RegisterDataBase("default", "mysql", conninfo)
	log.Println("init orm finish")
	Orm = orm.NewOrm()
}

```


## MySQL Driver

查询单列：g.Db2.QueryRow(verifySQL).Scan(&verify)

## Gorm




## beego.orm
