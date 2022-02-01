# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re
from threading import Event

import flask
import octoprint.plugin

# from octoprint_CalibrationTools import EStepsApi

CMD_TEST = "TEST"
CMD_LOAD_STEPS = "loadSteps"
CMD_START_EXTRUSION = "startExtrusion"
CMD_SAVE_E_STEPS = "saveESteps"

class API(octoprint.plugin.SimpleApiPlugin):
    def __init__(self) -> None:
        super().__init__()
        # self.espAPI = EStepsApi.API()

    @staticmethod
    def get_api_commands():
        # x = EStepsApi.apiCommands()
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
        self.espAPI.apiGateWay()

        if command == CMD_LOAD_STEPS:
            self._logger.debug("Load steps from EEPROM")
            if not self._printer.is_ready():
                self._logger.warning("Printer not ready, operation canceled")
                return flask.abort(503, {
                    "msg": "Printer not ready, operation canceled"
                })

            # Register listener waiting response for M92 command
            m92Event = Event()
            self.registerGCodeWaiter("M92", self.m92GCodeResponse, m92Event)

            # Issue M92 command
            self._printer.commands("M92")

            m92Event.wait()
            return flask.jsonify({
                "data": self.data["steps"]
            })

        if command == CMD_START_EXTRUSION:
            self._logger.debug("Heating the extruder [%s]", data)
            if not self._printer.is_ready():
                self._logger.warning("Printer not ready, operation canceled")
                return flask.abort(503, {
                    "msg": "Printer not ready, operation canceled"
                })

            # Register event to be trigger when temp is achieved
            self.registerEventTemp("T0", int(data["extrudeTemp"]), self.startExtrusion, data["extrudeLength"], data["extrudeSpeed"])

            # Heating the tool
            self._printer.commands("M104 S%(extrudeTemp)s" % data)
            return

        if command == CMD_SAVE_E_STEPS:
            eStepsSettings = self._settings.get(['eSteps'])
            userControlsTemp = eStepsSettings.get("userControlsTemp")
            turnOffHotend = eStepsSettings.get("turnOffHotend")
            self._printer.commands(["M92 E%(newESteps)s" % data, "M500"] + ["M104 S0"] if turnOffHotend and not userControlsTemp else  [])
            return

        if command == CMD_TEST:
            self.registerGCodeWaiter("M92", self.someTestFunc)
            return

############## HANDLERS ##############
    @staticmethod
    def startExtrusion(self, temps, extrudeLength, extrudeSpeed, *args):
        self._logger.debug("Temperature achieved, extrusion started [temps:%s, extrudeLength:%s, extrudeSpeed:%s, args:%s]",
        temps, extrudeLength, extrudeSpeed, args)

        # Extrude
        self._printer.extrude(amount=int(extrudeLength), speed=int(extrudeSpeed))

    @staticmethod
    def m92GCodeResponse(self, line, event):
        reg = re.compile("echo:\s*(?P<command>(?P<gCode>M\d{1,3}) X(?P<xVal>\d{1,3}.\d{1,3}) Y(?P<yVal>\d{1,3}.\d{1,3}) Z(?P<zVal>\d{1,3}.\d{1,3}) E(?P<eVal>\d{1,3}.\d{1,3}))")
        isM92command = reg.match(line)
        if isM92command:
            command = isM92command.group("command")
            if isM92command.group("gCode") == "M92":
                self.data["steps"]["X"] = float(isM92command.group("xVal"))
                self.data["steps"]["Y"] = float(isM92command.group("yVal"))
                self.data["steps"]["Z"] = float(isM92command.group("zVal"))
                self.data["steps"]["E"] = float(isM92command.group("eVal"))

                # Send the new data to the UI to be reloaded
                self._logger.debug("gCode: %s", command)
                self._logger.debug("X: %s, Y:%s, Z:%s, E:%s", self.data["steps"]["X"], self.data["steps"]["Y"], self.data["steps"]["Z"], self.data["steps"]["E"])
                self._logger.debug("Finished data collection")
                self.collectCommand = False
        if event:
            event.set()
