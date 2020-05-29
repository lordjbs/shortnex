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
import traceback
from ratelimit import Ratelimit
from users import User, UserSystem

VERSION = "v2.0"
print("shortnex " + VERSION + "\nmade by jbs")

print("shortnex | Loading config")
with open('config.json') as _config:
    data = json.load(_config)
config = {"port": data["port"], "database": data["database"], "url": data["url"], "rEnabled": data["ratelimit"]["enabled"], "uEnabled": data["usersystem"], "master": data["masterToken"]}
print("shortnex | Done...")
db = Database(config.get("database"))

print("shortnex | Loading ratelimit service...")
ratelimits = Ratelimit()

if config["rEnabled"]:
    try:
        ratelimits.loop()
        print("shortnex | Done loading ratelimit service!")
    except Exception:
        traceback.print_exc()
        print("shortnex | Failed loading ratelimit service, you could report this issue on git... Exiting..")
        exit(0)
else:
    print("shortnex | Ratelimit service is disabled, not loading.")


print("shortnex | Loading user service...")
if config["uEnabled"]:
    try:
        users = UserSystem(db)
        print("shortnex | Done loading user service!")
    except Exception:
        traceback.print_exc()
        print("shortnex | Failed loading user service, you could report this issue on git... Exiting..")
        exit(0)
else:
    print("shortnex | User service is disabled, not loading.")

print("shortnex | Loading flask...")

app = Flask(__name__, static_url_path='/static/')

print("shortnex | Successfully started! :)")


@app.route('/')
def index():
    return render_template("index.html")

# Clean: curl --header "Content-Type: application/json, charset=utf-8" --request POST --data '{"url":"https://example.org"}' http://localhost:5000/shorten
# PC: curl --header "Content-Type: application/json, charset=utf-8" --header "Authorization: 7t46eYTBh87WMpC7QndAmsUk3VKtXfgB" --request POST --data '{"url":"https://example.org"}' http://localhost:5000/shorten
# Laptop: curl --header "Content-Type: application/json, charset=utf-8" --header "Authorization: 46gRGjdWEqqZJ95xKYLYkJMtWsvZkncW" --request POST --data '{"url":"https://example.org"}' http://localhost:5000/shorten
@app.route("/shorten", methods=['POST'])
def shorten():
    if not ratelimits.check(request.remote_addr):
        return {"success": False, "message": "You are being ratelimited."}

    if request.method != "POST":
        return {"success": False, "message": "This route is POST only."}

    #Authorization
    authed = False
    if config["uEnabled"]:
        headers = list(request.headers)

        for key, val in headers:
            if "Authorization" in key:
                if not users.checkIfUserExists(val):
                    return {"success": False, "message": "No permissions"}
                else:
                    authed = True
        
        if not authed:
            return {"success": False, "message": "No permissions."}

    
    content = request.get_json()
    if not "url" in content:
        return {"success": False, "message": "The parameter 'url' does not exist.", "code": 1}

    if utils.checkIfProperURL(content.get("url")) is None:
        return {"success": False, "message": "That is not a proper url.", "code": 1}

    # url = utils.returnProperURL(content.get("url"))
    # TODO: Make the url config thing better lol
    try:
        id = utils.createID()
        db.addURL(id, content.get("url"), int(time.time()))
        return {"success": True, "id": id, "url": config.get("url")}
    except Exception:
        return {"success": False, "message": "Error has occurred while shortening. Please contact an administrator."}


@app.route("/<id>")
def goto(id):

    url = db.getURL(id)
    if not url:
        return {"success": False, "error": "Invalid ID"}
    else:
        return redirect(utils.returnProperURL(url))

# curl --header "Content-Type: application/json, charset=utf-8" --header "Authorization: 123456" --request POST --data '{"name":"user1", "email":"test@test.com"}' http://localhost:5000/users/create

@app.route("/users/create", methods=['POST'])
def createUser():

    if request.method != 'POST':
        return {"success": False, "message":"This route is POST only."}
    
    if not config["uEnabled"]:
        return {"success": False, "message": "Disabled."}

    headers = list(request.headers)
    success = False

    for key, val in headers:
        if "Authorization" in key:
            if not val == config["master"]:
                return {"success": False, "message": "Not authorized."}
            else:
                success = True
    
    if not success:
        return {"success": False, "message": "Auth header is missing."}


    reqcon = request.get_json()

    print(reqcon)

    if not 'name' or not 'email' in reqcon:
        return {"success": False, "message":"Missing argument, either name, email or auth."}
    
    token = utils.createRandomString(32)
    user = User(reqcon["name"], reqcon["email"], token)
    users.addUser(user)

    return {"success": True, "message":"Successfully created new user.", "name": reqcon["name"], "email": reqcon["email"], "token": token}

#TODO: As above
#TODO: Add functionality
@app.route("/users/delete", methods=['POST'])
def deleteUser():
    if request.method != 'POST':
        return {"success": False, "message":"This route is POST only."}
    
        if not config["uEnabled"]:
            return {"success": False, "message": "Disabled."}

    headers = list(request.headers)
    success = False

    for key, val in headers:
        if "Authorization" in key:
            if not val == config["master"]:
                return {"success": False, "message": "Not authorized."}
            else:
                success = True
    
    if not success:
        return {"success": False, "message": "Auth header is missing."}


    reqcon = request.get_json()

    print(reqcon)

    if not 'name' or not 'email' in reqcon:
        return {"success": False, "message":"Missing argument, either name, email or auth."}
    
    token = utils.createRandomString(32)
    user = User(reqcon["name"], reqcon["email"], token)
    users.addUser(user)

    return {"success": True, "message":"Successfully created new user.", "name": reqcon["name"], "email": reqcon["email"], "token": token}



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.get("port"))
