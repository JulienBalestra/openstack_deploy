   
# Run

### Fleet stack have:

* Etcd v3
* Flannel
* Rkt
* Docker
* SkyDNS
* Zookeeper
* Kafka
* Elasticsearch
* Logstash
* Kibana
* Journald Stream
* Traefik

### Start
    
    make check
    make instance
    make instance_off
    make image
    
    # Fleet standalone
    make fleet    
    make fleet_add_extra_member  
    make fleet_delete
    
    # Fleet for Kubernetes
    make kubernetes


# Requirements

### Generate the Debian 8 image or Ubuntu 16.04

Keep in mind the Debian 8 couldn't be used for Kubernetes (Rktnetes) because of the version of the Kernel and Systemd version

#### Requirements

**Inside the image:**
- /etc/apt/source.list
- cloud-init
- modprobe tun
- modprobe ip_tables
- systemd-container


**Over HTTP/s:**

- confd - https://github.com/kelseyhightower/confd/releases
- docker - https://github.com/docker/docker/releases
- rkt - https://github.com/coreos/rkt/releases
- fleet - https://github.com/coreos/fleet/releases
- netenv - https://github.com/kelseyhightower/setup-network-environment/releases
- etcd3 - https://github.com/coreos/etcd/releases
- flannel - docker://quay.io/coreos/flannel
- kubernetes

- ACI_URL - bucket to store aci



### Run the Fleet instance

**http://endpoint/aci**:
- elasticsearch.aci
- jds_kafka.aci
- kafka.aci
- kibana.aci
- logstash.aci
- skydns.aci
- traefik.aci
- zookeeper.aci


### Convert Docker to ACI

**Elasticsearch:**

    docker pull elasticsearch:latest
    docker save -o elasticsearch.tar.gz elasticsearch:latest
    docker2aci --image=./elasticsearch elasticsearch.tar.gz
    mv elasticsearch-latest.aci elasticsearch.aci

    ls -lhGg
    total 491M
    -rw------- 1 153M Jun 23 10:36 elasticsearch.aci
    -rw------- 1 339M Jun 23 10:35 elasticsearch.tar.gz
    
### Export the following environment

    export OS_AUTH_URL=
    export OS_TENANT_ID=
    export OS_TENANT_NAME=
    export OS_USERNAME=
    export OS_PASSWORD=
    export OS_REGION_NAME=
           
    export KEY_NAME=
    export FLAVOR_INSTANCE=
    export PUB_KEY=
    export DNS_NS=
    export BUCKET=
    export PROXY=
    export NTP=
    export NTPFALL=
    export PHONE_HOME=
    
    export CC=/usr/local/bin/go
    export GOROOT=/usr/local/src/go

