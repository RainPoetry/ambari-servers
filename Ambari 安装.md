# Ambari 安装

## 离线下载 Ambari 包

![1568112760619](doc\pic\install\1568112760619.png)



![1568112775101](doc\pic\install\1568112775101.png)



![1568112811171](doc\pic\install\1568112811171.png)

![1568112850399](doc\pic\install\1568112850399.png)

![1568112913999](doc\pic\install\1568112913999.png)

![1568163789016](doc\pic\install\1568163789016.png)

## 准备环境(所有的节点)

#### 修改主机名

- hostnamectl set-hostname hbase01
- vim /etc/sysconfig/network

```
# Created by anaconda
NETWORKING=yes
HOSTNAME=hbase01
```

#### 配置 Hosts

- vim /etc/hosts

```
172.18.0.231	hbase01
172.18.0.232	hbase02
172.18.0.233	hbase03
```

#### 关闭防火墙

- systemctl disable firewalld.service（禁用防火墙开机启动）

- systemctl stop firewalld.service（关闭防火墙）

- systemctl status firewalld.service（查看防火墙状态）

  ```
  ● firewalld.service - firewalld - dynamic firewall daemon
     Loaded: loaded (/usr/lib/systemd/system/firewalld.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
       Docs: man:firewalld(1)
  
  9月 10 18:26:57 hbase03 systemd[1]: Starting firewalld - dynamic firewall daemon...
  9月 10 18:26:58 hbase03 systemd[1]: Started firewalld - dynamic firewall daemon.
  9月 10 18:27:00 hbase03 firewalld[931]: WARNING: ICMP type 'beyond-scope' is not supported by the kernel for ipv6.
  9月 10 18:27:00 hbase03 firewalld[931]: WARNING: beyond-scope: INVALID_ICMPTYPE: No supported ICMP type., ignoring for run-time.
  9月 10 18:27:00 hbase03 firewalld[931]: WARNING: ICMP type 'failed-policy' is not supported by the kernel for ipv6.
  9月 10 18:27:00 hbase03 firewalld[931]: WARNING: failed-policy: INVALID_ICMPTYPE: No supported ICMP type., ignoring for run-time.
  9月 10 18:27:00 hbase03 firewalld[931]: WARNING: ICMP type 'reject-route' is not supported by the kernel for ipv6.
  9月 10 18:27:00 hbase03 firewalld[931]: WARNING: reject-route: INVALID_ICMPTYPE: No supported ICMP type., ignoring for run-time.
  9月 10 19:08:01 hbase03 systemd[1]: Stopping firewalld - dynamic firewall daemon...
  9月 10 19:08:02 hbase03 systemd[1]: Stopped firewalld - dynamic firewall daemon.
  ```

#### 关闭 SElinux

- vim  /etc/sysconfig/selinux 

```
# 将SELINUX=enforcing改为SELINUX=disabled
SELINUX=disabled

# 重启，使配置生效
reboot
```

#### 更改 yum 源

- 备份镜像

```
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
```

- 添加国内镜像

```
cd /etc/yum.repos.d
wget http://mirrors.163.com/.help/CentOS7-Base-163.repo
yum clean all
yum makecache
```

#### 时钟同步

```
[root@localhost ~] yum install -y ntp  
[root@localhost ~] chkconfig --list ntpd  
[root@localhost ~] systemctl is-enabled ntpd  
[root@localhost ~] systemctl enable ntpd  
[root@localhost ~] systemctl start ntpd 
```

#### 免密码登录

- 生成 SSH 秘钥

```
ssh-keygen -t rsa
```

- 根据公钥，生成 authorized_keys

```
scp id_rsa.pub > authorized_keys
```

- 将 hbase02 和 hbase03 的 authorized_keys 发送到 hbase01

```
# hbase02
scp authorized_keys root@hbase01:~/.ssh/authorized_keys_02
# hbase03
scp authorized_keys root@hbase01:~/.ssh/authorized_keys_03
```

- 在 hbase01 节点，将所有的 hbase02  和 hbase03  发送过来的 公钥 追加到 hbase01  的 authorized_keys 文件末尾

```
cat authorized_keys_02 >> authorized_keys
cat authorized_keys_03 >> authorized_keys
```

- 将 hbase01 的 authorized_keys 发送到 habse02 和 hbase03

```
scp authorized_keys root@hbase02:~/.ssh/
scp authorized_keys root@hbase03:~/.ssh/
```



#### 安装 JDK1.8

- 检查系统 JDK 版本

```
java -version
```

- 查看 java 安装包

```
rpm -qa | grep java
```

- 卸载 openjdk

```
yum remove *openjdk*
```

- 解压安装包

```
tar zxf  jdk-8u221-linux-x64.tar.gz -C /usr/package/
```

- vim /etc/profile（配置 java 环境变量 ）

```
export JAVA_HOME=/usr/package/jdk1.8
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin
```

- 使配置立即生效

```
source  /etc/profile
```

- 查看 jdk 安装情况

```
java -version
java
javac
```



## 配置本地 yum 源( 仅 hbase01 节点)

### 安装本地源工具

```
yum install yum-utils createrepo yum-plugin-priorities -y
```

### 添加 gpgcheck

- vim /etc/yum/pluginconf.d/priorities.conf

```
[main]
enabled = 1
gpgcheck=0
```

### 配置 HTTP 服务

```
#检查是否安装httpd 
yum list httpd

#未安装则安装httpd
yum install httpd

#配置HTTP 服务到系统层使其随系统自动启动
chkconfig httpd on
service httpd start
```

### 创建本地源

- 将 yum 文件放入到 /var/www/html 目录下

```
# 将 ambari 解压到 /var/www/html/ambari/ 目录下
tar zxf ambari-2.7.4.0-centos7.tar.gz -C /var/www/html/ambari/
# 将 hdp 压缩包 解压到 /var/www/html/hdp/ 目录下
tar zxf HDP-3.1.4.0-centos7-rpm.tar.gz -C /var/www/html/hdp/
tar zxf HDP-UTILS-1.1.0.22-centos7.tar.gz -C /var/www/html/hdp/
```

- 创建仓库信息文件

```
# 创建 ambari 仓库信息文件
cd /var/www/html/ambari/
createrepo ./

# 创建 hdp 仓库信息文件
cd /var/www/html/hdp/
createrepo ./
```

- 编辑 repo 文件

  - 进入 /etc/yum.repos.d

  ```
  cd /etc/yum.repos.d
  ```

  - 创建 ambari.repo

  ```
  [ambari-2.7.3.0]
  name=ambari Version - ambari-2.7.3.0
  baseurl=http://hbase01/ambari
  gpgcheck=0
  gpgkey=http://hbase01/ambari
  enabled=1
  priority=1
  ```

  - 创建 hdp.repo

  ```
  [HDP-3.1.0.0]
  name=HDP Version - HDP-3.1.0.0
  baseurl=http://hbase01/hdp
  gpgcheck=0
  gpgkey=http://hbase01/hdp
  enabled=1
  priority=1
  ```

- 使用 本地 yum 源

  - 将 ambari.repo 和 hdp.repo 传输到 hbase02 和 hbase03

  ```
  scp ambari.repo root@hbase02:/etc/yum.repos.d/
  scp ambari.repo root@hbase03:/etc/yum.repos.d/
  
  scp hdp.repo root@hbase02:/etc/yum.repos.d/
  scp hdp.repo root@hbase03:/etc/yum.repos.d/
  ```

  - 更新 yum  源 （3 个 主机都需要）

  ```
  yum clean all
  yum makecacche
  ```

  - 检查仓库是否可用

  ```
  yum repolist
  ```

  ![1568120112799](doc\pic\install\1568120112799.png)



## 安装 Ambari

#### 安装 Ambari-server

```
yum install ambari-server
```

#### 配置 Ambari-server

```
ambari-server setup
```

![1568162415234](doc\pic\install\1568162415234.png)

#### 启动 Ambari-server

```
ambari-server start
```



## 参考链接

[Ambari及其HDP集群安装及其配置教程](https://zhuanlan.zhihu.com/p/37322462)

[HDP 官网](https://docs.cloudera.com/HDPDocuments/index.html)