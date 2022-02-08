import flask
import octoprint.plugin


class AutoTuneBLP(octoprint.plugin.BlueprintPlugin):
    @octoprint.plugin.BlueprintPlugin.route("/echo", methods=["GET"])
    def myEcho(self):
        if not "text" in flask.request.values:
            abort(400, description="Expected a text to echo back.")
        return flask.request.values["text"]

