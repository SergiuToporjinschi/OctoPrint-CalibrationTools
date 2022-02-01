$(function () {
    function CalibrationToolsPIDTuneViewModel(parameters) {
        var self = this;

        self.bedCurrentTemp = ko.observable(0);
        self.bedCurrentTarget = ko.observable(0);

        OctoPrint.printer.getBedState().done(function (bedState) {
            self.bedCurrentTemp(bedState.bed.actual);
            self.bedCurrentTarget(bedState.bed.target);
        });
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