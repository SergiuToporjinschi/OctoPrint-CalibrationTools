$(function () {
    function CalibrationToolsGeneralViewModel(parameters) {
        this.loginState = parameters[0];
        var self = this;
        self.decimal3 = function (defaultVal) {
            return {
                numeric: {
                    decimals: 3,
                    default: defaultVal
                }
            }
        }
        self.isSmall = ko.observable($("#tab_plugin_CalibrationTools").width() < 800);
        ko.extenders.numeric = function (target, options) {
            var returnObs = ko.pureComputed({
                read: target,
                write: function (value) {
                    var newVal = options.decimals ? parseFloat(value).toFixed(options.decimals) : parseInt(value);
                    target(isNaN(newVal) ? options.default : newVal);
                }
            }).extend({
                notify: 'always'
            });
            returnObs(target());
            return returnObs;
        };

        self.onStartupComplete = function () {
            this.isSmall($("#tabs_content").width() < 800);
        }
        self.notify = function (title, message, type, hide) {
            new PNotify({
                title: title,
                text: message,
                type: type,
                hide: hide
            });
        }
        self.notifyError = function (title, message) {
            self.notify(title, message, 'error', false);
        }
        self.notifyInfo = function (title, message) {
            self.notify(title, message, 'info', true);
        }
        self.notifyWarning = function (title, message) {
            self.notify(title, message, 'warning', false);
        }
        self.failedFunction = function (response) {
            self.notifyError("Error", response.responseJSON.error);
        }
    }
    OCTOPRINT_VIEWMODELS.push({
        // This is the constructor to call for instantiating the plugin
        construct: CalibrationToolsGeneralViewModel,
        name: "calibrationToolsGeneralViewModel",
        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        dependencies: ["loginStateViewModel"]
        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
    });
});