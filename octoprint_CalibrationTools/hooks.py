# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import re
import threading
import traceback
import types


class Hooks():
    trackTemp = True
    events = []
    gCodeWaiters = []

    def gCodeReceived(self, comm, line, *args, **kwargs):
        try:
            if len(self.gCodeWaiters) <= 0:
                return line
            for waiter in self.gCodeWaiters:
                reg = waiter["regex"]
                waiter["callCount"] = waiter["callCount"] + 1
                if reg.match(line):
                    args = (line, reg, *waiter["args"])
                    if isinstance(waiter["func"], types.FunctionType):
                        args = (self, *args)
                    threading.Thread(target=waiter["func"], args=args).start()
                    waiter["dead"] = True
                    break
                # if waiter["callCount"] >= 3:
                #     self._logger.warning("Hanging thread: Removing waiter regex: %(regex)s" % waiter)
                #     waiter["dead"] = True
            self.gCodeWaiters = [w for w in self.gCodeWaiters if "dead" not in w or not w["dead"]]
        except Exception as e:
            self._logger.error(traceback.format_exc())
            self.gCodeWaiters = []
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

    # Check if the current message contains changes concerning registered extruder
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
    # Trigger a function when the temparature
    def registerEventTemp(self, tool, targetTemp, func, *arguments):
        if func is None or not isinstance(func, collections.abc.Callable):
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
        reg = re.compile(".*\s*(?P<gCode>[M,G]\d{1,4})")
        if command is None or not reg.match(command.upper()):
            self._logger.warn("registerGCodeAnswer: Attempt to register gCodeAnswer without a function or valid gCode command")
            return
        self.registerRegexMsg(reg, func, *arguments)

    def registerRegexMsg(self, regex, func, *arguments):
        if regex is None or func is None or not isinstance(func, collections.abc.Callable):
            self._logger.warn("registerRegexMsg: Attempt to register gCodeAnswer without a function or regex")
            return

        self.gCodeWaiters.append({
            "regex": regex,
            "func": func,
            "args": arguments,
            "callCount": 0
        })
