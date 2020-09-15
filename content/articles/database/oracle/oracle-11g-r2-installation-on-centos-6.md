Title: 安装 Oracle Database 11g R2
Date: 2014-07-19 00:00:00
Modified: 2014-07-19 00:00:00
Category: Database
Tags: Oracle
Slug: oracle-11g-r2-installation-on-centos-6
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

### 配置主机名

    :::bash
    cat > /etc/sysconfig/network <<EOF
    NETWORKING=yes
    HOSTNAME=oracle11gr2
    EOF

### 配置 hosts

    :::bash
    cat > /etc/hosts <<EOF
    127.0.0.1     localhost
    192.168.86.6  oracle11gr2
    EOF

### 安装依赖软件包

    :::bash
    yum -y install binutils.x86_64 \
                   compat-libcap1.x86_64 \
                   compat-libstdc++-33.x86_64 \
                   compat-libstdc++-33.i686 \
                   gcc.x86_64 \
                   gcc-c++.x86_64 \
                   glibc.x86_64 \
                   glibc.i686 \
                   glibc-devel.x86_64 \
                   glibc-devel.i686 \
                   ksh.x86_64 \
                   libgcc.x86_64 \
                   libgcc.i686 \
                   libstdc++.x86_64 \
                   libstdc++.i686 \
                   libstdc++-devel.x86_64 \
                   libstdc++-devel.i686 \
                   libaio.x86_64 \
                   libaio.i686 \
                   libaio-devel.x86_64 \
                   libaio-devel.i686 \
                   make.x86_64 \
                   sysstat.x86_64

### 创建 oracle 组和账号

    :::bash
    groupadd oinstall
    groupadd dba
    useradd -g oinstall -G dba oracle
    echo "oracle" | passwd oracle --stdin

### 配置系统参数

    :::bash
    cat >> /etc/sysctl.conf <<EOF
    fs.aio-max-nr = 1048576
    fs.file-max = 6815744
    # kernel.shmall = Total RAM in bytes / PAGE_SIZE
    kernel.shmall = 2097152
    # kernel.shmmax = Half of total RAM in bytes
    kernel.shmmax = 536870912
    kernel.shmmni = 4096
    kernel.sem = 250 32000 100 128
    net.ipv4.ip_local_port_range = 9000 65500
    net.core.rmem_default = 262144
    net.core.rmem_max = 4194304
    net.core.wmem_default = 262144
    net.core.wmem_max = 1048576
    vm.swappiness = 0
    vm.dirty_background_ratio = 3
    vm.dirty_ratio = 80
    vm.dirty_expire_centisecs = 500
    vm.dirty_writeback_centisecs = 100
    EOF
    sysctl -p

    cat >> /etc/pam.d/login <<EOF
    session required pam_limits.so
    EOF

    cat >> /etc/security/limits.conf <<EOF
    oracle soft nofile 1024
    oracle hard nofile 65536
    oracle soft nproc 2047
    oracle hard nproc 16384
    oracle soft stack 10240
    oracle hard stack 32768
    EOF

### 配置环境变量

    :::bash
    cat > /home/oracle/.bash_profile <<EOF
    # .bash_profile

    # Get the aliases and functions
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi

    # User specific environment and startup programs
    ORACLE_BASE=/home/oracle/app/oracle
    export ORACLE_BASE
    ORACLE_HOME=\$ORACLE_BASE/product/11.2.0/dbhome_1
    export ORACLE_HOME
    ORACLE_SID=ORCL
    export ORACLE_SID
    NLS_LANG=AMERICAN_AMERICA.ZHS16GBK
    export NLS_LANG
    LD_LIBRARY_PATH=\$ORACLE_HOME/lib
    export LD_LIBRARY_PATH
    PATH=\$ORACLE_HOME/bin:\$PATH
    export PATH
    EOF

## 执行安装

    :::bash
    sh ./runInstaller
