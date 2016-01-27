# Requirements

## Parameters

You'll need the following parameters to create the "nested_scaling":

* flavor
* image
* floatingip_network_name
* key_name
* dns_nameservers

### flavor


    nova flavor-list


### image


    nova image-list
    glance image-list
    
   
### floatingip_network_name

    
    neutron net-list

    for n in $(neutron net-list | awk '{print $2}' | grep -v id)
    do
    if [ $(neutron net-show ${n} | grep "router:external" | awk '{print $4}') == "True" ]
    then
        neutron net-show ${n}
    fi
    done
    
### key_name

    nova keypair-list
    
    nova keypair-add my_key > my_private_key && chmod 400 my_private_key
    
    
### dns_nameservers

  
    nm-tool | grep DNS 
    cat /etc/resolv.conf