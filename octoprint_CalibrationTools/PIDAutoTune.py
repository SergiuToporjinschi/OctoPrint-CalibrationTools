# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re
from threading import Event

import flask
import octoprint.plugin

CMD_PID_SAVE = "pid_save"

class API(octoprint.plugin.SimpleApiPlugin):

    @staticmethod
    def apiCommands():
        return {CMD_PID_SAVE : []}

    def apiGateWay(self, command, data):
        self._logger.debug("DIPGateway")
        if command == CMD_PID_SAVE:
            self._logger.debug("DIPSave-")

