# EMR HBase
create cluster (go advanced & select services)
enable ssh from local ip
connect via ssh
```
$ sudo su
# hbase shell

> create table
> create 't1', 'f1'
> put 't1', 'r1', 'f1:col1', 'v1'
> exit

```
### Hive
```
$ hive
set hbase.zookeeper.quorum=ec2-3-17-128-19.us-east-2.compute.amazonaws.com;
create external table inputTable (key string, value string)
     stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
      with serdeproperties ("hbase.columns.mapping" = ":key,f1:col1")
      tblproperties ("hbase.table.name" = "t1");

select count(key) from inputTable ;
select * from inputTable;
```
Query took ~3 seconds to complete


### PySpark

ERROR: 
```
# pyspark
Python 2.7.15 (default, Nov 28 2018, 22:38:08) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-28)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
19/01/13 20:57:04 ERROR SparkContext: Error initializing SparkContext.
java.lang.IllegalArgumentException: Required executor memory (4608), overhead (460 MB), and PySpark memory (0 MB) is above the max threshold (3072 MB) of this cluster! Please check the values of 'yarn.scheduler.maximum-allocation-mb' and/or 'yarn.nodemanager.resource.memory-mb'.
        at org.apache.spark.deploy.yarn.Client.verifyClusterResources(Client.scala:345)
        at org.apache.spark.deploy.yarn.Client.submitApplication(Client.scala:175)
        at org.apache.spark.scheduler.cluster.YarnClientSchedulerBackend.start(YarnClientSchedulerBackend.scala:57)
```

### Spark
ERROR
```
# spark-shell
19/01/13 20:57:55 ERROR Main: Failed to initialize Spark session.
java.lang.IllegalArgumentException: Required executor memory (4608), overhead (460 MB), and PySpark memory (0 MB) is above the max threshold (3072 MB) of this cluster! Please check the values of 'yarn.scheduler.maximum-allocation-mb' and/or 'yarn.nodemanager.resource.memory-mb'.
        at org.apache.spark.deploy.yarn.Client.verifyClusterResources(Client.scala:345)
```