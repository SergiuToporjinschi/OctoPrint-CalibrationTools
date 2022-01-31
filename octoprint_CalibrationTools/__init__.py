# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import octoprint.plugin

from octoprint_CalibrationTools import api, hooks, models

defaultSettings = {
    "eSteps": {
        "userControlsTemp": "checked",
        "turnOffHotend": "",
        "extrudeTemp": 210,
        "extrudeLength": 100,
        "extrudeSpeed": 50,
        "markLength": 120
    }
}

class CalibrationtoolsPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    api.API,
    hooks.Hooks,
    models.CalibrationModel
):
    collectCommand = False
    data = {}


    def initialize(self):
        self.collectCommand = False

    def on_after_startup(self):
        self._logger.debug("---------------[ CalibrationTools ]---------------")
        self.data = self.getModel()
        self.collectCommand = True
        self._printer.commands("M92")

    # ~~ AssetPlugin mixin
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/CalibrationTools.js"],
            "css": ["css/style.css"]
        }
    # self._settings.valid_boolean_trues:

    def get_settings_defaults(self):
        return defaultSettings

    def get_template_configs(self):
        return [
            {
                "type": "tab",
                "name": "Calibration Tools",
                "template": "CalibrationTools_tab.jinja2",
                "custom_bindings": True,
            },
            {
                "type": "settings",
                "name": "Calibration settings",
                "template": "CalibrationTools_settings.jinja2",
                "custom_bindings": False,
            },
        ]

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
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = CalibrationtoolsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.firmware.info": __plugin_implementation__.firmwareInfo,
        "octoprint.comm.protocol.gcode.received": __plugin_implementation__.gCodeReceived,
        "octoprint.comm.protocol.temperatures.received": __plugin_implementation__.processTemp
    }
