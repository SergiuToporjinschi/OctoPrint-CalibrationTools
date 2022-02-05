$(function () {
    function CalibrationToolsGeneralViewModel(parameters) {
        this.loginState = parameters[0];
        this.decimal3 = function (defaultVal) {
            return {
                numeric: {
                    decimals: 3,
                    default: defaultVal
                }
            }
        }
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
    }
    // OCTOPRINT_VIEWMODELS.push([GeneralViewModel, ["loginStateViewModel"], []]);
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