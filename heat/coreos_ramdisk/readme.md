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

    
    neutron net-list --router:external True
    
### key_name

    nova keypair-list
    
    nova keypair-add my_key > my_private_key && chmod 400 my_private_key
    
    
### dns_nameservers

  
    nm-tool | grep DNS 
    cat /etc/resolv.conf