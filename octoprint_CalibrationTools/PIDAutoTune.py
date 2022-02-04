# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re
from threading import Event

import flask
import octoprint.plugin

CMD_PID_SAVE = "pid_save"
CMD_PID_START = "pid_start"
CMD_PID_LOAD_CURRENT_VALUES = "pid_getCurrentValues"
CMD_PID_GET_VALUES = "pid_getValues"

#this regex matches:
# !!DEBUG:send echo: Kp: 30.56 Ki: 3.03 Kd: 77.16
# !!DEBUG:send Kp: 30.56 Ki: 3.03 Kd: 77.16
# !!DEBUG:send echo: p:18.84 i:1.18 d:201.41
# !!DEBUG:send p:18.84 i:1.18 d:201.41
# !!DEBUG:send echo: M304 P131.06 I11.79 D971.23
# !!DEBUG:send M304 P131.06 I11.79 D971.23
allPIDsFormats = r".*p:{0,1}\s{0,1}?(?P<p>\d{1,3}.\d{1,3})\sk*i:{0,1}\s{0,1}?(?P<i>\d{1,3}.\d{1,3})\sk*d:{0,1}\s{0,1}?(?P<d>\d{1,3}.\d{1,3})"

class API(octoprint.plugin.SimpleApiPlugin):
    pidHotEndCycles = []
    pidCurrentValues = {}
    #catch for "echo: p:28.27 i:2.82 d:70.81"  or   "M301 P27.08 I2.51 D73.09"
    getPid = re.compile(allPIDsFormats, flags=re.IGNORECASE)
    @staticmethod
    def apiCommands():
        return {
            CMD_PID_LOAD_CURRENT_VALUES: [],
            CMD_PID_SAVE : [],
            CMD_PID_GET_VALUES: [],
            CMD_PID_START: ["fanSpeed", "noCycles", "hotEndIndex", "targetTemp"]
            }

    def apiGateWay(self, command, data):
        self._logger.debug("DIPGateway")
        if command == CMD_PID_LOAD_CURRENT_VALUES:
            hasResult301 = Event()
            hasResult304 = Event()
            self.registerRegexMsg(self.getPid, self.m301_m304CodeResponse, hasResult301, "hotEnd")
            self.registerRegexMsg(self.getPid, self.m301_m304CodeResponse, hasResult304, "bed")

            self._printer.commands(["M301", "M304"])
            hasResult301.wait(5)
            hasResult304.wait(5)

            return flask.jsonify({
                "data": self.pidCurrentValues
            })

        if command == CMD_PID_START:
            self.pidHotEndCycles = {
                "hotEnd": [],
                "bed":[]
            }
            #Two cycles are for tuning
            for i in range(0, data['noCycles'] - 2):
                #response type !!DEBUG:send Kp: 30.56 Ki: 3.03 Kd: 77.16
                self.registerRegexMsg(self.getPid, self.m106CodeResponse, data["heater"])

            self._printer.commands(["M106 S%(fanSpeed)s" % data, "M303 C%(noCycles)s E%(hotEndIndex)s S%(targetTemp)s U1" % data])

        if command == CMD_PID_SAVE:
            self._logger.debug("DIPSave-")
            return flask.jsonify({
                "data": self.pidCycles
            })
        if command == CMD_PID_GET_VALUES:
            self._logger.debug("pid_getValues-")
            return flask.jsonify({
                "data": self.pidCycles
            })

    @staticmethod
    def m301_m304CodeResponse(self, line, regex, event, storingKey):
        self._logger.debug("m301_m304CodeResponse: %s", line)
        match = regex.match(line)
        if match:
            self.pidCurrentValues[storingKey] = {
                "P": match.group("p"),
                "I": match.group("i"),
                "D": match.group("d")
            }
            if event:
                event.set()

    @staticmethod
    def m106CodeResponse(self, line, regex, storingKey):
        self._logger.debug("m106CodeResponse: %s", line)
        match = regex.match(line)
        if match:
            self.pidHotEndCycles[storingKey].append({
                "P": match.group("p"),
                "I": match.group("i"),
                "D": match.group("d")
            })
        self._logger.debug("cycles %s", self.pidHotEndCycles)
