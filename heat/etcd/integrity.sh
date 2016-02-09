#!/usr/bin/env bash

function go_to_dirname
{
    echo "Go to working directory..."
    cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    if [ $? -ne 0 ]
    then
        echo "go_to_dirname failed";
        exit 1
    fi
    echo "-> Current directory is" $(pwd)
}

go_to_dirname


sti \
-v True \
-f etcd.yaml \
-r registry.yaml \
-P  "context" \
    "image" \
    "flavor" \
    "dns_nameservers" \
    "key_name" \
    "bastion_size" \
    "etcd_tar"\
    "vulcand_tar" \
    "floatingip_network_name"