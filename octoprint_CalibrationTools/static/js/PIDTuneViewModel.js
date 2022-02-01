$(function () {
    function CalibrationToolsPIDTuneViewModel(parameters) {
        var self = this;
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];

        self.bedCurrentTemp = ko.observable(0);
        self.bedCurrentTarget = ko.observable(0);
        self.is_admin = ko.observable(false);
        self.pid = {
            fanSpeed: ko.observable(255),
            noCycles: ko.observable(5),
            hotEndIndex: ko.observable(0),
            targetTemp: ko.observable(200)
        };

        OctoPrint.printer.getBedState().done(function (bedState) {
            self.bedCurrentTemp(bedState.bed.actual);
            self.bedCurrentTarget(bedState.bed.target);
        });

        self.onBeforeBinding = self.onUserLoggedIn = self.onUserLoggedOut = function () {
            self.pid.fanSpeed(self.settingsViewModel.settings.plugins.CalibrationTools.pid.fanSpeed());
            self.pid.noCycles(self.settingsViewModel.settings.plugins.CalibrationTools.pid.noCycles());
            self.pid.hotEndIndex(self.settingsViewModel.settings.plugins.CalibrationTools.pid.hotEndIndex());
            self.pid.targetTemp(self.settingsViewModel.settings.plugins.CalibrationTools.pid.targetTemp());
            self.is_admin(self.loginStateViewModel.isAdmin());
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