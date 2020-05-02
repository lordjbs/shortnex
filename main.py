# shortnex v2.0
# made by jbs (https://github.com/lordjbs/)
# Copyright (C) 2018-2020 jbs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    # TODO: Make the url config thing better lol
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
        return redirect(utils.returnProperURL(url))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.get("port"))
