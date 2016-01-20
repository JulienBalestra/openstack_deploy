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
    
    
### Tips


Outputs :

* { get_attr: [web_group, outputs, ip] } : 

[
    [
        {"net-rbHIus": ["192.168.1.101"]},
        {"net-rbHIus": ["192.168.1.100"]}
    ]
]

* { get_attr: [web_group, outputs_list, networks] } : 

[
   {
     "output_value": [
       {
         "5vanad2iowvf": [
           "192.168.1.104"
         ]
       }
]

Meta : "[\".member.0.nkvbx2sn3rk6=[u'192.168.1.105']\", \".member.0.4ncdtfgwnuiz=[u'192.168.1.104']\"]"