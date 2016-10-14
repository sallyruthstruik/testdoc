from testdoc.write_plugins.base_write_plugin import BaseWritePlugin

__author__ = 'stas'

class DocsWriter:

    def __init__(self, configuration):
        """
        :type configuration: testdoc.configurator.BaseConfiguration
        """
        self.configuration = configuration

        self.write_plugins = [] #type: list[BaseWritePlugin]


    def write_docs(self, func):
        registry = self.configuration.get_registry()

        docString = func.__doc__
        for plugin in self.write_plugins:
            data = registry.get_info_about(func, plugin)

            if data:
                docString = plugin.apply(docString, func, data)

        func.__doc__ = docString

    def add_plugin(self, plugin):
        """
        :type plugin: BaseWritePlugin
        """

        self.write_plugins.append(plugin)