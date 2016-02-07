import yaml


class StackIntegrity(object):
	def __init__(self, file_path):
		self.content = self._get_content(file_path)
		self.parameters = self.content["parameters"]
		self.outputs = self.content["outputs"]
		self.heat_template_version = self.content["heat_template_version"]
		self.description = self.content["description"]
		self.resources = self.content["resources"]

		self.used_params = set()
		self.declared_params = set()

		self.used_outputs = set()
		self.declared_outputs = set()

		self.used_resources = set()
		self.declared_resources = set()

	@staticmethod
	def _get_content(file_path):
		with open(file_path, 'r') as fd:
			return yaml.load(fd)

	def _set_used_type(self, get_type, section, set_to_add):
		if type(section) is list:
			for i in section:
				self._set_used_type(get_type, i, set_to_add)
		elif type(section) is dict:
			for key, value in section.iteritems():
				if key == get_type:
					try:
						set_to_add.add(value)
					except TypeError:
						set_to_add.add(value[0])
				else:
					self._set_used_type(get_type, value, set_to_add)

	def _set_parameters_section(self):
		for i in self.parameters:
			self.declared_params.add(i)

	def assert_params_equality(self):
		self._set_parameters_section()
		self._set_used_type('get_param', self.resources, self.used_params)
		assert self.declared_params == self.used_params

	def capable_outputs(self):
		self._set_used_type('get_attr', self.outputs, self.declared_outputs)
		resources_names = set(self.resources.keys())
		assert len(self.declared_outputs - resources_names) == 0

	def capable_resources(self):
		self._set_used_type('get_resource', self.resources, self.declared_resources)
		resources_names = set(self.resources.keys())
		assert len(self.declared_outputs - resources_names) == 0
