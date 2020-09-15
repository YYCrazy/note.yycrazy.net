Title: CDH 5.7 Installation On CentOS 6
Date: 2016-12-31 00:00:00
Modified: 2016-12-31 00:00:00
Category: Bigdata
Tags: CDH
Slug: cdh-5-7-installation-on-centos-6
Authors: YYCrazy

## 关闭 SELinux

    :::bash
    setenforce 0

    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux

## 关闭防火墙

    :::bash
    chkconfig iptables off
    service iptables stop

    chkconfig ip6tables off
    service ip6tables stop

## 配置系统参数

### IPv6

    :::bash
    echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6
    echo 1 > /proc/sys/net/ipv6/conf/default/disable_ipv6

    cat >> /etc/sysctl.conf <<EOF
    net.ipv6.conf.all.disable_ipv6 = 1
    net.ipv6.conf.default.disable_ipv6 = 1
    EOF

### Swappiness

    :::bash
    echo 1 > /proc/sys/vm/swappiness

    cat >> /etc/sysctl.conf <<EOF
    vm.swappiness = 1
    EOF

### Transparent Huge Pages

    :::bash
    echo never > /sys/kernel/mm/transparent_hugepage/defrag
    echo never > /sys/kernel/mm/transparent_hugepage/enabled

    cat >> /etc/rc.local <<EOF
    echo never > /sys/kernel/mm/transparent_hugepage/defrag
    echo never > /sys/kernel/mm/transparent_hugepage/enabled
    EOF

### Open Files

    :::bash
    cat >> /etc/pam.d/login <<EOF
    session required pam_limits.so
    EOF

    cat >> /etc/security/limits.conf <<EOF
    * soft nofile 65535
    * hard nofile 65535
    EOF

    sed -i 's/#UsePAM no/UsePAM yes/g' /etc/ssh/sshd_config

### File Access Time

**/etc/fstab**

    :::bash
    cat > /etc/fstab <<EOF
    /dev/sda1   swap        swap        defaults            0 0
    /dev/sda2   /           ext4        defaults            1 1
    /dev/sga1   /sga        ext4        defaults,noatime    0 0
    /dev/sgb1   /sgb        ext4        defaults,noatime    0 0
    /dev/sgc1   /sgc        ext4        defaults,noatime    0 0
    /dev/sgd1   /sgd        ext4        defaults,noatime    0 0
    /dev/sge1   /sge        ext4        defaults,noatime    0 0
    /dev/sgf1   /sgf        ext4        defaults,noatime    0 0
    tmpfs       /dev/shm    tmpfs       defaults            0 0
    devpts      /dev/pts    devpts      gid=5,mode=620      0 0
    sysfs       /sys        sysfs       defaults            0 0
    proc        /proc       proc        defaults            0 0
    EOF

## 配置主机名

**bigdata-m-001.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-m-001.bigdata.com
    EOF

**bigdata-m-002.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-m-002.bigdata.com
    EOF

**bigdata-m-003.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-m-003.bigdata.com
    EOF

**bigdata-w-001.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-w-001.bigdata.com
    EOF

**bigdata-w-002.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-w-002.bigdata.com
    EOF

**bigdata-w-003.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-w-003.bigdata.com
    EOF

**bigdata-w-004.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-w-004.bigdata.com
    EOF

**bigdata-w-005.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-w-005.bigdata.com
    EOF

**bigdata-w-006.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-w-006.bigdata.com
    EOF

**bigdata-w-007.bigdata.com**

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=bigdata-w-007.bigdata.com
    EOF

## 配置 hosts

    :::bash
    cat > /etc/hosts <<EOF
    127.0.0.1       localhost
    192.168.86.201  bigdata-m-001.bigdata.com bigdata-m-001
    192.168.86.202  bigdata-m-002.bigdata.com bigdata-m-002
    192.168.86.203  bigdata-m-003.bigdata.com bigdata-m-003
    192.168.86.1    bigdata-w-001.bigdata.com bigdata-w-001
    192.168.86.2    bigdata-w-002.bigdata.com bigdata-w-002
    192.168.86.3    bigdata-w-003.bigdata.com bigdata-w-003
    192.168.86.4    bigdata-w-004.bigdata.com bigdata-w-004
    192.168.86.5    bigdata-w-005.bigdata.com bigdata-w-005
    192.168.86.6    bigdata-w-006.bigdata.com bigdata-w-006
    192.168.86.7    bigdata-w-007.bigdata.com bigdata-w-007
    EOF

## 配置软件源

    :::bash
    rm -f /etc/yum.repos.d/*

    cat > /etc/yum.repos.d/centos.repo <<EOF
    [CentOS]
    name = CentOS
    baseurl = http://bigdata-m-003.bigdata.com/CentOS-6.8-x86_64/
    gpgkey = http://bigdata-m-003.bigdata.com/CentOS-6.8-x86_64/RPM-GPG-KEY-CentOS-6
    gpgcheck = 1
    enabled = 1
    EOF

    cat > /etc/yum.repos.d/cloudera-manager.repo <<EOF
    [Cloudera-Manager]
    name = Cloudera-Manager
    baseurl = http://bigdata-m-003.bigdata.com/Cloudera/CM/5.7/
    gpgkey = http://bigdata-m-003.bigdata.com/Cloudera/CM/5.7/RPM-GPG-KEY-cloudera
    gpgcheck = 1
    enabled = 1
    EOF

### 配置软件源服务

**bigdata-m-003.bigdata.com**

    :::bash
    cd /data && nohup python -m SimpleHTTPServer 80 > /dev/null 2>&1 &

    yum -y install httpd

    kill -9 `netstat -antp | grep "0 0.0.0.0:80" | awk -F" " '{print $7}' | cut -d "/" -f 1`

    chkconfig httpd on
    service httpd start

    ln -s /data/CentOS-6.8-x86_64 /var/www/html/CentOS-6.8-x86_64
    ln -s /data/Cloudera /var/www/html/Cloudera
    ln -s /data/JDBC /var/www/html/JDBC
    ln -s /data/JDK /var/www/html/JDK

## 配置时钟同步

### 配置时区

    :::bash
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

### 配置 ntp

    :::bash
    yum -y install ntp ntpdate

    cat > /etc/ntp.conf <<EOF
    driftfile /var/lib/ntp/drift
    restrict default kod nomodify notrap nopeer noquery
    restrict -6 default kod nomodify notrap nopeer noquery
    restrict 127.0.0.1
    restrict -6 ::1
    server 192.168.86.253
    includefile /etc/ntp/crypto/pw
    keys /etc/ntp/keys
    EOF

    chkconfig ntpd on
    service ntpd start

    ntpq -p

## 配置 Java 环境

    :::bash
    yum -y install wget unzip

    wget http://bigdata-m-003.bigdata.com/JDK/jdk-8u74-linux-x64.rpm
    wget http://bigdata-m-003.bigdata.com/JDK/jce_policy-8.zip

    rpm -ivh jdk-8u74-linux-x64.rpm

    unzip jce_policy-8.zip
    cp UnlimitedJCEPolicyJDK8/local_policy.jar /usr/java/jdk1.8.0_74/jre/lib/security
    cp UnlimitedJCEPolicyJDK8/US_export_policy.jar /usr/java/jdk1.8.0_74/jre/lib/security

    alternatives --install /usr/bin/java java /usr/java/jdk1.8.0_74/jre/bin/java 9999

    cat > /etc/profile.d/java_home.sh <<EOF
    export JAVA_HOME="/usr/java/jdk1.8.0_74"
    EOF

## 配置 SSH 密钥登陆

    :::bash
    ssh-keygen -t rsa -b 8192 -N ''
    ssh-copy-id -i root@bigdata-m-001.bigdata.com
    ssh-copy-id -i root@bigdata-m-002.bigdata.com
    ssh-copy-id -i root@bigdata-m-003.bigdata.com
    ssh-copy-id -i root@bigdata-w-001.bigdata.com
    ssh-copy-id -i root@bigdata-w-002.bigdata.com
    ssh-copy-id -i root@bigdata-w-003.bigdata.com
    ssh-copy-id -i root@bigdata-w-004.bigdata.com
    ssh-copy-id -i root@bigdata-w-005.bigdata.com
    ssh-copy-id -i root@bigdata-w-006.bigdata.com
    ssh-copy-id -i root@bigdata-w-007.bigdata.com

## 配置 MySQL

**bigdata-m-003.bigdata.com**

    :::bash
    yum -y install mysql mysql-server

    chkconfig mysqld on
    service mysqld start

    mysql_secure_installation

    mysql -uroot -p <<EOF
    create database scm default charset utf8 collate utf8_general_ci;
    grant all privileges on scm.* to 'scm_db_usr'@'%' identified by '__scm_db_pwd__';
    create database hive default charset utf8 collate utf8_general_ci;
    grant all privileges on hive.* to 'hive_db_usr'@'%' identified by '__hive_db_pwd__';
    create database hue default charset utf8 collate utf8_general_ci;
    grant all privileges on hue.* to 'hue_db_usr'@'%' identified by '__hue_db_pwd__';
    create database oozie default charset utf8 collate utf8_general_ci;
    grant all privileges on oozie.* to 'oozie_db_usr'@'%' identified by '__oozie_db_pwd__';
    flush privileges;
    EOF

## 配置 Cloudera Manager 及 CDH

**bigdata-m-003.bigdata.com**

    :::bash
    mkdir -p /usr/share/java
    wget -O /usr/share/java/mysql-connector-java.jar http://bigdata-m-003.bigdata.com/JDBC/MySQL/mysql-connector-java-5.1.40-bin.jar

    yum -y install cloudera-manager-server

    /usr/share/cmf/schema/scm_prepare_database.sh --host bigdata-m-003.bigdata.com --port 3306 mysql scm scm_db_usr __scm_db_pwd__

    chkconfig cloudera-scm-server on
    service cloudera-scm-server start

### Web 控制台

- http://bigdata-m-003.bigdata.com:7180
    - 账号：admin
    - 密码：admin

- 集群安装
    - 选择存储库
        - 选择方法
            - 使用 Parcel (建议)
                - Parcel 目录：/opt/cloudera/parcels
                - 本地 Parcel 存储库路径：/opt/cloudera/parcel-repo
                - 远程 Parcel 存储库 URL
                    - http://bigdata-m-003.bigdata.com/Cloudera/CDH/5.7/
        - 选择 CDH 的版本
            - CDH-5.7.0-1.cdh5.7.0.p0.45
        - 选择您要安装在主机上的 Cloudera Manager Agent 特定发行版
            - 自定义存储库：http://bigdata-m-003.bigdata.com/Cloudera/CM/5.7/
        - 为 GPG 签名密钥的位置输入自定义 URL
            - 自定义 GPG 主要 URL：http://bigdata-m-003.bigdata.com/Cloudera/CM/5.7/RPM-GPG-KEY-cloudera
