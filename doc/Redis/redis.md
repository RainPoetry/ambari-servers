## Redis 安装教程

### 安装依赖
```
yum install -y redis
```

### 修改 redis 配置文件
```
/etc/redis.conf
```

### 启动 redis
```
systemctl start redis
```

## 参考资料

[redis-server - GitHup](https://github.com/Symantec/ambari-redis-service)

[redis5 安装教程](https://my.oschina.net/ruoli/blog/2252393)

[redis-cluster 官方文档](https://redis.io/topics/cluster-tutorial)

[阿里云 rpm 仓库](http://mirrors.aliyun.com/centos/7/os/x86_64/Packages/)

[ RPM 下载 - rpmfind](https://rpmfind.net/linux/rpm2html/search.php?query=redis)

[ RPM 下载 - pkgs](https://centos.pkgs.org/7/ius-x86_64/redis5-5.0.3-1.ius.centos7.x86_64.rpm.html)