KUBERNETES=kubernetes
FLEET=fleet

GLANCE_IMG=fleet

IMG=image
INSTANCE=instance
INSTANCE_OUTPUT=instance_id
HAPPY_END=generate_finished_well

FLAGS=--insecure
$(eval NOW := $(shell date +%s))

$(eval GOPATH := $(shell pwd))
PHONE_PORT=80
PHONE=phone
SUDO=sudo


GO_SRCS = get_phone/phone.go

default: all

$(PHONE): $(GO_SRCS)
	GOPATH=$(GOPATH) $(CC) build -o $(PHONE) get_phone/phone.go

clean:
	@openstack $(FLAGS) stack delete --yes --wait $(KUBERNETES) || true
	@openstack $(FLAGS) stack delete --yes --wait $(FLEET) || true

fclean: clean
	@openstack $(FLAGS) stack delete --yes --wait $(INSTANCE) || true
	@openstack $(FLAGS) image delete $(IMG) || true
	@test -f $(IMG) && rm -v $(IMG) || true
	@rm $(PHONE) || true

check:
	@test '$(KEY_NAME)'
	@test '$(PUB_KEY)'
	@test '$(DNS_NS)'
	@test '$(BUCKET)'
	@test '$(PROXY)'
	@test '$(NTP)'
	@test '$(NTPFALL)'
	@test '$(KUBERNETES)'
	@test '$(FLEET)'
	@test '$(IMG)'
	@test '$(INSTANCE)'
	@test '$(FLAVOR_INSTANCE)'
	@test '$(NOW)'
	@test '$(PHONE_HOME)'
	@echo {} | jq . > /dev/null

$(INSTANCE): check
	@openstack --insecure stack output show instance instance_id -f json -c output_value || \
	openstack $(FLAGS) stack create $(INSTANCE) \
	-t generate_image.yaml \
	-e registry.yaml \
	--parameter apt_proxy="$(PROXY)" \
	--parameter key_name='$(KEY_NAME)' \
	--parameter floatingip_network_name='ext-net' \
	--parameter flavor='m1.small' \
	--parameter image='ubuntu-16.04-server' \
	--parameter dns_nameservers='$(DNS_NS)' \
	--parameter etcd_tar="$(BUCKET)/etcd/etcd-v3.0.4-linux-amd64.tar.gz" \
	--parameter fleet_tar="$(BUCKET)/fleet/fleet-v0.11.7-linux-amd64.tar.gz" \
	--parameter confd_bin="$(BUCKET)/confd/confd-0.11.0-linux-amd64" \
	--parameter rkt_tar="$(BUCKET)/rkt/rkt-v1.12.0.tar.gz" \
	--parameter flannel_tar="$(BUCKET)/flannel/flannel.tar.gz" \
	--parameter docker_tar="$(BUCKET)/docker/docker-1.11.2.tgz" \
	--parameter cni_tar="$(BUCKET)/cni/cni-v0.3.0.tar.gz" \
	--parameter kubernetes_tar="$(BUCKET)/kubernetes/kubernetes-server-linux-amd64.tar.gz" \
	--parameter netenv_bin="$(BUCKET)/netenv/setup-network-environment" \
	--parameter torus_tar="$(BUCKET)/torus/torus_v0.1.1_linux_386.tar.gz" \
	--parameter aci_url="$(BUCKET)/aci" \
	--parameter ssh_authorized_keys="$(PUB_KEY)" \
	--parameter ntp="$(NTP)" \
	--parameter ntpfall="$(NTPFALL)" \
	--parameter phone="$(PHONE_HOME)" \
	--wait

instance_off: instance_finished_well
	$(shell openstack $(FLAGS) server show \
	    $(shell openstack $(FLAGS) stack output show $(INSTANCE) $(INSTANCE_OUTPUT) -f json -c output_value | \
	        jq -r .[0].Value) \
	    -f json | jq -r '.[1].Value == "Shutdown"')

instance_finished_well: check
	openstack $(FLAGS) console log show $(shell openstack $(FLAGS) stack output show $(INSTANCE) $(INSTANCE_OUTPUT) -f json -c output_value | \
        jq -r .[0].Value) | grep -wc $(HAPPY_END)

$(IMG): instance_off
	openstack --insecure stack output show instance instance_id -f json -c output_value | \
        jq -r .[0].Value | xargs -I {} openstack $(FLAGS) image create --id {} $(GLANCE_IMG)
	touch $(IMG)


$(KUBERNETES): check
	@openstack $(FLAGS) stack create $(KUBERNETES) \
	-t $(KUBERNETES).yaml \
	-e registry.yaml \
	--parameter key_name=$(KEY_NAME) \
	--parameter flavor_static='m1.medium' \
	--parameter flavor_stateless="m1.large" \
	--parameter flavor_statefull="m1.large" \
	--parameter image='$(GLANCE_IMG)' \
	--parameter dns_nameservers=$(DNS_NS) \
	--parameter floatingip_network_name='ext-net' \
	--wait

$(FLEET): check
	@openstack $(FLAGS) stack create $(FLEET) \
	-t $(FLEET).yaml \
	-e registry.yaml \
	--parameter key_name=$(KEY_NAME) \
	--parameter flavor_static='m1.medium' \
	--parameter flavor_stateless="m1.large" \
	--parameter flavor_statefull="m1.large" \
	--parameter image='$(GLANCE_IMG)' \
	--parameter dns_nameservers=$(DNS_NS) \
	--parameter floatingip_network_name='ext-net' \
	--wait

fleet_add_extra_member: check
	@./add_member.sh

fleet_delete_extra_member: check
	@./delete_member.sh

fleet_delete_extra_members: check
	@./delete_member.sh all

fleet_delete: fleet_delete_extra_members
	openstack $(FLAGS) stack delete --yes $(FLEET) --wait

.PHONY: all instance $(IMG) $(INSTANCE) check fclean clean $(PHONE) $(FLEET) $(KUBERNETES) instance_finished_well instance_off
