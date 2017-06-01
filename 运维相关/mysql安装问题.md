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

    create database test;
    show databases;
    status;										// 查看MySQL版本
    select version();							// 查看MySQL版本
    show global variables like 'port';			// 查看MySQL端口号

