# Requirements

### Generate the Debian 8 image

#### Requirements

**Inside the image:**
- /etc/apt/source.list
- cloud-init
- modprobe tun
- modprobe ip_tables


**Over HTTP/s:**
- confd
- rkt
- fleet
- etcd2
- flannel
- docker



### Run the Fleet instance

**http://endpoint/aci**:
- kafka.aci
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