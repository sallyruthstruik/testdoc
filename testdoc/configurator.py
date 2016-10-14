from testdoc.docs_registry import DocsRegistry
from testdoc.docs_writer import DocsWriter

__author__ = 'stas'

class BaseConfiguration:

    def __init__(self, write_plugins):
        """
        :type write_plugins: list[testdoc.write_plugins.base_write_plugin.BaseWritePlugin]
        """
        self.docsRegistry = DocsRegistry(self)
        self.docsWriter = DocsWriter(self)

        self.plugins = write_plugins

        for plugin in write_plugins:
            plugin.configuration = self

            plugin.bootstrap()

            self.docsWriter.add_plugin(plugin)
            self.docsRegistry.add_plugin(plugin)


    def should_write_doc(self, func):
        """
        Should return boolean which indicates when docs should be writed for func.
        For example, it cat return ('test' in sys.argv) if you want write docs only when tests are proceed

        :rtype: bool
        """
        return True

    def get_registry(self):
        """
        Should return instance of DocsRegistry

        :rtype: testdoc.docs_registry.DocsRegistry
        """

        return self.docsRegistry

    def get_doc_writer(self):
        """
        Should return instance of DocsWriter

        :rtype: testdoc.docs_writer.DocsWriter
        """

        return self.docsWriter
