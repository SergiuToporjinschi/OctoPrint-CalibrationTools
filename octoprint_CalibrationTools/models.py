# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class CalibrationModel():
    def getModel(self):
        self._logger.debug("getModel")
        steps = self.getSteps()
        temps = self.getTemps()
        return {
            "steps": steps,
            "temps": temps
        }

    def getSteps(self):
        self._logger.debug("getSteps")
        return {
            "X": 0,
            "Y": 0,
            "Z": 0,
            "E": 0
        }

    def getTemps(self):
        return {'B': (), 'T0': ()}

