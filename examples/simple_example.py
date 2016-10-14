
from testdoc import Testdoc
from testdoc.configurator import BaseConfiguration
from testdoc.write_plugins.simple_json_plugin import SimpleJsonPlugin

__author__ = 'stas'

class Configuration(BaseConfiguration):
    pass

testdoc = Testdoc(Configuration(
    write_plugins=[SimpleJsonPlugin()]
))

@testdoc
def square(input):
    """
    Simple function which returns square of input argument
    """

    return input**2

square(2)
square(4)

print(square.__doc__)
"""
In second run will return::

    Simple function which returns square of input argument


    [
        {
            "func": "__main__",
            "output": "4",
            "exception": "None",
            "args": "(2,)",
            "kwargs": "{}"
        },
        {
            "func": "__main__",
            "output": "16",
            "exception": "None",
            "args": "(4,)",
            "kwargs": "{}"
        }
    ]
"""