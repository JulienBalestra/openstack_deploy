#!/usr/bin/env bash

python stack_integrity.py \
-f tests/test_resources/valid_etcd/etcd.yaml \
-r tests/test_resources/valid_etcd/registry.yaml \
-P  "context" \
    "image" \
    "flavor" \
    "dns_nameservers" \
    "key_name" \
    "bastion_size" \
    "etcd_tar"\
    "vulcand_tar" \
    "floatingip_network_name"