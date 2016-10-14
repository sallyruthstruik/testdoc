import re
from testdoc.doc_info import DocInfo

__author__ = 'stas'

class BaseWritePlugin:

    configuration = None    #type: testdoc.configurator.BaseConfiguration


    def get_prefix_whitepaces(self, docString):
        """
        returns prefix whitespaces or tabs for docString
        """

        prefixes = []

        for line in docString.split("\n"):
            if not line:
                continue

            try:
                prefix = re.findall(r"^\s+", line)[0]
            except (KeyError, IndexError):
                prefix = ""

            prefixes.append(prefix)

        return min(prefixes, key=len)

    def render_with_prefix(self, prefix, s):

        return "\n".join([
            prefix + line
            for line in s.split("\n")
        ])

    def bootstrap(self):
        """
        Should perform plugin bootstraping.
        By default does nothing
        """

    def apply(self, docString, func, data):
        """
        Should return updated docstring base on docInfo

        :type docString: str
        :type data: list
        :param data: List of items produced by serialize_info function

        :rtype: str
        """

        raise NotImplementedError()


    def serialize_func_info(self, func):
        """
        Should return serialized object for registry info
        """
        raise NotImplementedError()

    def serialize_call_info(self, func, args, kwargs, exception, output):
        """
        Should return serialized object for one func call
        """
        return {}

    def extract_calls_info(self, func, calls):
        """
        Should perform callsInfo object base on it calls

        :type calls: list[dict]
        """
        return {}




