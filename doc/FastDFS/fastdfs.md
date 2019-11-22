## FastDFS 教程

### 准备 FastDFS RPM 包
因为官方没有提供 FastDFS 的 RPM 包，因此需要我们手动制作。这一块，我采用的是 FPM 实现的，最终生成的 [RPM 文件地址](https://github.com/RainPoetry/ambari-servers/tree/master/doc/FastDFS/rpm)

#### 编译 FastDFS
```
# 解压 libfastcommon 和 fastdfs 压缩包
unzip libfastcommon-1.0.36.zip
unzip fastdfs-5.11.zip

# 编译 fastdfs
 cd fastdfs-5.11/
 ./make.sh  && ./make.sh install
```

#### 安装 FPM 
```
# 安装ruby模块
yum -y install ruby rubygems ruby-devel
# 查看当前使用的rubygems仓库
gem sources list
# 添加淘宝的Rubygems仓库，外国的源慢，移除原生的Ruby仓库
gem sources --add https://gems.ruby-china.com/ --remove http://rubygems.org/
# 安装fpm，gem从rubygem仓库安装软件类似yum从yum仓库安装软件。首先安装低版本的json，高版本的json需要ruby2.0以上，然后安装低版本的fpm，够用。
gem install json -v 1.8.3
gem install fpm -v 1.3.3

# 上面的2步安装仅适合CentOS6系统，CentOS7系统一步搞定，即 gem install fpm
```

#### 制作 FastDFS RPM 文件
```
fpm -s dir -t rpm -n fastdfs -v 5.11 --post-install /root/fdfs-env.sh -f /usr/lib64/libfastcommon.so /usr/lib/libfastcommon.so /usr/include/fastcommon /etc/fdfs /usr/bin/fdfs_* /usr/lib/libfdfsclient.so /usr/lib64/libfdfsclient.so /etc/rc.d/init.d/fdfs_* /run/systemd/generator.late/fdfs_*
```
- fdfs-env.sh 文件信息如下
```
#!/bin/bash
ln -s /usr/lib64/libfastcommon.so /usr/local/lib/libfastcommon.so
ln -s /usr/lib64/libfastcommon.so /usr/lib/libfastcommon.so
ln -s /usr/lib64/libfdfsclient.so /usr/local/lib/libfdfsclient.so
ln -s /usr/lib64/libfdfsclient.so /usr/lib/libfdfsclient.so
```
执行完fpm 命令后，会在当前目录下生成一个 fastdfs 的 rpm 文件

### 安装 fastdfs
将 fastdfs 的 RPM 文件放入本地 yum 源
```
yum install fastdfs
```

### 安装 Tracker 和 Storage
- Tracker:
```
# 创建 Tracker 的 data 目录
mkdir /opt/fastdfs_tracker


# 配置 /etc/fdfs目录下tracker.conf
1.disabled=false 
2.port=22122 #默认端口号 
3.base_path=/opt/fastdfs_tracker #我刚刚创建的目录 
4.http.server_port=8080 #默认端口是8080
5.store_lookup=0  #采用


# 启动
service fdfs_trackerd start
```
- storage:
```
# 建立存储目录
mkdir /opt/fastdfs_storage
mkdir /opt/fastdfs_storage_data


# 修改存储节点目录下/etc/fdfs/storage.conf配置信息
disabled=false #启用配置文件  
group_name=group1 #组名（第一组为 group1， 第二组为 group2）  
port=23000 #storage 的端口号,同一个组的 storage 端口号必须相同  
base_path=/opt/fastdfs_storage #设置storage数据文件和日志目录 
store_path0=/opt/fastdfs_storage_data #实际文件存储路径  
store_path_count=1 #存储路径个数，需要和 store_path 个数匹配  
tracker_server=192.168.43.70:22122 #tracker 服务器的 IP 地址和端口  
tracker_server=192.168.43.70:22122 #多个 tracker 直接添加多条配置  
http.server_port=8888 #设置 http 端口号


# 启动Storage
service fdfs_storaged start
```

## 参考资料
[ FPM 制作 RPM 包](https://www.zyops.com/autodeploy-rpm/)
[CentOS7 搭建 FastDFS ](https://yongliangzhang.github.io/blogs/2018/02/01/CentOS_7.2%E6%90%AD%E5%BB%BAFastDFS_%E5%88%86%E5%B8%83%E5%BC%8F%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%EF%BC%8C%E5%AE%9E%E7%8E%B0%E9%AB%98%E5%8F%AF%E7%94%A8%E9%9B%86%E7%BE%A4/#2-%E5%AE%89%E8%A3%85Tracker%E5%B9%B6%E5%AE%9E%E7%8E%B0%E8%8A%82%E7%82%B9%E4%BF%A1%E6%81%AF%E9%85%8D%E7%BD%AE)