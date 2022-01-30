# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from ast import arg

import re
import threading
import traceback
import types
import collections


class Hooks():
    trackTemp = True
    events = []
    gCodeWaiters = []

    def gCodeReceived(self, comm, line, *args, **kwargs):
        if len(self.gCodeWaiters) <= 0 and not line.startswith('echo:'):
            return line

        reg = re.compile("echo:\s*(?P<gCode>M\d{1,4})")
        mCommand = reg.match(line)
        if mCommand:
            gCode = mCommand.group("gCode")
            for waiter in self.gCodeWaiters:
                if gCode.upper() == waiter["cmd"]:
                    arg = (line, *waiter["args"])
                    if isinstance(waiter["func"], types.FunctionType):
                        arg = (self, *arg)
                    threading.Thread(target=waiter["func"], args=arg).start()
                    self.gCodeWaiters.remove(waiter)
        return line

    def firmwareInfo(self, comm_instance, firmware_name, firmware_data, *args, **kwargs):
        self.data["info"] = {
            "firmware": firmware_data
        }

    # Hook for temperature messages
    # This is active only when there are events registered to temperature changes
    def processTemp(self, comm_instance, parsed_temperatures, *args, **kwargs):
        if len(self.events) <= 0:
            return parsed_temperatures

        try:
            self.checkAndTriggerEvent(parsed_temperatures.copy())
        except Exception as e:
            self._logger.error(traceback.format_exc())
        return parsed_temperatures

    # Check if the current message contains changes concerning registered tool
    # if the criteria is meat then the execution function is called
    def checkAndTriggerEvent(self, temps):
        for tool, values in temps.items():
            (curTemp, trgTemp) = values
            for event in self.events:
                if event["tool"] == tool and curTemp >= event["targetTemp"]:
                    arg = (temps, *event["args"])
                    if isinstance(event["func"], types.FunctionType):
                        arg = (self, *arg)
                    threading.Thread(target=event["func"], args=arg).start()
                    self.events.remove(event)

    # Registering a temp event
    def registerEventTemp(self, tool, targetTemp, func, *arguments):
        if func is None or not isinstance(func, collections.Callable):
            self._logger.warn("registerEventTemp: Attempt to register event without a function")
            return

        event = {
            "tool": tool,
            "targetTemp": targetTemp,
            "func": func,
            "args": arguments
        }
        self._logger.debug("Registering event [%s, isFunction: %s]", event, isinstance(func, types.FunctionType))
        self.events.append(event)

    # Registering a gCodeWaiter
    def registerGCodeWaiter(self, command, func, *arguments):
        if command is None or not re.compile("(?P<gCode>M\d{1,4})").match(command.upper()) or func is None or not isinstance(func, collections.Callable):
            self._logger.warn("registerGCodeAnswer: Attempt to register gCodeAnswer without a function or gCode command")
            return
        self.gCodeWaiters.append({
            "cmd": command.upper(),
            "func": func,
            "args": arguments
        })
