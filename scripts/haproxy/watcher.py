#! /usr/bin/python
import json
import subprocess
import argparse
import urllib2
import socket


class Watcher(object):
	def __init__(self, meta_url, hajson_path, hacfg_path, habase_path, port):
		self.meta_url = meta_url
		self.metadata_servers = list()
		self.hajson_path = hajson_path
		self.haproxy_servers = list()
		self.hacfg_path = hacfg_path
		self.habase_path = habase_path
		self.port = port

	@staticmethod
	def is_ip(string):
		try:
			socket.inet_aton(string)
			return True
		except socket.error:
			return False

	def _get_metadata(self):
		req = urllib2.Request(self.meta_url)
		res = urllib2.urlopen(req)
		metadata = json.loads(res.read())
		res.close()
		self.metadata_servers = json.loads(metadata.get('meta', {}).get('servers', '[]'))
		if type(self.metadata_servers) is not list:
			raise TypeError("%s:%s" % (self.metadata_servers, type(self.metadata_servers)))
		for ip in self.metadata_servers:
			if self.is_ip(ip) is False:
				raise TypeError(
					"not a valid IP address [%s] %s:%s" % (ip, self.metadata_servers, type(self.metadata_servers)))
		return self.metadata_servers

	def _get_current_server_list(self):
		with open(self.hajson_path, 'r') as curr:
			self.haproxy_servers = json.loads(curr.read())

	def _need_update(self):
		self.metadata_servers.sort()
		self.haproxy_servers.sort()
		if self.metadata_servers == self.haproxy_servers:
			return False
		return True

	def _update_haproxy_json(self):
		with open(self.hajson_path, "wt") as jcfg:
			jcfg.write(json.dumps(self.metadata_servers))

	def _generate_new_haproxy_cfg(self):
		with open(self.habase_path, "r") as ref:
			reference = ref.read()

		with open(self.hacfg_path, "wt") as ha_cfg:
			ha_cfg.write(reference)
			ha_cfg.write("""
listen app *:80
	mode http
	balance roundrobin
	option httpclose
	option forwardfor\n""")
			for i, ip in enumerate(self.metadata_servers):
				ha_cfg.write('    server server-{0} {1}:{2}\n'.format(i, ip, self.port))

	def _reload_service(self):
		cmd = ['/usr/sbin/service', 'haproxy', 'reload']
		ret = subprocess.call(cmd)
		if ret != 0:
			raise SystemError("cant reload config %s" % " ".join(cmd))

	def do(self):
		self._get_metadata()
		self._get_current_server_list()
		if self._need_update():
			self._update_haproxy_json()
			self._generate_new_haproxy_cfg()
			self._reload_service()


if __name__ == "__main__":
	args = argparse.ArgumentParser()
	args.add_argument('-p', '--port', type=int, default=80, help='Destination port')
	args.add_argument('-m', '--meta_url', type=str, default="http://169.254.169.254/openstack/latest/meta_data.json",
					  help='URL for metadata')
	args.add_argument('-j', '--haproxy_json', type=str, default="/etc/haproxy/servers.json",
					  help='HA Proxy Json list of servers')
	args.add_argument('-c', '--haproxy_config', type=str, default="/etc/haproxy/haproxy.cfg",
					  help='HA Proxy config file')
	args.add_argument('-b', '--haproxy_base', type=str, default="/etc/haproxy/haproxy_base.cfg",
					  help='HA Proxy base for config file')
	ap = args.parse_args()
	w = Watcher(meta_url=ap.meta_url,
				hajson_path=ap.haproxy_json,
				hacfg_path=ap.haproxy_config,
				habase_path=ap.haproxy_base,
				port=ap.port)
	w.do()
