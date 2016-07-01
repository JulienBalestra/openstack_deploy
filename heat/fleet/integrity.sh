#!/usr/bin/env bash

set -e

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
-f base.yaml \
-P  "context" \
    "floatingip_network_name"

../../scripts/heat_tools/stack_integrity.py \
-v True \
-f generate_image.yaml \
-r registry.yaml \
-P key_name \
 floatingip_network_name \
 flavor \
 image \
 dns_nameservers \
 etcd_tar \
 fleet_tar \
 confd_bin \
 rkt_tar \
 ssh_authorized_keys \
 aci_url \
 docker_tar \
 netenv_bin \
 flannel_tar

../../scripts/heat_tools/stack_integrity.py \
-v True \
-f etcd_static.yaml \
-r registry.yaml \
-P key_name \
 flavor \
 image \
 dns_nameservers \
 router


../../scripts/heat_tools/stack_integrity.py \
-v True \
-f fleet_stateless.yaml \
-r registry.yaml \
-P key_name \
 flavor \
 image \
 dns_nameservers \
 router \
 etcd_initial_cluster \
 floatingip_network_name

../../scripts/heat_tools/stack_integrity.py \
-v True \
-f fleet_statefull.yaml \
-r registry.yaml \
-P key_name \
 flavor \
 image \
 dns_nameservers \
 router \
 etcd_initial_cluster

../../scripts/heat_tools/stack_integrity.py \
-v True \
-f all.yaml \
-r registry.yaml \
-P key_name \
 flavor \
 image \
 dns_nameservers \
 flavor_static \
 flavor_stateless \
 flavor_statefull \
 floatingip_network_name

