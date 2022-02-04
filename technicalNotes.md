# PID

#### M301 -> set PID hotEnd

Send: M301
echo: p:28.27 i:2.82 d:70.81
echo: M301 P27.08 I2.51 D73.09
Recv: ok

#### M304 -> set BED hotEnd

Send: M304
echo: p:18.84 i:1.18 d:201.41
echo: M304 P131.06 I11.79 D971.23
Recv: ok

#### PID auto-tune ends like this:

T:202.00 /0.00 B:25.00 /0.00 @:0 B@:0
bias: 120 d: 120 min: 197.00 max: 203.00 Ku: 50.93 Tu: 20.20
Classic PID
Kp: 30.56 Ki: 3.03 Kd: 77.16
PID Autotune finished! Put the last Kp, Ki and Kd constants from below into Configuration.h
\#define DEFAULT_Kp 30.56
\#define DEFAULT_Ki 3.03
\#define DEFAULT_Kd 77.16
ok

#### All PID formats

!!DEBUG:send echo: Kp: 30.56 Ki: 3.03 Kd: 77.16
!!DEBUG:send Kp: 30.56 Ki: 3.03 Kd: 77.16
!!DEBUG:send echo: p:18.84 i:1.18 d:201.41
!!DEBUG:send p:18.84 i:1.18 d:201.41
!!DEBUG:send echo: M304 P131.06 I11.79 D971.23
!!DEBUG:send M304 P131.06 I11.79 D971.23

## regex for all pid formats

    r".*p:{0,1}\s{0,1}?(?P<p>\d{1,3}.\d{1,3})\sk*i:{0,1}\s{0,1}?(?P<i>\d{1,3}.\d{1,3})\sk*d:{0,1}\s{0,1}?(?P<d>\d{1,3}.\d{1,3})"

# Util Octoprint functions

#### Regex for getting temperatures

\s*T:(?P<toolTemp>\d{1,3}.\d{1,3}).*B:(?P<betTemp>\d{1,3}.\d{1,3}).\*

#### extrude command from JS

OctoPrint.printer.issueToolCommand("extrude", {"amount":100, "speed":50})

#### Notification JS

new PNotify({
title: "Success",
text: _.sprintf(text, {
command: _.escape(commandSpec.name)
}),
type: "success"
});

#### Notification JS with buttons

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

#### confirmation modal

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

#### dialog with showing progress

showProgressModal(options, promise)

#### dialog with multi buttons

showSelectionDialog({"title": "tt", "message": "text", "selections":["ss","fdgd","asdas","asda"]})

#### Message dialog

showMessageDialog("sss", {options})

#### Modal dialog with buttons

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
