#!/bin/bash

set -x
export DEBIAN_FRONTEND=noninteractive

function apt
{
    apt-get -qqy update
    apt-get -qqy upgrade
    apt-get -y install curl python python-dev haproxy
    if [ $? -ne 0 ]
    then
        echo "fail to install packages"
        exit 2
    fi
}

function haproxy_setup
{
    #sed -i 's/ENABLED=0/ENABLED=1/' /etc/default/haproxy
    cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy_base.cfg
    echo [] > /etc/haproxy/servers.json
}

function check_watcher
{
    if [ ! -f "/usr/local/src/haproxy/watcher.py" ]
    then
        echo "/usr/local/src/haproxy/watcher.py not here"
        ls -l /usr/local/src/
        ls -l /usr/local/src/haproxy/
        exit 3
    fi
    # TODO crontab
}

apt
haproxy_setup
check_watcher