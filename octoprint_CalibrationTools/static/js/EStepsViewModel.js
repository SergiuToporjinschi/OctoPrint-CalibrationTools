$(function () {
    function CalibrationToolsEStepsModelView(parameters) {
        var self = this;
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];
        self.controlViewModel = parameters[2];
        self.terminalViewModel = parameters[3];
        self.access = parameters[4];

        self.is_admin = ko.observable(false);
        self.steps = ko.observable();
        self.steps["X"] = ko.observable();
        self.steps["Y"] = ko.observable();
        self.steps["Z"] = ko.observable();
        self.steps["E"] = ko.observable();

        self.testParam = {};
        self.testParam["extrudeTemp"] = ko.observable(210);
        self.testParam["extrudeLength"] = ko.observable(100);
        self.testParam["extrudeSpeed"] = ko.observable(50);
        self.testParam["markLength"] = ko.observable(120);

        self.results = {};
        self.results["remainedLength"] = ko.observable(20);
        self.results["actualExtrusion"] = ko.computed(function () {
            return (self.testParam.markLength() - self.results.remainedLength()).toFixed(3);
        });
        self.results["newSteps"] = ko.computed(function () {
            return (self.steps.E() / self.results.actualExtrusion() * 100).toFixed(3);
        });
        self.results["newStepsDisplay"] = ko.computed(function () {
            return "M92 E" + self.results.newSteps();
        });

        self.onBeforeBinding = self.onUserLoggedIn = self.onUserLoggedOut = function () {
            self.testParam.extrudeTemp(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.extrudeTemp());
            self.testParam.extrudeLength(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.extrudeLength());
            self.testParam.extrudeSpeed(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.extrudeSpeed());
            self.testParam.markLength(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.markLength());
            self.is_admin(self.loginStateViewModel.isAdmin());
        }

        self.from_json = function (response) {
            self.steps["X"](response.data.X);
            self.steps["Y"](response.data.Y);
            self.steps["Z"](response.data.Z);
            self.steps["E"](response.data.E);
        }

        self.loadEStepsActive = ko.observable(true);
        self.loadESteps = function () {
            self.loadEStepsActive(false);
            OctoPrint.simpleApiCommand("CalibrationTools", "eSteps_load").done(function (response) {
                self.from_json(response);
            }).always(function (response) {
                self.loadEStepsActive(true);
            })
        }
        self.startExtrusionActive = ko.observable(false)
        self.startExtrusion = function () {
            self.startExtrusionActive(true);
            OctoPrint.simpleApiCommand("CalibrationTools", "eSteps_startExtrusion", {
                "extrudeTemp": self.testParam.extrudeTemp(),
                "extrudeLength": self.testParam.extrudeLength(),
                "extrudeSpeed": self.testParam.extrudeSpeed()
            }).done(function (response) {
                new PNotify({
                    title: "E axe calibration started",
                    text: "<span style='font-weight:bold; color: red;'>Heating nuzzle has started!!!</span><br> When extrusion stops you have to fulfil <b>Length after extrusion</b> and save the new value ",
                    type: "warning"
                });
                console.log(response);
            }).fail(function (response) {
                new PNotify({
                    title: "Error on starting extrusion ",
                    text: response.responseJSON.error,
                    type: "error",
                    hide: false
                });
            }).always(function (response) {
                self.startExtrusionActive(false);
            });
        }

        self.saveESteps = function () {
            OctoPrint.simpleApiCommand("CalibrationTools", "eSteps_save", {
                "newESteps": self.results.newSteps()
            }).done(function () {
                new PNotify({
                    title: "Saved",
                    text: self.results.newSteps() + " steps/mm had been set for E axe",
                    type: "info"
                });
            });
        }

        self.onAllBound = self.onEventConnected = function () {
            OctoPrint.simpleApiGet("CalibrationTools").done(function (response) {
                self.from_json(response);
            });
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push({
        // This is the constructor to call for instantiating the plugin
        construct: CalibrationToolsEStepsModelView,
        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        dependencies: ["loginStateViewModel", "settingsViewModel", "controlViewModel", "terminalViewModel", "accessViewModel"],
        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        elements: ["#calibration_eSteps"]
    });
});