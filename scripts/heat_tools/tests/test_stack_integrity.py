import unittest
import os

from scripts.heat_tools import stack_integrity


class TestCheckStackIntegrityValid(unittest.TestCase):
	file_path = "test_resources/etcd_valid.yaml"
	csi = stack_integrity.StackIntegrity

	@classmethod
	def setUpClass(cls):
		os.chdir(os.path.dirname(__file__))
		cls.csi = stack_integrity.StackIntegrity(cls.file_path)

	def test_parameters(self):
		self.csi.assert_params_equality()

	def test_outputs(self):
		self.csi.capable_outputs()


class TestCheckStackIntegrityInvalid(unittest.TestCase):
	file_path = "test_resources/etcd_invalid.yaml"
	csi = stack_integrity.StackIntegrity

	@classmethod
	def setUpClass(cls):
		os.chdir(os.path.dirname(__file__))
		cls.csi = stack_integrity.StackIntegrity(cls.file_path)

	def test_parameters(self):
		with self.assertRaises(AssertionError):
			self.csi.assert_params_equality()

	def test_outputs(self):
		with self.assertRaises(AssertionError):
			self.csi.capable_outputs()
