$(function () {
    function CalibrationToolsXYZStepsModelView(parameters) {
        var self = this;
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];
        self.controlViewModel = parameters[2];
        self.generalVM = parameters[5];
        self.columnLabelCls = ko.computed(function () {
            return self.generalVM.isSmall() ? "span2" : "span3";
        });
        self.columnFieldCls = ko.computed(function () {
            return self.generalVM.isSmall() ? "span10" : "span9";
        });
        self.eStepsXYZ = {
            currentSteps: {
                X: ko.observable(0).extend(self.generalVM.decimal3(0.000)),
                Y: ko.observable(0).extend(self.generalVM.decimal3(0.000)),
                Z: ko.observable(0).extend(self.generalVM.decimal3(0.000))
            },
            gCodeCubeSize: {
                X: ko.observable().extend(self.generalVM.decimal3(22.000)),
                Y: ko.observable().extend(self.generalVM.decimal3(22.000)),
                Z: ko.observable().extend(self.generalVM.decimal3(22.000))
            },
            printedCubeSize: {
                X: ko.observable().extend(self.generalVM.decimal3(25.000)),
                Y: ko.observable().extend(self.generalVM.decimal3(25.000)),
                Z: ko.observable().extend(self.generalVM.decimal3(25.000))
            },
            newSteps: {
                X: ko.observable().extend(self.generalVM.decimal3(0.000)),
                Y: ko.observable().extend(self.generalVM.decimal3(0.000)),
                Z: ko.observable().extend(self.generalVM.decimal3(0.000))
            }
        };

        self.eStepsXYZ.newSteps.X = ko.computed(function () {
            return parseFloat(self.eStepsXYZ.currentSteps.X() * self.eStepsXYZ.gCodeCubeSize.X() / self.eStepsXYZ.printedCubeSize.X()).toFixed(3);
        }, self);
        self.eStepsXYZ.newSteps.Y = ko.computed(function () {
            return parseFloat(self.eStepsXYZ.currentSteps.Y() * self.eStepsXYZ.gCodeCubeSize.Y() / self.eStepsXYZ.printedCubeSize.Y()).toFixed(3);
        }, self);
        self.eStepsXYZ.newSteps.Z = ko.computed(function () {
            return parseFloat(self.eStepsXYZ.currentSteps.Z() * self.eStepsXYZ.gCodeCubeSize.Z() / self.eStepsXYZ.printedCubeSize.Z()).toFixed(3);
        }, self);

        self.loadEStepsActive = ko.observable(true);
        self.loadESteps = function () {
            self.loadEStepsActive(false);
            OctoPrint.simpleApiCommand("CalibrationTools", "eSteps_load").done(function (response) {
                self.eStepsXYZ.currentSteps.X(response.data.X);
                self.eStepsXYZ.currentSteps.Y(response.data.Y);
                self.eStepsXYZ.currentSteps.Z(response.data.Z);
            }).always(function (response) {
                self.loadEStepsActive(true);
            })
        };

        self.saveEStepsXYZActive = ko.observable(true)
        self.saveEStepsXYZ = function () {
            self.saveEStepsXYZActive(false);
            OctoPrint.simpleApiCommand("CalibrationTools", "eSteps_save", {
                "newXSteps": self.eStepsXYZ.newSteps.X(),
                "newYSteps": self.eStepsXYZ.newSteps.Y(),
                "newZSteps": self.eStepsXYZ.newSteps.Z()
            }).done(function (response) {
                new PNotify({
                    title: "Saved",
                    text: "X: " + self.eStepsXYZ.newSteps.X() + "steps/mm<br>Y: " + self.eStepsXYZ.newSteps.Y() + "steps/mm<br>Z: " + self.eStepsXYZ.newSteps.Z() + " steps/mm<br> had been set for X/Y/Z axes",
                    type: "info"
                });
            }).always(function (response) {
                self.saveEStepsXYZActive(true);
            })
        };

        // self.labelColumnCss = viewModel.profitStatus = ko.pureComputed(function () {
        //     return "span3" $("#tab_plugin_CalibrationTools").width() < 800
        // });

        self.isAdmin = ko.observable(false);

        self.onBeforeBinding = self.onUserLoggedIn = self.onUserLoggedOut = function () {
            self.eStepsXYZ.gCodeCubeSize.X(self.settingsViewModel.settings.plugins.CalibrationTools.XYZSteps.gCodeCubeSize.X());
            self.eStepsXYZ.gCodeCubeSize.Y(self.settingsViewModel.settings.plugins.CalibrationTools.XYZSteps.gCodeCubeSize.Y());
            self.eStepsXYZ.gCodeCubeSize.Z(self.settingsViewModel.settings.plugins.CalibrationTools.XYZSteps.gCodeCubeSize.Z());

            self.eStepsXYZ.printedCubeSize.X(self.settingsViewModel.settings.plugins.CalibrationTools.XYZSteps.gCodeCubeSize.X());
            self.eStepsXYZ.printedCubeSize.Y(self.settingsViewModel.settings.plugins.CalibrationTools.XYZSteps.gCodeCubeSize.Y());
            self.eStepsXYZ.printedCubeSize.Z(self.settingsViewModel.settings.plugins.CalibrationTools.XYZSteps.gCodeCubeSize.Z());

            self.isAdmin(self.loginStateViewModel.isAdmin());
        }
    }
    OCTOPRINT_VIEWMODELS.push({
        // This is the constructor to call for instantiating the plugin
        construct: CalibrationToolsXYZStepsModelView,
        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        dependencies: ["loginStateViewModel", "settingsViewModel", "controlViewModel", "terminalViewModel", "accessViewModel", "calibrationToolsGeneralViewModel"],
        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        elements: ["#calibration_x-y-z"]
    });
});