Title: 编译安装 MySQL 5.7
Date: 2016-12-03 00:00:00
Modified: 2016-12-03 00:00:00
Category: Database
Tags: MySQL
Slug: building-mysql-5-7-from-source-on-centos-6
Authors: YYCrazy

## 安装准备

### 关闭 SELinux

    :::bash
    setenforce 0

    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux

### 关闭防火墙

    :::bash
    chkconfig iptables off
    service iptables stop

    chkconfig ip6tables off
    service ip6tables stop

### 安装依赖软件包

    :::bash
    yum -y install gcc gcc-c++ cmake make git bison m4 ncurses-devel

### 创建 mysql 组和账号

    :::bash
    groupadd -r mysql
    useradd -s /bin/false -g mysql -r mysql

### 创建数据目录

    :::bash
    mkdir -p /data/mysql
    chown -R mysql:mysql /data/mysql

## 安装 MySQL

    :::bash
    tar zxf mysql-boost-5.7.16.tar.gz -C /usr/local/src

    cd /usr/local/src/mysql-5.7.16
    cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/mysql \
            -DDEFAULT_COLLATION=utf8_general_ci \
            -DDEFAULT_CHARSET=utf8 \
            -DWITH_BOOST=boost
    make && make install

## 配置 MySQL

### 环境变量

    :::bash
    cat > /etc/profile.d/mysql.sh <<EOF
    export PATH="/usr/local/mysql/bin":\$PATH
    EOF

### 配置文件

    :::bash
    cat > /etc/my.cnf <<EOF
    [mysql]
    port                           = 3306
    socket                         = /tmp/mysql.sock

    [mysqld]
    user                           = mysql
    port                           = 3306
    socket                         = /tmp/mysql.sock
    pid-file                       = /tmp/mysql.pid
    log-error                      = /data/mysql/mysql-error.log
    basedir                        = /usr/local/mysql/
    datadir                        = /data/mysql/
    default-storage-engine         = InnoDB
    character-set-server           = utf8
    collation-server               = utf8_general_ci

    key-buffer-size                = 32M
    tmp-table-size                 = 32M
    max-heap-table-size            = 32M
    query-cache-type               = 0
    query-cache-size               = 0
    max-connections                = 500
    thread-cache-size              = 50
    open-files-limit               = 65535
    table-definition-cache         = 1024
    table-open-cache               = 2048

    max-allowed-packet             = 16M
    max-connect-errors             = 1000000
    sql-mode                       = STRICT_ALL_TABLES
    sysdate-is-now                 = 1

    log-bin                        = /data/mysql/mysql-bin
    log-bin-index                  = /data/mysql/mysql-bin.index
    expire-logs-days               = 14
    sync-binlog                    = 1

    server-id                      = 1

    innodb-flush-method            = O_DIRECT
    innodb-log-files-in-group      = 2
    innodb-log-file-size           = 128M
    innodb-flush-log-at-trx-commit = 1
    innodb-file-per-table          = 1
    innodb-buffer-pool-size        = 1456M
    EOF

### 系统服务

    :::bash
    cp support-files/mysql.server /etc/rc.d/init.d/mysql.server
    chmod +x /etc/rc.d/init.d/mysql.server

    chkconfig --add mysql.server

### 初始化

    :::bash
    /usr/local/mysql/bin/mysqld --initialize-insecure
    /usr/local/mysql/bin/mysql_ssl_rsa_setup

## 其他

### c++: Internal error: Killed (program cc1plus)

该问题的原因是 VPS 内存太小且没有 SWAP 分区。解决方案是创建 SWAP 分区：

    :::bash
    dd if=/dev/zero of=/swapfile bs=64M count=16
    chmod 0600 /swapfile
    mkswap /swapfile
    swapon /swapfile

使用完毕后关闭 SWAP 分区：

    :::bash
    swapoff -a
