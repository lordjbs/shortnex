# shortnex v2.0
# made by jbs (https://github.com/lordjbs/)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, request, redirect, render_template
import utils
from database import Database
import json
import time

VERSION = "v2.0"
print("shortnex " + VERSION + "\nmade by jbs")

print("shortnex | Loading config and flask")
with open('config.json') as _config:
    data = json.load(_config)
config = {"port": data["port"], "database": data["database"], "url": data["url"]}
db = Database(config.get("database"))

app = Flask(__name__, static_url_path='/static/')

@app.route('/')
def index():
    return render_template("index.html")


# curl --header "Content-Type: application/json, charset=utf-8" --request POST --data '{"url":"https://example.org"}' http://localhost:5000/shorten
@app.route("/shorten", methods=['POST'])
def shorten():
    if request.method != "POST":
        return {"success": "false", "error": "This route is POST only."}

    content = request.get_json()
    if not "url" in content:
        return {"success": False, "error": "The parameter 'url' does not exist.", "code": 1}

    if utils.checkIfProperURL(content.get("url")) is None:
        return {"success": False, "error": "That is not a proper url.", "code": 1}

    url = utils.returnProperURL(content.get("url"))
    #TODO: Make the url config thing better lol
    try:
        id = utils.createID()
        db.addURL(id, content.get("url"), int(time.time()))
        return {"success": True, "id": id, "url": config.get("url")}
    except Exception:
        return {"success": False, "error": "Error has occurred while shortening. Please contact an administrator."}


@app.route("/<id>")
def goto(id):
    url = db.getURL(id)
    if not url:
        return {"success": False, "error": "Invalid ID"}
    else:
        if not str.startswith(url, "https://") or not str.startswith(url, "http://"):
            return redirect("https://" + url)
        return redirect(url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.get("port"))