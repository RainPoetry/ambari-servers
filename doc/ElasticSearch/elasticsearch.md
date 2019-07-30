## ElasticSearch 安装教程

### 安装依赖
```
yum install elasticsearch
```

### 修改 elasticsearch.yml 文件
```
cluster.name: es-test

node.name: slave2
node.master: true
node.data: true

path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

bootstrap.memory_lock: false
bootstrap.system_call_filter: false

network.host: 0.0.0.0

http.port: 9200
discovery.seed_hosts: ["172.18.130.101", "172.18.130.102","172.18.130.103"]
cluster.initial_master_nodes: ["172.18.130.103"]

http.cors.enabled: true
http.cors.allow-origin: "*"
```

### 启动服务
```
systemctl start elasticsearch
```

## 问题汇总
- java.nio.file.AccessDeniedException: /var/lib/elasticsearch/nodes/0/node.lock
```
chown -R elasticsearch:elasticsearch /var/lib/elasticsearch 
```

## 参考资料

[elasticsearch-server - GitHup](https://github.com/Symantec/ambari-elasticsearch-service)

[RPM 官网下载](https://www.elastic.co/cn/downloads/elasticsearch)

[ElasticSearch集群搭建](https://juejin.im/post/5bad9520f265da0afe62ed95#heading-8)