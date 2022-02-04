$(function () {
    function CalibrationToolsPIDTuneViewModel(parameters) {
        var self = this;
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];
        self.controlViewModel = parameters[2];

        self.pidCurrentValues = {
            "hotEnd": {
                "P": ko.observable(0),
                "I": ko.observable(0),
                "D": ko.observable(0)
            },
            "bed": {
                "P": ko.observable(0),
                "I": ko.observable(0),
                "D": ko.observable(0)
            }
        };

        self.isAdmin = ko.observable(false);
        self.pid = {
            "hotEnd": {
                fanSpeed: ko.observable(255),
                noCycles: ko.observable(8),
                hotEndIndex: ko.observable(0),
                targetTemp: ko.observable(200)
            },
            "bed": {
                fanSpeed: ko.observable(255),
                noCycles: ko.observable(8),
                index: ko.observable(-1),
                targetTemp: ko.observable(200)
            }
        };

        /**
         * Get current PIDs settings for bed and hotEnd
         */
        self.getCurrentValues = function () {
            OctoPrint.simpleApiCommand("CalibrationTools", "pid_getCurrentValues").done(function (response) {
                self.pidCurrentValues.hotEnd.P(response.data.hotEnd.P);
                self.pidCurrentValues.hotEnd.I(response.data.hotEnd.I);
                self.pidCurrentValues.hotEnd.D(response.data.hotEnd.D);
                self.pidCurrentValues.bed.P(response.data.bed.P);
                self.pidCurrentValues.bed.I(response.data.bed.I);
                self.pidCurrentValues.bed.D(response.data.bed.D);
            }).fail(function (response) {
                new PNotify({
                    title: "Error on getting current PID values ",
                    text: response.responseJSON.error,
                    type: "error",
                    hide: false
                });
            });
        };

        self.onBeforeBinding = self.onUserLoggedIn = self.onUserLoggedOut = function () {
            self.pid.hotEnd.fanSpeed(self.settingsViewModel.settings.plugins.CalibrationTools.pid.hotEnd.fanSpeed());
            self.pid.hotEnd.hotEndIndex(self.settingsViewModel.settings.plugins.CalibrationTools.pid.hotEnd.hotEndIndex());
            self.pid.hotEnd.noCycles(self.settingsViewModel.settings.plugins.CalibrationTools.pid.hotEnd.noCycles());
            self.pid.hotEnd.targetTemp(self.settingsViewModel.settings.plugins.CalibrationTools.pid.hotEnd.targetTemp());
            self.pid.bed.index(-1);
            self.pid.bed.noCycles(self.settingsViewModel.settings.plugins.CalibrationTools.pid.bed.noCycles());
            self.pid.bed.targetTemp(self.settingsViewModel.settings.plugins.CalibrationTools.pid.bed.targetTemp());
            self.isAdmin(self.loginStateViewModel.isAdmin());
        }

        self.startPidHotEnd = function () {
            OctoPrint.simpleApiCommand("CalibrationTools", "pid_start", {
                "fanSpeed": Number(self.pid.hotEnd.fanSpeed()),
                "noCycles": Number(self.pid.hotEnd.noCycles()),
                "hotEndIndex": Number(self.pid.hotEnd.hotEndIndex()),
                "targetTemp": Number(self.pid.hotEnd.targetTemp())
            }).done(function (response) {
                new PNotify({
                    title: "PID HotEnd tuning has started",
                    text: "In progress",
                    type: "info"
                });
                console.log(response);
            }).fail(function (response) {
                new PNotify({
                    title: "Error on starting PID autotune ",
                    text: response.responseJSON.error,
                    type: "error",
                    hide: false
                });
            });
        }
        self.startPidBed = function () {
            OctoPrint.simpleApiCommand("CalibrationTools", "pid_start", {
                "heater": "bed",
                "fanSpeed": self.pid.bed.fanSpeed(),
                "noCycles": self.pid.bed.noCycles(),
                "hotEndIndex": self.pid.bed.hotEndIndex(),
                "targetTemp": self.pid.bed.targetTemp()
            }).done(function (response) {
                new PNotify({
                    title: "PID HotEnd tuning has started",
                    text: "In progress",
                    type: "info"
                });
                console.log(response);
            }).fail(function (response) {
                new PNotify({
                    title: "Error on starting PID autotune ",
                    text: response.responseJSON.error,
                    type: "error",
                    hide: false
                });
            });
        }
    }
    OCTOPRINT_VIEWMODELS.push({
        // This is the constructor to call for instantiating the plugin
        construct: CalibrationToolsPIDTuneViewModel,
        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        dependencies: ["loginStateViewModel", "settingsViewModel", "controlViewModel", "terminalViewModel", "accessViewModel"],
        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        elements: ["#calibration_pid"]
    });
});