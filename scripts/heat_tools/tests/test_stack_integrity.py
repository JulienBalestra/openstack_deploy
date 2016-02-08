import unittest
import os

from scripts.heat_tools import stack_integrity


class ValidTestCheckStackIntegrity(unittest.TestCase):
	context = "%s/%s" % (os.path.dirname(__file__), 'test_resources/valid_etcd')
	stack_file_path = "etcd.yaml"
	registry_file_path = "registry.yaml"
	csi = stack_integrity.StackIntegrity
	parameters = ["context", "image", "flavor", "dns_nameservers",
				  "floatingip_network_name", "key_name", "bastion_size",
				  "etcd_tar", "vulcand_tar"]

	@classmethod
	def setUpClass(cls):
		os.chdir(cls.context)
		cls.csi = stack_integrity.StackIntegrity(
				cls.stack_file_path, cls.registry_file_path, cls.parameters)

	def test_parameters(self):
		self.csi.assert_params_equality()
		self.csi.capable_parameters()

	def test_outputs(self):
		self.csi.capable_outputs()

	def test_resources(self):
		self.csi.capable_resources()

	def test_depends(self):
		self.csi.right_depends()

	def test_follow_nested(self):
		self.csi.follow_nested_stack()

	def test_do_all(self):
		self.csi.do_all()


class InvalidTestCheckStackIntegrity(unittest.TestCase):
	context = "%s/%s" % (os.path.dirname(__file__), 'test_resources/invalid_etcd')
	stack_file_path = "etcd.yaml"
	registry_file_path = "registry.yaml"
	csi = stack_integrity.StackIntegrity
	parameters = ["context", "image", "flavor", "dns_nameservers",
				  "key_name", "bastion_size", "etcd_tar", "vulcand_tar"]

	@classmethod
	def setUpClass(cls):
		os.chdir(cls.context)
		cls.csi = stack_integrity.StackIntegrity(
				cls.stack_file_path, cls.registry_file_path, cls.parameters)

	def test_parameters(self):
		with self.assertRaises(AssertionError):
			self.csi.assert_params_equality()
		with self.assertRaises(AssertionError):
			self.csi.capable_parameters()

	def test_outputs(self):
		with self.assertRaises(AssertionError):
			self.csi.capable_outputs()

	def test_resources(self):
		with self.assertRaises(AssertionError):
			self.csi.capable_resources()

	def test_depends(self):
		with self.assertRaises(AssertionError):
			self.csi.right_depends()
