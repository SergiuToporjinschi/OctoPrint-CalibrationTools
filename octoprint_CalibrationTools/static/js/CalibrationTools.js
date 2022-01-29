$(function () {
    function CalibrationToolsViewModel(parameters) {
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
        self.results = {};

        self.results["remainedLength"] = ko.observable(20);
        self.results["markLength"] = ko.observable(120);
        self.results["actualExtrusion"] = ko.computed(function () {
            return (self.results.markLength() - self.results.remainedLength()).toFixed(3);
        });

        self.results["newSteps"] = ko.computed(function () {
            return (self.steps.E() / self.results.actualExtrusion() * 100).toFixed(3);
        });

        self.onBeforeBinding = self.onUserLoggedIn = self.onUserLoggedOut = function () {
            self.is_admin(self.loginStateViewModel.isAdmin());
        }

        /**open settings*/
        self.openCalibrationSettings = function () {
            $('a#navbar_show_settings').click();
            $('li#settings_plugin_CalibrationTools_link a').click();
            $("#settings_plugin_CalibrationTools").click();
        }

        self.from_json = function (response) {
            self.steps["X"](response.data.X);
            self.steps["Y"](response.data.Y);
            self.steps["Z"](response.data.Z);
            self.steps["E"](response.data.E);
        }

        self.loadESteps = function () {
            OctoPrint.simpleApiCommand("CalibrationTools","loadSteps").done(function (response) {
                self.from_json(response);
            })
            // OctoPrint.simpleApiGet("CalibrationTools").done(function (response) {
            //     console.log("CalibrationTools");
            //     self.from_json(response);
            // });
        }

        self.tempRestart = function () {
            OctoPrint.system.executeCommand("core", "restart");
        }
        self.runCommand = function () {
            OctoPrint.control.sendGcodeWithParameters("G90");
        }

        self.onAllBound = self.onEventConnected = function () {
            OctoPrint.simpleApiGet("CalibrationTools").done(function (response) {
                console.log("CalibrationTools");
                self.from_json(response);
            });
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push({
        // This is the constructor to call for instantiating the plugin
        construct: CalibrationToolsViewModel,
        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        dependencies: ["loginStateViewModel", "settingsViewModel", "controlViewModel", "terminalViewModel", "accessViewModel"],
        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        elements: ["#tab_plugin_CalibrationTools"]
    });
});