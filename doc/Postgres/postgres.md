## postgres 安装教程

### 安装依赖
```
yum -y install postgresql11 postgresql11-server postgresql11-libs
```
### 初始化数据库：
```
/usr/pgsql-11/bin/postgresql-11-setup initdb
```
### 开启访问权限：
- 修改 pg_hba.conf 文件
```
host    all             all             0.0.0.0/0               trust
```
- 修改 postgressql.conf 文件
```
# 修改端口号
port = 5434
```
### 启动数据库
```
{params.postgres_bin}/pg_ctl -D {params.postgres_data} -l {params.postgres_log_file} start
```

### 关闭数据库
- 方式一
```
{params.postgres_bin}/pg_ctl -D {params.postgres_data} -l {params.postgres_log_file} stop
```
- 方式二
```
kill -INT `head -1 {params.postgres_pid_file}`
```
### 以服务的形式启动、关闭数据库(备用方案)
```
systemctl enable postgresql-11
systemctl start postgresql-11
systemctl stop postgresql-11
```

## 参考资料
[RPM 官方地址](https://yum.postgresql.org/rpmchart.php)