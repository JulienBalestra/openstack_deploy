import unittest
import os

from scripts.heat_tools import check_stack_integrity


class TestCheckStackIntegrity(unittest.TestCase):
	file_path = "test_resources/etcd.yaml"
	csi = check_stack_integrity.CheckStackIntegrity

	@classmethod
	def setUpClass(cls):
		os.chdir(os.path.dirname(__file__))
		cls.csi = check_stack_integrity.CheckStackIntegrity(cls.file_path)

	def test_parameters(self):
		self.csi.assert_params_equality()
