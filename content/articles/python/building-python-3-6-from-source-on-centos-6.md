Title: 编译安装 Python 3.6
Date: 2018-05-25 00:00:00
Modified: 2018-05-25 00:00:00
Category: Python
Slug: building-python-3-6-from-source-on-centos-6
Authors: YYCrazy

## 安装准备

    :::bash
    yum -y install gcc gcc-c++ make openssl-devel bzip2-devel zlib-devel xz-devel

### LibreSSL

    :::bash
    wget https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-2.6.4.tar.gz
    tar zxf libressl-2.6.4.tar.gz -C /usr/local/src

    cd /usr/local/src/libressl-2.6.4
    ./configure --prefix=/usr/local/ssl
    make && make install

    cat > /etc/ld.so.conf.d/libressl.conf <<EOF
    /usr/local/ssl/lib
    EOF
    ldconfig

    cat >> ~/.bash_profile <<EOF
    LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/ssl/lib
    export LD_LIBRARY_PATH
    EOF
    source ~/.bash_profile

## 安装 Python

    :::bash
    wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
    tar zxf Python-3.6.5.tgz -C /usr/local/src

    cd /usr/local/src/Python-3.6.5
    ./configure \
        --prefix=/usr/local/python3 \
        --enable-optimizations \
        --enable-shared \
        --enable-ipv6
    make && make install

    cat > /etc/ld.so.conf.d/python3.conf <<EOF
    /usr/local/python3/lib
    EOF
    ldconfig

## 其他

### 配置 PIP 源

    :::bash
    mkdir ~/.pip
    cat > ~/.pip/pip.conf <<EOF
    [global]
    index-url = https://mirrors.aliyun.com/pypi/simple/

    [install]
    trusted-host=mirrors.aliyun.com
    EOF

### 更新 PIP 版本

    :::bash
    /usr/local/python3/bin/python3 -m pip install --upgrade pip
