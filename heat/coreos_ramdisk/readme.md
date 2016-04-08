# Requirements

## Parameters

You'll need the following parameters to create the stack:

* coreos_image=coreos_ipxe
* coreos_flavor=m1.highmem
* dns_nameservers=8.8.8.8
* key_name=keypair
* floatingip_network_name=public
* bastion_image=Debian Jessie
* bastion_flavor=m1.tiny

Run like:


    heat stack-create coreos0 -f coreos.yaml -e registry.yaml \
    -P "coreos_image="                      # TODO: Here specific coreos_ipxe.iso \
    -P "coreos_flavor="                     # TODO: Here specific at least 8 GB memory  \  
    -P "key_name="                          # TODO: Here public keyname  \
    -P "dns_nameservers=8.8.8.8"            # Generic: Google DNS  \
    -P "floatingip_network_name=public"     # Generic: public network  \
    -P "bastion_image=Debian Jessie"        # Generic: Debian latest  \
    -P "bastion_flavor=m1.tiny"             # Generic: smaller flavor
