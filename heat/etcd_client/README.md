# Requirements

## Discovery check

    ./integrity.sh


## Discovery stack

    curl -X PUT http://myetcd.local/v2/keys/discovery/_token/_config/size -d value=3
    DISCOVERY="http://myetcd.local/v2/keys/discovery/_token"
    
    heat stack-create \
    -f etcd.yaml  \
    -P "context=my_custom-" \
    -P image= \
    -P flavor= \
    -P dns_nameservers= \
    -P key_name= \
    -P etcd_tar= \
    -P plug_to_router= \
    -P etcd_discovery_url= \
    -e registry.yaml
