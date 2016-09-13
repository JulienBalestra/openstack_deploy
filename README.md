# Openstack and goodies

[![Build Status](https://travis-ci.org/JulienBalestra/openstack_deploy.svg?branch=master)](https://travis-ci.org/JulienBalestra/openstack_deploy)

## Heat Stacks

* Computor (42 school application)
* CoreOS RamDisk (iPXE)
* AutoScaling without nested Stack
* Etcd prototypes
* Get a working instance as fast as possible
* fleet stack for kubernetes
* http benchmark
* Jenkins slave prototype
* library for registries
* AutoScaling with nested Stack
* LB without LBaaS prototype

The lastest production ready stack is the heat/fleet called by
 
    make -C heat/fleet instance
    make -C heat/fleet image
    make -C heat/fleet fleet

## Utilities

* HAProxy
* Stack Integrity (heat template-validate is not enough)
