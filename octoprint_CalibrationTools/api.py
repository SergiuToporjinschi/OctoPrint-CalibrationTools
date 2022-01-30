# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import octoprint.plugin
import flask


CMD_LOAD_STEPS = "loadSteps"
CMD_TEST = "TEST"
CMD_START_EXTRUSION = "startExtrusion"

def someTestFunc(self, temps):
    self._logger.debug("a ajuns %s", temps)


class API(octoprint.plugin.SimpleApiPlugin):
    @staticmethod
    def get_api_commands():
        return {
            CMD_LOAD_STEPS: [],
            CMD_START_EXTRUSION: [],
            CMD_TEST: []
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
        if command == CMD_START_EXTRUSION:
            self._logger.debug("Heating the tools")
            self._printer.commands("M104 S180")
            self.registerEventTemp("T0", 180, self.startExtrusion)

            return
        if command == CMD_TEST:
            self.registerEventTemp("T0", 100, someTestFunc)
            return
