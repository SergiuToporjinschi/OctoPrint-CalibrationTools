class CalibrationModel():
    def getModel(self):
        self._logger.debug("getModel")
        steps = self.getSteps()
        return {
            "steps": steps
        }

    def getSteps(self):
        self._logger.debug("getSteps")
        return {
            "X": 0,
            "Y": 0,
            "Z": 0,
            "E": 0
        }
