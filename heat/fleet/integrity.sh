#!/usr/bin/env bash

function go_to_dirname
{
    echo "Go to working directory..."
    cd $( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd -L && pwd -P )
    if [ $? -ne 0 ]
    then
        echo "go_to_dirname failed";
        exit 1
    fi
    echo "-> Current directory is" $(pwd)
}

go_to_dirname


../../scripts/heat_tools/stack_integrity.py \
-v True \
-f fleet.yaml \
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