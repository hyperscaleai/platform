import shutil
class BackupUtil:
    def backup_mysql(self):
        shutil.copytree()
        '''
        Backup:
        cp -r /var/lib/mysql/aihf /mnt/data1/backup/mysql/YYYYMMDD/var/lib/mysql
        
        Restore:
        cp -r /mnt/data1/backup/mysql/20190107/var/lib/mysql/aihf /var/lib/mysql/aihf
        chown -R mysql:mysql /var/lib/mysql/aihf
        chmod -R 660 /var/lib/mysql/aihf
        chmod 700 /var/lib/mysql/aihf
        '''

    def mysql(self):
        '''
            docker pull mysql/mysql-server:5.7
            #Local access only
            docker run --name=mysql57 -d mysql/mysql-server:5.7            
            docker logs mysql57 2>&1 | grep GENERATED
            docker exec -it mysql57 mysql -uroot -p
            docker exec -it mysql57 bash
            docker inspect mysql57 | grep Source

            #Access by other hosts as well
            docker run --name=mysql57 -e MYSQL_ROOT_HOST=% -p 3306:3306 -d mysql/mysql-server:5.7

            
            ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
            ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
            ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'password';


            #Shutdown and copy mysql data folder from docker volume
            cp -r $(docker inspect mysql57 | grep Source | + SOME MAGIC) /var/lib/mysql
            chown -R 27:sudo /var/lib/mysql # or whatever group it is running

            #Recreate container OR reconfigure to bind new directories
            docker rm -v mysql57

            docker run --name=mysql57 --mount type=bind,src=/var/lib/mysql,dst=/var/lib/mysql -d mysql/mysql-server:5.7

            docker run --name=mysql57 --mount type=bind,src=/var/lib/mysql,dst=/var/lib/mysql -e MYSQL_ROOT_HOST=% -p 3306:3306 -d mysql/mysql-server:5.7

            #optinally mount both config and data directory
            docker run --name=mysql57 \
                   --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
                   --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
                   -d mysql/mysql-server:5.7

        :return:
        '''

    def install_hadoop_env(self):
        '''
        Install Java


        export HADOOP_HOME=/opt/hdp/hadoop
        export SPARK_HOME=/opt/hdp/spark
        export HADOOP_CONF_DIR=/opt/hdp/hadoop/etc/hadoop

        export FLUME_HOME=/opt/hdp/flume
        export FLUME_CONF_DIR=$FLUME_HOME/conf
        export FLUME_CLASSPATH=$FLUME_CONF_DIR

        export HDFS_NAMENODE_USER=root
        export HDFS_DATANODE_USER=root
        export HDFS_SECONDARYNAMENODE_USER=root
        export YARN_RESOURCEMANAGER_USER=root
        export YARN_NODEMANAGER_USER=root

        export SPARK_CONF_DIR=/opt/hdp/spark/conf

        export SPARK_MASTER_HOST=localhost

        export JAVA_HOME=/usr/lib/jvm/java-8-oracle

        export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:/opt/hdp/hive/bin:$SPARK_HOME/bin:/opt/hdp/presto/bin:$FLUME_HOME/bin

        export CLASSPATH=$CLASSPATH:$FLUME_HOME/lib/*:$FLUME_CONF_DIR/*

        :return:
        '''


    def install_engineering_env(self):
        '''
        MySQL Workbench:
            sudo apt install mysql-workbench


        :return:
        '''