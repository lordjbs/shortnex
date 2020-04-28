# shortnex v2.0
# made by jbs (https://github.com/lordjbs/)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, request, redirect, send_from_directory, render_template, url_for
import utils
from database import Database
import json
import time

with open('config.json') as _config:
    data = json.load(_config)
config = {"port": data["port"], "database": data["database"]}
db = Database(config.get("database"))

app = Flask(__name__, static_url_path='/static/')


@app.route('/')
def index():
    return render_template("index.html")


# curl --header "Content-Type: application/json, charset=utf-8" --request POST --data '{"url":"https://lordjbs.xyz"}' http://localhost:5000/shorten
@app.route("/shorten", methods=['POST'])
def shorten():
    if request.method != "POST":
        return {"success": "false", "error": "This route is POST only."}

    content = request.get_json()
    print(content)
    if not "url" in content:
        return {"success": False, "error": "The parameter 'url' does not exist.", "code": 1}

    if utils.checkIfProperURL(content.get("url")) is None:
        return {"success": False, "error": "That is not a proper url.", "code": 1}

    url = utils.returnProperURL(content.get("url"))

    try:
        id = utils.createID()
        db.add(id, content.get("url"), int(time.time()))
        return {"success": True, "id": id, "url": request.base_url}
    except Exception:
        return {"success": False, "message": "Error has occurred while shortening. Please contact an administrator."}


@app.route("/<id>")
def goto(id):
    if not db.getURL(id):
        return {"success": False, "error": "Invalid ID"}
    else:
        return redirect(db.getURL(id))

@app.route("/check/tokensystem")
def tokensystem():
    return {"active": False}

