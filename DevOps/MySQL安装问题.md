# MySQL安装问题

*2017.6.1*

## Ubuntu下MySQL重新安装

    sudo rm /var/lib/mysql/ -R
    sudo rm /etc/mysql/ -R
    sudo apt-get autoremove mysql* --purge
    sudo apt-get remove apparmor
    sudo apt-get install mysql-server mysql-common 


## CentOS下MySQL重新安装

    rpm -e mysql
    rpm -e --nodeps mysql
    yum install -y mysql-server mysql mysql-devel

## 启动MySQL

    sudo service mysql start			// Ubuntu
    service mysqld start				// CentOS
    

## CentOS开机启动

    chkconfig --list | grep mysqld 
    chkconfig mysqld on


## 登陆MySQL

    mysqladmin -u root password 'root'
    mysql -u root -p

## 测试MySQL

    mysql>
    create database test;
    show databases;
    status;							// 查看MySQL版本
    select version();					// 查看MySQL版本
    show global variables like 'port';			// 查看MySQL端口号
    
    
    
## 远程登陆MySQL

    sudo vim/etc/mysql/my.cnf
    sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf

找到 `bind-address = 127.0.0.1` 这一行，注释掉，或改为`0.0.0.0`

    mysql>
    grant all privileges on *.*  to  'root'@'%'  identified by 'YourPassword'  with grant option;
    flush privileges;

退出MySQL命令

    sudo service mysql(d) restart

