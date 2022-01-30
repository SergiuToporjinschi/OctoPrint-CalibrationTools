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

## Notification JS with buttons
new PNotify({
    title: "tit",
    text: "sime",
    hide: false,
    confirm: {
        confirm: true,
        buttons: [
        {
            text: "btnText",
            click: function(notice) {console.log("btnPress")
                                     }
        }
    ]},
    buttons: {
        sticker: false,
        closer: false
    }
})


## confirmation modal
showConfirmationDialog({
    title: gettext("Are you sure you want to update now?"),
    html: "ss",
    proceed: gettext("Proceed"),
    onproceed: function() {
        console.log("proc");
    },
    onclose: function() {
        console.log("close");
    }
});


## dialog with showing progress
showProgressModal(options, promise)

## dialog with multi buttons
showSelectionDialog({"title": "tt", "message": "text", "selections":["ss","fdgd","asdas","asda"]})

## Message dialog
showMessageDialog("sss", {options})

## modal dialog with buttons
showConfirmationDialog({
"message": "something",
"question": "que?",
"cancel" : "somaCancel",
"proceed" : "someProceed",
})
    var title = options.title || gettext("Are you sure?");
    var message = options.message || "";
    var question = options.question || gettext("Are you sure you want to proceed?");
    var html = options.html;
    var checkboxes = options.checkboxes;
    var cancel = options.cancel || gettext("Cancel");
    var proceed = options.proceed || gettext("Proceed");
    var proceedClass = options.proceedClass || "danger";
    var onproceed = options.onproceed || undefined;
    var oncancel = options.oncancel || undefined;
    var onclose = options.onclose || undefined;
    var dialogClass = options.dialogClass || "";
    var nofade = options.nofade || false;
    var noclose = options.noclose || false;