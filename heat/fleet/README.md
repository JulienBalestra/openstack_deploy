# Requirements

### Generate the Debian 8 image

#### Requirements

**Inside the image:**
- /etc/apt/source.list
- cloud-init
- modprobe tun


**Over HTTP/s:**
- confd
- rkt
- fleet
- etcd2
- flannel



### Run the Fleet instance

**http://endpoint/aci**:
- kafka.aci
- zookeeper.aci