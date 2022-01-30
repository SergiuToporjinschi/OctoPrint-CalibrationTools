# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import octoprint.plugin
import flask

CMD_LOAD_STEPS = "loadSteps"


def someTestFunc(self, temps, a, b):
    self._logger.debug("a ajuns %s, %s, %s", temps, a,b)


class API(octoprint.plugin.SimpleApiPlugin):
    @staticmethod
    def get_api_commands():
        return {
            CMD_LOAD_STEPS: [],
            "TEST": []
        }

    def on_api_get(self, request):
        self._logger.debug("api.on_api_get")
        return flask.jsonify(
            {
                "data": self.data["steps"]
            }
        )

    def on_api_command(self, command, data):
        self._logger.debug("api command [%s] received", command)
        if command == CMD_LOAD_STEPS:
            self._printer.commands("M92")
            return flask.jsonify({
                "data": self.data["steps"]
            })
        if command == "TEST":
            self.registerEventTemp("T0", 100, someTestFunc, 1,"test")
            return
