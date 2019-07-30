## MySQL 安装教程

### 安装依赖
```
yum install -y mysql-community-common.x86_64 mysql-community-libs.x86_64 mysql-community-client.x86_64 mysql-community-server.x86_64
```

### 启动 MySQL

```
systemctl start  mysqld.service 
```

### 查看初始密码
```
cat /var/log/mysqld.log | grep 'temporary password'
```

### 修改默认密码为临时密码(用于 python 操作 mysql 数据库做准备)
```
mysqladmin -uroot -p'11k)zL(4vp,l' password 'AaBbCc123='
```
临时密码需要大小写、字母、数字、符号组成

### 登陆 Mysql , 修改 root 的信息，以及授权其他机器访问
```
# 设置密码的策略
set global validate_password_policy=0;
# 设置密码的长度
set global validate_password_length=4;
# 修改 root 用户的密码
alter user 'root'@'localhost' identified by 'root';
# 设置其他机器登陆的密码
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
FLUSH  PRIVILEGES;
```

## MySQL 卸载步骤
```
rpm -e --nodeps mysql-community-common mysql-community-libs mysql-community-client mysql-community-server
rm -rf /var/log/mysqld.log
rm -rf /var/lib/mysql
```

## 问题汇总

### mariadb冲突
```
# 查找所有的 mariadb 包
rpm -pa | rpm -qa | grep mariadb
# 依次卸载找到的 mariadb 依赖
例如：rpm -e --nodeps mariadb-server
```

## 参考资料
- [ MySQL 修改root密码的4种方法](https://blog.csdn.net/qq_33285112/article/details/78982766)
- [ Mysql 安装](https://www.cnblogs.com/shihuibei/p/9249155.html)
- [ RPM 官网下载](https://dev.mysql.com/downloads/mysql/)
- [ mysql python 库依赖](https://dev.mysql.com/downloads/connector/python/)