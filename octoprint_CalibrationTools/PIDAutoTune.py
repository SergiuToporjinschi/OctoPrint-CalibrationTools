# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re
from threading import Event

import flask
import octoprint.plugin

CMD_PID_SAVE = "pid_save"
CMD_PID_START = "pid_start"

regexPID = "Kp:\s*(?P<P>\d{1,3}.\d{1,3})\s*Ki:\s*(?P<I>\d{1,3}.\d{1,3})\s*Kd:\s*(?P<D>\d{1,3}.\d{1,3})"
regexGetPid = "\s*Kp:\s*(?P<p>\d{1,3}.\d{1,3})\s*Ki:\s*(?P<i>\d{1,3}.\d{1,3})\s*Kd:\s*(?P<d>\d{1,3}.\d{1,3})"
PIDStarted = "PID Autotune start"
PIDStoped = "PID Autotune finished!"
PIDStopedP = "#define DEFAULT_Kp\s*(?P<P>\d{1,3}.\d{1,3})"
PIDStopedI = "#define DEFAULT_Ki\s*(?P<I>\d{1,3}.\d{1,3})"
PIDStopedD = "#define DEFAULT_Kd\s*(?P<D>\d{1,3}.\d{1,3})"
regexFinished = "PID Autotune finished!.*\n#define DEFAULT_Kp\s*(?P<P>\d{1,3}.\d{1,3}).*\n#define DEFAULT_Ki\s*(?P<I>\d{1,3}.\d{1,3})\n#define DEFAULT_Kd\s*(?P<D>\d{1,3}.\d{1,3})"
class API(octoprint.plugin.SimpleApiPlugin):

    @staticmethod
    def apiCommands():
        return {
            CMD_PID_SAVE : [],
            CMD_PID_START: ["fanSpeed", "noCycles", "hotEndIndex", "targetTemp"]
            }

    def apiGateWay(self, command, data):
        self._logger.debug("DIPGateway")
        if command == CMD_PID_START:
            self.pidCycles = []

            for i in range(0,data['noCycles']):
                self.registerRegexMsg(regexGetPid, self.m106CodeResponse)

            self._printer.commands(["M106 S%(fanSpeed)s" % data, "M303 C%(noCycles)s E%(hotEndIndex)s S%(targetTemp)s U1" % data])
            self._logger.debug("cycles %s", self.pidCycles)

        if command == CMD_PID_SAVE:
            self._logger.debug("DIPSave-")
            return flask.jsonify({
                "data": self.pidCycles
            })

    @staticmethod
    def m106CodeResponse(self, line):
        self._logger.debug("m106CodeResponse: %s", line)
        # isM106Response = re.compile(regexFinished).match(line)
        # if isM106Response:
        #     p = isM106Response.group("P")
        #     i = isM106Response.group("I")
        #     d = isM106Response.group("D")
        #     self._logger.debug("P:%s, I:%s, d:%d", p, i, d)
        # self._logger.debug("line: %s", line)
        self.pidCycles.append(line)
        self._logger.debug("cycles %s", self.pidCycles)
