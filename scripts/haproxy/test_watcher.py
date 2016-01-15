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
			a.read.side_effect = [json.dumps({"servers": ["192.168.0.1"]})]
			mock_urlopen.return_value = a
			res = self.w._get_metadata()
			assert res == [u'192.168.0.1']

		mock_metadata()
		self.assertEqual([u'192.168.0.1'], self.w.metadata_servers)

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
			self.assertEqual('["192.168.0.1"]', f.read())

	def test_04_generate_new_haproxy_cfg(self):
		self.w._generate_new_haproxy_cfg()
		with open(self.hacfg_path, 'r') as cfg:
			content = cfg.read()
		self.assertIn("    server server-0 192.168.0.1:80", content)


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
			f.write('["192.168.0.1"]')

	@classmethod
	def tearDownClass(cls):
		with open("etc_haproxy_servers.json", 'w') as f:
			f.write("[]")

	def test_00_get_metadata(self):
		@patch('watcher.urllib2.urlopen')
		def mock_metadata(mock_urlopen):
			a = Mock()
			a.read.side_effect = [json.dumps({"servers": ["192.168.0.1"]})]
			mock_urlopen.return_value = a
			res = self.w._get_metadata()
			assert res == [u'192.168.0.1']

		mock_metadata()
		self.assertEqual([u'192.168.0.1'], self.w.metadata_servers)

	def test_01_get_current_server_list(self):
		self.w._get_current_server_list()
		self.assertEqual([u'192.168.0.1'], self.w.haproxy_servers)

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
			a.read.side_effect = [json.dumps({"notserver": ["192.168.0.1"]})]
			mock_urlopen.return_value = a
			res = self.w._get_metadata()
			assert res == [u'192.168.0.1']

		with self.assertRaises(KeyError):
			mock_metadata()


if __name__ == "__main__":
	unittest.main()
