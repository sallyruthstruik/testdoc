from flask.app import Flask
from flask.globals import request
from jinja2.environment import Template
from werkzeug.routing import Rule
from testdoc.utils import Utils
from testdoc.write_plugins.base_write_plugin import BaseWritePlugin

__author__ = 'stas'

class FlaskPlugin(BaseWritePlugin):

    def __init__(self, app):
        self.app = app  #type: Flask


    def apply(self, docString, func, data):
        return docString

#         prefix = self.get_prefix_whitepaces(docString)
#
#         out = """
# {desc}
# {fname}
#         """.format(
#             desc=self.render_with_prefix(
#                 prefix, docString.strip("\t ")
#             ),
#             fname=self.render_with_prefix(
#                 prefix, data[0]["func"]["name"]
#             )
#         )


    def serialize_func_info(self, func):

        return {
            "name": func.__name__,
            "rules": self._get_rules(func)
        }

    def _get_rules(self, func):

        out = []
        for rule in self.app.url_map.iter_rules():
            assert isinstance(rule, Rule)

            if Utils.funcKey(
                    self.app.view_functions[rule.endpoint]
            ) == Utils.funcKey(func):

                out.append({
                    "endpoint": rule.endpoint,
                    "methods": sorted(rule.methods),
                    "url": rule.rule
                })

        return out

    def html(self):
        """
        Renders HTML with detail info about decorated functions

        :rtype: str
        """

        t = Template("""
        {% for item in data %}
            <h1>{{item.funcInfo.name}}</h1>
            Rules:
            {% for rule in item.funcInfo.rules %}
                <ul>
                    <li>Endpoint: {{rule.endpoint}}</li>
                    <li>Methods: {{rule.methods}}</li>
                    <li>Url: <a href="{{rule.url}}">{{rule.url}}</a>
                </ul>
            {% endfor %}
        {% endfor %}
        """)
        print(self.configuration.get_registry().get_plugin_data(self))
        return t.render(
            data=self.configuration.get_registry().get_plugin_data(self)
        )


