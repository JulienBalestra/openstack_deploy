STACK=all

GLANCE_IMG=fleet

IMG=image
INSTANCE=instance
INSTANCE_OUTPUT=instance_id

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
	@heat $(FLAGS) stack-delete -y $(STACK) || true
	@test -f $(INSTANCE) && rm -v $(INSTANCE) || true

fclean: clean
	@heat $(FLAGS) stack-delete -y $(INSTANCE) || true
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
	@test '$(STACK)'
	@test '$(IMG)'
	@test '$(INSTANCE)'
	@test '$(FLAVOR_INSTANCE)'
	@test '$(NOW)'
	@test '$(PHONE_HOME)'
	@echo {} | jq . > /dev/null

instance: check
	openstack --insecure stack output show instance instance_id -f json -c output_value | \
		jq -r .[0].Value || \
	openstack $(FLAGS) stack create $(INSTANCE) \
	-t generate_image.yaml \
	-e registry.yaml \
	--parameter key_name='$(KEY_NAME)' \
	--parameter floatingip_network_name='ext-net' \
	--parameter flavor='m1.small' \
	--parameter image='ubuntu-16.04-server' \
	--parameter dns_nameservers='$(DNS_NS)' \
	--parameter etcd_tar="$(BUCKET)/etcd/etcd-v3.0.4-linux-amd64.tar.gz" \
	--parameter fleet_tar="$(BUCKET)/fleet/fleet-v0.11.7-linux-amd64.tar.gz" \
	--parameter confd_bin="$(BUCKET)/confd/confd-0.11.0-linux-amd64" \
	--parameter rkt_tar="$(BUCKET)/rkt/rkt-v1.11.0.tar.gz" \
	--parameter flannel_tar="$(BUCKET)/flannel/flannel.tar.gz" \
	--parameter docker_tar="$(BUCKET)/docker/docker-1.11.2.tgz" \
	--parameter cni_tar="$(BUCKET)/cni/cni-v0.3.0.tar.gz" \
	--parameter kubernetes_tar="$(BUCKET)/kubernetes/kubernetes-server-linux-amd64.tar.gz" \
	--parameter netenv_bin="$(BUCKET)/netenv/setup-network-environment" \
	--parameter torus_tar="$(BUCKET)/torus/torus_v0.1.1_linux_386.tar.gz" \
	--parameter aci_url="$(BUCKET)/aci" \
	--parameter ssh_authorized_keys="$(PUB_KEY)" \
	--parameter apt_proxy="$(PROXY)" \
	--parameter ntp="$(NTP)" \
	--parameter ntpfall="$(NTPFALL)" \
	--parameter phone="$(PHONE_HOME)" \
	--wait

$(IMG): check
	openstack $(FLAGS) image delete $(GLANCE_IMG) || true
	openstack --insecure stack output show instance instance_id -f json -c output_value | \
        		jq -r .[0].Value | xargs -I {} \
		openstack $(FLAGS) image create --id {} $(GLANCE_IMG)
	touch $(IMG)


all: check
	openstack $(FLAGS) stack create $(STACK) \
	-t all.yaml \
	-e registry.yaml \
	--parameter key_name=$(KEY_NAME) \
	--parameter flavor_static='m1.medium' \
	--parameter flavor_stateless="m1.large" \
	--parameter flavor_statefull="m1.large" \
	--parameter image='$(GLANCE_IMG)' \
	--parameter dns_nameservers=$(DNS_NS) \
	--parameter floatingip_network_name='ext-net' \
	--wait

.PHONY: all instance $(IMG) $(INSTANCE) check fclean clean $(PHONE)