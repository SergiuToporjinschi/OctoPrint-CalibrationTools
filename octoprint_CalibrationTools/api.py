# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import traceback
from ast import Try

import flask

from octoprint_CalibrationTools import EStepsApi, PIDAutoTune


class API(EStepsApi.API, PIDAutoTune.API):

    commandsRegistration = {}

    @staticmethod
    def get_api_commands():
        API.commandsRegistration = {
            "eSteps" : {"cls" : EStepsApi.API},
            "PIDAutoTune": {"cls" : PIDAutoTune.API}
        }

        result = {}
        for key, api in API.commandsRegistration.items():
            API.commandsRegistration[key].update({"commands": api["cls"].apiCommands()})
            result.update( API.commandsRegistration[key]["commands"])
        return result

    def on_api_get(self, request):
        # request.args.get('x')
        self._logger.debug("api.on_api_get")
        return flask.jsonify(
            {
                "data": self.data["steps"]
            }
        )

    def on_api_command(self, command, data):
        try:
            self._logger.debug("API command [%s] received payload [%s]", command, data)
            for key, api in self.commandsRegistration.items():
                if command in api["commands"]:
                    return api["cls"].apiGateWay(self, command, data)
        except Exception as e:
            self._logger.error(traceback.format_exc())
            return flask.abort(500, {
                "msg": "An error curred"
            })
