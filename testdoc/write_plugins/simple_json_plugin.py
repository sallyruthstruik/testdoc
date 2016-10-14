import json
from testdoc.write_plugins.base_write_plugin import BaseWritePlugin

__author__ = 'stas'


class SimpleJsonPlugin(BaseWritePlugin):


    def serialize_func_info(self, func):
        return {
            "func": func.__module__,
            "args": str(args),
            "kwargs": str(kwargs),
            "exception": str(exception),
            "output": str(output)
        }


    def apply(self, docString, func, data):

        docString = """
{}

{}
""".format(
            docString,
            self.render_with_prefix(
                self.get_prefix_whitepaces(docString),
                json.dumps(data, ensure_ascii=False, indent=4))
        )

        return docString