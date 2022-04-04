$(function () {
    function CalibrationToolsEStepsModelView(parameters) {
        var self = this;
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];
        self.controlViewModel = parameters[2];
        self.terminalViewModel = parameters[3];
        self.access = parameters[4];
        self.generalVM = parameters[5];

        self.columnLabelCls = ko.computed(function () {
            return self.generalVM.isSmall() ? "span4" : "span3";
        });
        self.columnFieldCls = ko.computed(function () {
            return self.generalVM.isSmall() ? "span8" : "span9";
        });

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
            return self.generalVM.round(self.testParam.markLength() - self.results.remainedLength());
        });
        self.results["newSteps"] = ko.computed(function () {
            return self.generalVM.round(self.steps.E() / self.results.actualExtrusion() * 100);
        });
        // self.results["newStepsDisplay"] = ko.computed(function () {
        //     return "M92 E" + self.results.newSteps();
        // });

        self.onBeforeBinding = self.onUserLoggedIn = self.onUserLoggedOut = function () {
            self.testParam.extrudeTemp(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.extrudeTemp());
            self.testParam.extrudeLength(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.extrudeLength());
            self.testParam.extrudeSpeed(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.extrudeSpeed());
            self.testParam.markLength(self.settingsViewModel.settings.plugins.CalibrationTools.eSteps.markLength());
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
                self.generalVM.notifyWarning("E-Steps calibration started", "<span style='font-weight:bold; color: red;'>Extruder heating has started!!!</span><br> When extrusion stops you will have to fill <b>Length after extrusion</b> and save the new value ")
            }).fail(function (response) {
                self.generalVM.notifyError("Error on starting extrusion ", response.responseJSON.error);
            }).always(function (response) {
                self.startExtrusionActive(false);
            });
        }

        self.saveESteps = function () {
            OctoPrint.simpleApiCommand("CalibrationTools", "eSteps_save", {
                "newESteps": self.results.newSteps()
            }).done(function () {
                self.generalVM.notifyInfo("Saved", self.results.newSteps() + " steps/mm has been set for E-Steps");
            }).fail(self.generalVM.failedFunction);
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
        dependencies: ["loginStateViewModel", "settingsViewModel", "controlViewModel", "terminalViewModel", "accessViewModel", "calibrationToolsGeneralViewModel"],
        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        elements: ["#calibration_eSteps"]
    });
});