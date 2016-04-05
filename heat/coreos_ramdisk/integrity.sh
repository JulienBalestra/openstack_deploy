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
-f coreos.yaml \
-r registry.yaml \
-P  "context" \
    "coreos_image" \
    "bastion_image" \
    "coreos_flavor" \
    "bastion_flavor" \
    "dns_nameservers" \
    "key_name" \
    "floatingip_network_name"