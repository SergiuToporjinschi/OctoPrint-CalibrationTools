# OctoPrint-CalibrationTools

**TODO:** Describe what your plugin does.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/SergiuToporjinschi/OctoPrint-CalibrationTools/archive/master.zip

**TODO:** Describe how to install your plugin, if more needs to be done than just installing it via pip or through
the plugin manager.

## Configuration

**TODO:** Describe your plugin's configuration options (if any).






## Regex for getting temperatures
\s*T:(?P<toolTemp>\d{1,3}.\d{1,3}).*B:(?P<betTemp>\d{1,3}.\d{1,3}).*

## extrude command from JS
OctoPrint.printer.issueToolCommand("extrude", {"amount":100, "speed":50})


## Notification JS
new PNotify({
    title: "Success",
    text: _.sprintf(text, {
        command: _.escape(commandSpec.name)
    }),
    type: "success"
});