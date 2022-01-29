import re
class Hooks():
 ##~~ Softwareupdate hook
    def calibrateGCodeReceived(self, comm, line, *args, **kwargs):
        if not self.collectCommand: return line
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

    def calibrateGCodeSending(self, comm, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
        self._logger.debug("Sending GCODE [%s]", gcode)
        if cmd == "M92":
            self.collectCommand = True