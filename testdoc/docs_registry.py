import json
from testdoc.utils import Utils
from testdoc.write_plugins.base_write_plugin import BaseWritePlugin

__author__ = 'stas'

class DocsRegistry:
    """
    Simple docs regisry. Uses json and local file as storage
    """
    def __init__(self, configuration,
                 filepath=".docs_registry.json"):
        """
        :type configuration: testdoc.configurator.BaseConfiguration
        """
        self.configuration = configuration


        self.filepath = filepath
        self.registry = self.read()

        self.plugins = []   #type: list[BaseWritePlugin]

    def read(self):
        try:
            with open(self.filepath, "r") as fd:
                return json.loads(fd.read())
        except Exception:
            return {}

    def flush(self):
        with open(self.filepath, "w") as fd:
            fd.write(json.dumps(self.registry, ensure_ascii=False, indent=4))

    def write_docs(self, func, args, kwargs, exception, output):
        """

        Perform writing one doc example for function func
        based on it args, kwargs, output and produced exception

        data stores in next format::

            {
                PluginName: {
                    funcKey: {
                        "funcInfo": <result of plugin.serialize_func_info>
                        "callsInfo": <result of plugin.extract_calls_info>
                        "calls": [
                            ...<result of plugin.serialize_call_info>
                        ]
                    }
                }
            }

        :type args: tuple
        :type kwargs: dict
        :type exception: Exception

        """

        funcKey = self._get_func_key(func)

        for plugin in self.plugins:     #type: BaseWritePlugin
            self.registry.setdefault(plugin.__class__.__name__, {
                funcKey: {
                    "funcInfo": plugin.serialize_func_info(func),
                    "calls": [],
                    "callsInfo": {}
                }
            })

            funcKeyObj = self.registry[plugin.__class__.__name__][funcKey]


            oneCallInfo = plugin.serialize_call_info(
                func, args, kwargs, exception, output
            )

            if oneCallInfo not in funcKeyObj["calls"]:
                funcKeyObj["calls"].append(oneCallInfo)
                funcKeyObj["callsInfo"] = plugin.extract_calls_info(
                    func, funcKeyObj["calls"]
                )

        self.flush()

    def get_info_about(self, func, plugin):
        """
        Returns array of object representing func call

        :rtype: list
        """
        try:
            return self.registry[plugin.__class__.__name__][self._get_func_key(func)]
        except KeyError:
            pass

    @Utils.tolist
    def get_plugin_data(self, plugin):
        """
        Returns list of objects:

        {
            "key": funcKey,
            "funcInfo": funcInfo,
            "callsInfo": callsInfo
        }

        from registry
        """

        for key, data in self.registry.get(plugin.__class__.__name__).items():
            yield dict(
                key=key,
                funcInfo=data["funcInfo"],
                callsInfo=data["callsInfo"]
            )


    def add_plugin(self, plugin):
        """
        :type plugin: BaseWritePlugin
        """

        self.plugins.append(plugin)

    def _get_func_key(self, func):
        return Utils.funcKey(func)

