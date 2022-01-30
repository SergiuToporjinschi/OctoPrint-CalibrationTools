# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from ast import arg

import re
import threading
import traceback

class Hooks():
    trackTemp = True
    events = []

    def gCodeReceived(self, comm, line, *args, **kwargs):
        if not self.collectCommand:
            return line
        self._logger.debug("collectCommand is true, collecting info")

        reg = re.compile("echo:\s*(?P<command>(?P<gCode>M\d{1,3}) X(?P<xVal>\d{1,3}.\d{1,3}) Y(?P<yVal>\d{1,3}.\d{1,3}) Z(?P<zVal>\d{1,3}.\d{1,3}) E(?P<eVal>\d{1,3}.\d{1,3}))")
        isM92command = reg.match(line)
        if isM92command:
            command = isM92command.group("command")
            if isM92command.group("gCode") == "M92":
                xValue = isM92command.group("xVal")
                yValue = isM92command.group("yVal")
                zValue = isM92command.group("zVal")
                eValue = isM92command.group("eVal")
                self.data["steps"]["X"] = float(xValue)
                self.data["steps"]["Y"] = float(yValue)
                self.data["steps"]["Z"] = float(zValue)
                self.data["steps"]["E"] = float(eValue)

                # Send the new data to the UI to be reloaded
                self._logger.debug(line)
                self._logger.debug("gCode: %s", command)
                self._logger.debug("X: %s", xValue)
                self._logger.debug("Y: %s", yValue)
                self._logger.debug("Z: %s", zValue)
                self._logger.debug("E: %s", eValue)
                self._logger.debug("Finished data collection")
                self.collectCommand = False
        return line

    def gCodeSending(self, comm, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
        self._logger.debug("Sending GCODE [%s]", gcode)
        if cmd == "M92":
            self.collectCommand = True

    def firmwareInfo(self, comm_instance, firmware_name, firmware_data, *args, **kwargs):
        self.data["info"] = {
            "firmware": firmware_data
        }

    ## Hook for temperature messages
    ## This is active only when there are events registered to temperature changes
    def processTemp(self, comm_instance, parsed_temperatures, *args, **kwargs):
        if len(self.events) <= 0: return parsed_temperatures
        try:
            self.checkAndTriggerEvent(parsed_temperatures.copy())
        except Exception as e:
            self._logger.error(traceback.format_exc())
        return parsed_temperatures

    ## Check if the current message contains changes concerning registered tool
    ## if the criteria is meat then the execution function is called
    def checkAndTriggerEvent(self, temps):
        for tool, values in temps.items():
            (curTemp, trgTemp) = values
            for event in self.events:
                if event["tool"] == tool and curTemp >= event["targetTemp"]:
                    threading.Thread(target=event["func"], args=(self, temps, *event["args"])).start()
                    self.events.remove(event)

    ## Registering a temp event
    def registerEventTemp(self, tool, targetTemp, func, *arguments):
        if func is None:
            self._logger.warn("registerEventTemp: Attempt to register event without a function")
            return

        event = {
            "tool": tool,
            "targetTemp": targetTemp,
            "func": func,
            "args": arguments
        }
        self._logger.debug("Registering event [%s]", event)
        self.events.append(event)
