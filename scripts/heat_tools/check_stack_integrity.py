import yaml


class CheckStackIntegrity(object):
	def __init__(self, file_path):
		self.content = self._get_content(file_path)
		self.parameters = self.content["parameters"]
		self.outputs = self.content["outputs"]
		self.heat_template_version = self.content["heat_template_version"]
		self.description = self.content["description"]
		self.resources = self.content["resources"]
		self.used_params = set()
		self.declared_params = set()

	@staticmethod
	def _get_content(file_path):
		with open(file_path, 'r') as fd:
			return yaml.load(fd)

	def _find_orphans_params(self):
		print self.parameters

	def _set_used_type(self, get_type, section):
		if type(section) is list:
			for i in section:
				CheckStackIntegrity._set_used_type(self, get_type, i)
		elif type(section) is dict:
			for key, value in section.iteritems():
				if key == get_type:
					self.used_params.add(value)
				else:
					CheckStackIntegrity._set_used_type(self, get_type, value)

	def _set_parameters_section(self):
		for i in self.parameters:
			self.declared_params.add(i)

	def assert_params_equality(self):
		self._set_parameters_section()
		self._set_used_type('get_param', self.resources)
		assert self.declared_params == self.used_params


if __name__ == "__main__":
	p = CheckStackIntegrity("etcd.yaml")
	p.assert_params_equality()
