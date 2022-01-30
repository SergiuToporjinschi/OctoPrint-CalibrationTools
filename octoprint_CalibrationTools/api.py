# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import octoprint.plugin
import flask


CMD_TEST = "TEST"
CMD_LOAD_STEPS = "loadSteps"
CMD_START_EXTRUSION = "startExtrusion"
CMD_SAVE_E_STEPS = "saveESteps"


def someTestFunc(self, temps):
    self._logger.debug("a ajuns %s", temps)


class API(octoprint.plugin.SimpleApiPlugin):
    @staticmethod
    def get_api_commands():
        return {
            CMD_LOAD_STEPS: [],
            CMD_START_EXTRUSION: [],
            CMD_SAVE_E_STEPS: [],
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
        self._logger.debug("api command [%s] received payload [%s]", command, data)
        if command == CMD_LOAD_STEPS:
            self._logger.debug("Load steps from EEPROM")
            if not self._printer.is_ready():
                self._logger.warning("Printer not ready, operation canceled")
                return flask.abort(503, {
                    "msg": "Printer not ready, operation canceled"
                })

            self._printer.commands("M92")

            return flask.jsonify({
                "data": self.data["steps"]
            })

        if command == CMD_START_EXTRUSION:
            self._logger.debug("Heating the tools")
            if not self._printer.is_ready():
                self._logger.warning("Printer not ready, operation canceled")
                return flask.abort(503, {
                    "msg": "Printer not ready, operation canceled"
                })

            # Register event to be trigger when temp is achieved
            self.registerEventTemp("T0", 180, self.startExtrusion)

            # Heating the tool
            self._printer.commands("M104 S180")
            return

        if command == CMD_SAVE_E_STEPS:
            self._printer.commands(["M92 E%(newESteps)s" % data, "M500"])
            return

        if command == CMD_TEST:
            # self.registerEventTemp("T0", 100, someTestFunc)
            return flask.abort(503, {
                "msg": "Printer not ready, operation canceled"
            })

    @staticmethod
    def startExtrusion(self, temps, *args):
        self._logger.debug("Temperature achieved, extrusion started %s, %s", temps, args)

        # Extrude
        self._printer.extrude(amount=120, speed=50)
