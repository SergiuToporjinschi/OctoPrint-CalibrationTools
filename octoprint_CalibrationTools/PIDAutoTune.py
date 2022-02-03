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

regexPID = "Kp:\s*(?P<P>\d{1,3}.\d{1,3})\s*Ki:\s*(?P<I>\d{1,3}.\d{1,3})\s*Kd:\s*(?P<D>\d{1,3}.\d{1,3})"
regexGetPid = "\s*Kp:\s*(?P<p>\d{1,3}.\d{1,3})\s*Ki:\s*(?P<i>\d{1,3}.\d{1,3})\s*Kd:\s*(?P<d>\d{1,3}.\d{1,3})"
PIDStarted = "PID Autotune start"
PIDStoped = "PID Autotune finished!"
PIDStopedP = "#define DEFAULT_Kp\s*(?P<P>\d{1,3}.\d{1,3})"
PIDStopedI = "#define DEFAULT_Ki\s*(?P<I>\d{1,3}.\d{1,3})"
PIDStopedD = "#define DEFAULT_Kd\s*(?P<D>\d{1,3}.\d{1,3})"
regexFinished = "PID Autotune finished!.*\n#define DEFAULT_Kp\s*(?P<P>\d{1,3}.\d{1,3}).*\n#define DEFAULT_Ki\s*(?P<I>\d{1,3}.\d{1,3})\n#define DEFAULT_Kd\s*(?P<D>\d{1,3}.\d{1,3})"
class API(octoprint.plugin.SimpleApiPlugin):
    pidHotEndCycles = []
    pidCurrentValues = {}
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
            #catch for "echo: p:28.27 i:2.82 d:70.81"  or   "M301 P27.08 I2.51 D73.09"

            getPid = re.compile(r".*p:??(?P<p>\d{1,3}.\d{1,3})\s*i:?(?P<i>\d{1,3}.\d{1,3})\s*d:?(?P<d>\d{1,3}.\d{1,3})", flags=re.IGNORECASE)

            hasResult301 = Event()
            hasResult304 = Event()
            self.registerRegexMsg(getPid, self.m301_m304CodeResponse, hasResult301, "hotEnd")
            self.registerRegexMsg(getPid, self.m301_m304CodeResponse, hasResult304, "bed")

            self._printer.commands(["M301", "M304"])
            hasResult301.wait(5)
            hasResult304.wait(5)

            return flask.jsonify({
                "data": self.pidCurrentValues
            })

        if command == CMD_PID_START:
            self.pidHotEndCycles = []

            #Two cycles are for tuning
            for i in range(0, data['noCycles'] - 2):
                self.registerRegexMsg(regexGetPid, self.m106CodeResponse)

            self._printer.commands(["M106 S%(fanSpeed)s" % data, "M303 C%(noCycles)s E%(hotEndIndex)s S%(targetTemp)s U1" % data])
            self._logger.debug("cycles %s", self.pidHotEndCycles)

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
    def m106CodeResponse(self, line):
        self._logger.debug("m106CodeResponse: %s", line)
        self.pidHotEndCycles.append(line)
