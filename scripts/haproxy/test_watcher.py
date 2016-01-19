import unittest
import os

import json
from mock import patch, Mock

import watcher


class TestWatcherModify(unittest.TestCase):
	w = type(watcher.Watcher)
	hajson_path = "etc_haproxy_servers.json"
	hacfg_path = "etc_haproxy_haproxy.cfg"
	habase_path = "etc_haproxy_haproxy_base.cfg"

	@classmethod
	def setUpClass(cls):
		os.chdir("%s/test_resources" % os.path.dirname(__file__))
		cls.w = watcher.Watcher(
				meta_url="mock",
				hajson_path=cls.hajson_path,
				hacfg_path=cls.hacfg_path,
				habase_path=cls.habase_path,
				port=80
		)

	@classmethod
	def tearDownClass(cls):
		with open("etc_haproxy_servers.json", 'w') as f:
			f.write("[]")

	def test_00_get_metadata(self):
		@patch('watcher.urllib2.urlopen')
		def mock_metadata(mock_urlopen):
			a = Mock()
			a.read.side_effect = [json.dumps(
					{
						"random_seed": "value",
						"uuid": "value",
						"availability_zone": "value",
						"hostname": "value",
						"launch_index": 0,
						"meta": {
							"autoscaling_networks": '[[{"net-rbHIus": ["192.168.1.101"]},{"net-rbHIus": ["192.168.1.100"]}]]'
						},
						"public_keys": {
							"public": "value Generated-by-Nova"
						},
						"name": "value"
					}

			)]
			mock_urlopen.return_value = a
			res = self.w._get_metadata()
			assert res == [u'192.168.1.101', u'192.168.1.100']

		mock_metadata()
		self.assertEqual([u'192.168.1.101', u'192.168.1.100'], self.w.metadata_servers)

	def test_01_get_current_server_list(self):
		self.w._get_current_server_list()
		self.assertEqual([], self.w.haproxy_servers)

	def test_02_need_update(self):
		self.assertTrue(self.w._need_update())

	def test_03_update_haproxy_json(self):
		with open(self.w.hajson_path, 'r') as f:
			self.assertEqual('[]', f.read())
		self.w._update_haproxy_json()
		with open(self.w.hajson_path, 'r') as f:
			self.assertEqual('["192.168.1.100", "192.168.1.101"]', f.read())

	def test_04_generate_new_haproxy_cfg(self):
		self.w._generate_new_haproxy_cfg()
		with open(self.hacfg_path, 'r') as cfg:
			content = cfg.read()
		self.assertIn("    server server-0 192.168.1.100:80", content)
		self.assertIn("    server server-1 192.168.1.101:80", content)


class TestWatcherunModify(unittest.TestCase):
	w = type(watcher.Watcher)
	hajson_path = "etc_haproxy_servers.json"
	hacfg_path = "etc_haproxy_haproxy.cfg"
	habase_path = "etc_haproxy_haproxy_base.cfg"

	@classmethod
	def setUpClass(cls):
		os.chdir("%s/test_resources" % os.path.dirname(__file__))
		cls.w = watcher.Watcher(
				meta_url="mock",
				hajson_path=cls.hajson_path,
				hacfg_path=cls.hacfg_path,
				habase_path=cls.habase_path,
				port=80
		)
		with open("etc_haproxy_servers.json", 'w') as f:
			f.write('["192.168.1.101", "192.168.1.100"]')

	@classmethod
	def tearDownClass(cls):
		with open("etc_haproxy_servers.json", 'w') as f:
			f.write("[]")

	def test_00_get_metadata(self):
		@patch('watcher.urllib2.urlopen')
		def mock_metadata(mock_urlopen):
			a = Mock()
			a.read.side_effect = [json.dumps(
					{
						"random_seed": "value",
						"uuid": "value",
						"availability_zone": "value",
						"hostname": "value",
						"launch_index": 0,
						"meta": {
							"autoscaling_networks": '[[{"net-rbHIus": ["192.168.1.101"]},{"net-rbHIus": ["192.168.1.100"]}]]'
						},
						"public_keys": {
							"public": "value Generated-by-Nova"
						},
						"name": "value"
					}

			)]
			mock_urlopen.return_value = a
			res = self.w._get_metadata()
			assert res == [u'192.168.1.101', u'192.168.1.100']

		mock_metadata()
		self.assertEqual([u'192.168.1.101', u'192.168.1.100'], self.w.metadata_servers)

	def test_01_get_current_server_list(self):
		self.w._get_current_server_list()
		self.assertEqual([u'192.168.1.101', u'192.168.1.100'], self.w.haproxy_servers)

	def test_02_need_update(self):
		self.assertFalse(self.w._need_update())


class TestWatcherEmpty(unittest.TestCase):
	w = type(watcher.Watcher)
	hajson_path = "etc_haproxy_servers.json"
	hacfg_path = "etc_haproxy_haproxy.cfg"
	habase_path = "etc_haproxy_haproxy_base.cfg"

	@classmethod
	def setUpClass(cls):
		os.chdir("%s/test_resources" % os.path.dirname(__file__))
		cls.w = watcher.Watcher(
				meta_url="mock",
				hajson_path=cls.hajson_path,
				hacfg_path=cls.hacfg_path,
				habase_path=cls.habase_path,
				port=80
		)

	@classmethod
	def tearDownClass(cls):
		with open("etc_haproxy_servers.json", 'w') as f:
			f.write("[]")

	def test_00_get_metadata(self):
		@patch('watcher.urllib2.urlopen')
		def mock_metadata(mock_urlopen):
			a = Mock()
			a.read.side_effect = [json.dumps(
					{
						"random_seed": "value",
						"uuid": "value",
						"availability_zone": "value",
						"hostname": "value",
						"launch_index": 0,
						"meta": {
							"autoscaling_networks": '[[]]'
						},
						"public_keys": {
							"public": "value Generated-by-Nova"
						},
						"name": "value"
					}

			)]
			mock_urlopen.return_value = a
			res = self.w._get_metadata()
			assert res == []

		mock_metadata()
		self.assertEqual([], self.w.metadata_servers)


class TestWatcherInvalidIP(unittest.TestCase):
	w = type(watcher.Watcher)
	hajson_path = "etc_haproxy_servers.json"
	hacfg_path = "etc_haproxy_haproxy.cfg"
	habase_path = "etc_haproxy_haproxy_base.cfg"

	@classmethod
	def setUpClass(cls):
		os.chdir("%s/test_resources" % os.path.dirname(__file__))
		cls.w = watcher.Watcher(
				meta_url="mock",
				hajson_path=cls.hajson_path,
				hacfg_path=cls.hacfg_path,
				habase_path=cls.habase_path,
				port=80
		)

	@classmethod
	def tearDownClass(cls):
		with open("etc_haproxy_servers.json", 'w') as f:
			f.write("[]")

	def test_00_get_metadata(self):
		@patch('watcher.urllib2.urlopen')
		def mock_metadata(mock_urlopen):
			a = Mock()
			a.read.side_effect = [json.dumps(
					{
						"random_seed": "value",
						"uuid": "value",
						"availability_zone": "value",
						"hostname": "value",
						"launch_index": 0,
						"meta": {
							"autoscaling_networks": '[[{"net-rbHIus": ["titi"]},{"net-rbHIus": ["toto"]}]]'
						},
						"public_keys": {
							"public": "value Generated-by-Nova"
						},
						"name": "value"
					}

			)]
			mock_urlopen.return_value = a
			res = self.w._get_metadata()
			assert res == []

		with self.assertRaises(TypeError):
			mock_metadata()


if __name__ == "__main__":
	unittest.main()
