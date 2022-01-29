# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.


import octoprint.plugin
import re
from octoprint_CalibrationTools import (
    api
)

class CalibrationtoolsPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.SimpleApiPlugin
):
    collectCommand = False
    m92Data = {
        "X": 0,
        "Y": 0,
        "Z": 0,
        "E": 0
    }

    def initialize(self):
        self.collectCommand = False
        self._api = api.API(self)

    def on_after_startup(self):
        self._logger.debug("----------------[CalibrationTools]----------------")
        self.collectCommand = True
        self._printer.commands("M92")

    # API handling
    def get_api_commands(self):
        return self._api.get_api_commands()

    def on_api_command(self, command, data):
        return self._api.on_api_command(command, data)

    def on_api_get(self, request):
        return self._api.on_api_get(request)

    ##~~ AssetPlugin mixin
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/CalibrationTools.js"],
            "css": ["css/style.css"]
        }


    ##~~ Softwareupdate hook
    def comm_protocol_gcode_received(self, comm, line, *args, **kwargs):
        if not self.collectCommand: return line

        reg = re.compile("echo:\s*(?P<command>(?P<gCode>M\d{1,3}) X(?P<xVal>\d{1,3}.\d{1,3}) Y(?P<yVal>\d{1,3}.\d{1,3}) Z(?P<zVal>\d{1,3}.\d{1,3}) E(?P<eVal>\d{1,3}.\d{1,3}))")
        isM92command = reg.match(line)
        if isM92command:
            command = isM92command.group("command")
            if isM92command.group("gCode") == "M92":
                xValue = isM92command.group("xVal")
                yValue = isM92command.group("yVal")
                zValue = isM92command.group("zVal")
                eValue = isM92command.group("eVal")

                self.m92Data["X"] = float(xValue)
                self.m92Data["Y"] = float(yValue)
                self.m92Data["Z"] = float(zValue)
                self.m92Data["E"] = float(eValue)

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

    def comm_protocol_gcode_sending(self, comm, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
        self._logger.debug("sending GCODE")
        if cmd == "M92":
            self._logger.debug("{} detected, collecting data".format(cmd))
            self.collectCommand = True

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "CalibrationTools": {
                "displayName": "Calibration Tools",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "SergiuToporjinschi",
                "repo": "OctoPrint-CalibrationTools",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/SergiuToporjinschi/OctoPrint-CalibrationTools/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Calibration Tools"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = CalibrationtoolsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.received": __plugin_implementation__.comm_protocol_gcode_received,
        "octoprint.comm.protocol.gcode.sending": __plugin_implementation__.comm_protocol_gcode_sending
        # "octoprint.comm.protocol.atcommand.sending": __plugin_implementation__.comm_protocol_atcommand_sending
    }
