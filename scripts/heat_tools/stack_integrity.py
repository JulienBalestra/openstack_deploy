#! /usr/bin/python
import yaml
import os
import argparse

STARTING_DIR = os.getcwd()


class StackIntegrity(object):
	appends = ["depends_on"]
	registry_file_directory = None

	def __init__(self, stack_file_path, registry_file_path, parameters=None, verbose=False):
		self.verbose = verbose
		if verbose:
			print "Instance for %s" % stack_file_path
		if parameters:
			self.given_parameters = set([k for k in parameters])

		self.registry_file_path = registry_file_path
		if StackIntegrity.registry_file_directory is None and registry_file_path is not None:
			StackIntegrity.registry_file_directory = os.path.split(os.path.abspath(registry_file_path))[0]

		stack_content = self._get_content(stack_file_path)
		self.parameters = stack_content["parameters"]
		self.outputs = stack_content["outputs"] if stack_content.has_key("outputs") else dict()
		self.heat_template_version = stack_content["heat_template_version"]
		self.description = stack_content["description"]
		self.resources = stack_content["resources"]

		registry_content = self._get_content(registry_file_path) if registry_file_path else None
		self.registries = registry_content["resource_registry"] if registry_file_path else {}

		self.used_params = set()
		self.declared_params = set()
		self.used_outputs = set()
		self.declared_outputs = set()
		self.used_resources = set()
		self.declared_resources = set()
		self.used_registries = set()

	def _get_content(self, file_path):
		if os.path.isfile(file_path) is False:
			os.chdir(self.registry_file_directory)
		if os.path.isfile(file_path) is False:
			os.chdir(STARTING_DIR)
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
						for v in value:
							set_to_add.add(v)
							if get_type not in self.appends:
								break
				else:
					self._set_used_type(get_type, value, set_to_add)

	def _deep_inside_nested_stack(self, get_type, section):
		if type(section) is dict:
			for key, value in section.iteritems():
				if key == "type" and value in self.registries:
					nested_file_path = self.registries[value]
					r = StackIntegrity(
							nested_file_path, self.registry_file_path, section["properties"].keys(), self.verbose)
					r.do_all()
				else:
					self._deep_inside_nested_stack(get_type, value)

	def _set_parameters_section(self):
		for i in self.parameters:
			self.declared_params.add(i)

	def capable_parameters(self):
		is_default = self.declared_params - self.given_parameters
		for i in is_default:
			if self.parameters[i].has_key("default") is False:
				raise AssertionError("%s not in parameters" % i)

	def assert_params_equality(self):
		self._set_parameters_section()
		self._set_used_type('get_param', self.resources, self.used_params)
		if self.declared_params != self.used_params:
			raise AssertionError("%s vs %s" % (
				self.declared_params - self.used_params,
				self.used_params - self.declared_params))

	def capable_outputs(self):
		self._set_used_type('get_attr', self.outputs, self.declared_outputs)
		resources_names = set(self.resources.keys())
		assert len(self.declared_outputs - resources_names) == 0

	def capable_resources(self):
		attr_set = set()
		resources_set = set(self.resources.keys())
		self._set_used_type('get_resource', self.resources, self.declared_resources)
		self._set_used_type('get_attr', self.resources, attr_set)

		if len(set(attr_set - resources_set)) != 0:
			raise AssertionError("%s" % set(attr_set - resources_set))
		resources_names = set(self.resources.keys())
		assert len(self.declared_outputs - resources_names) == 0

	def right_depends(self):
		depends = set()
		resources_keys_set = set(self.resources.keys())
		self._set_used_type("depends_on", self.resources, depends)
		if len(depends - resources_keys_set) != 0:
			raise AssertionError("%d != 0 %s" % (len(depends - resources_keys_set), depends - resources_keys_set))

	@staticmethod
	def runner(func, verbose):
		if verbose:
			print func.__name__, "..."
		func()
		if verbose:
			print func.__name__, "OK\n"

	def do_all(self):
		for f in [
			self.right_depends,
			self.capable_resources,
			self.capable_outputs,
			self.assert_params_equality,
			self.capable_parameters,
			self.follow_nested_stack
		]:
			self.runner(f, self.verbose)

	def follow_nested_stack(self):
		types = set()
		self._set_used_type("type", self.resources, types)
		self.used_registries = types.intersection()
		for i in self.registries:
			self._deep_inside_nested_stack(i, self.resources)


def fast_arg_parsing():
	args = argparse.ArgumentParser()
	args.add_argument("-f", "--stack_file", type=str, help="stack_file")
	args.add_argument("-P", "--parameter", nargs="*", type=str, help="key=value")
	args.add_argument("-r", "--registry", type=str, help="registry_file")
	args.add_argument("-v", "--verbose", type=bool, default=False, help="verbose")

	return args.parse_args().stack_file, args.parse_args().parameter, args.parse_args().registry, \
		   args.parse_args().verbose


if __name__ == "__main__":
	stack_file, parameters, registry_file_directory, verbose = fast_arg_parsing()
	if verbose:
		print "stack_file %s\n" \
			  "parameters %s\n" \
			  "registry_file_directory %s\n" % (stack_file, parameters, registry_file_directory)

	if stack_file is None:
		raise AttributeError
	integrity = StackIntegrity(
			stack_file_path=stack_file,
			registry_file_path=registry_file_directory,
			parameters=parameters,
			verbose=verbose
	)
	integrity.do_all()
