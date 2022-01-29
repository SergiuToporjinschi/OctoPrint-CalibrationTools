# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import flask
CMD_LOAD_STEPS_EEPROM = "loadSteps"


class API:
    def __init__(self, plugin):
        self._settings = plugin._settings  # noqa
        self._logger = plugin._logger  # noqa
        self._printer = plugin._printer  # noqa
        self.m92Data = plugin.m92Data  # noqa
        self._plugin = plugin

    @staticmethod
    def get_api_commands():
        return {
            CMD_LOAD_STEPS_EEPROM: []
        }

    def on_api_get(self, request):
        self._logger.info("on api get")
        return flask.jsonify(
            {
                "data": self.m92Data
            }
        )

    def on_api_command(self, command, data):
        if command == CMD_LOAD_STEPS_EEPROM:
            self._logger.info("CMD_LOAD_STEPS_EEPROM")
            self._printer.commands("M92")
            return flask.jsonify({
                "data": self.m92Data
            })
