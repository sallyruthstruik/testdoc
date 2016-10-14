from functools import wraps

__author__ = 'stas'


class Testdoc:

    def __init__(self, configuration):
        """
        :type configuration: testdoc.configurator.BaseConfiguration
        """

        self._configuration = configuration

    def __call__(self, func):

        @wraps(func)
        def inner(*a, **k):

            exception = None
            try:
                output = func(*a, **k)

                return output
            except Exception as exception:
                raise exception
            finally:
                if self._configuration.should_write_doc(func):
                    self._configuration.get_registry().write_docs(
                        func, args=a, kwargs=k, exception=exception, output=output
                    )

        self._configuration.get_doc_writer().write_docs(inner)

        return inner



