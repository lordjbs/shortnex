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

from main import db

class User:
    def __init__(self, _name, _email, _token):
        self.name = _name
        self.email = _email
        self.token = _token
        self.shortenedLinks = []
    
    def getName(self):
        return self.name

    def getEmail(self):
        return self.email
    
    def getToken(self):
        return self.token
    
    def getShortenedLinks(self):
        return self.shortenedLinks

class UserSystem:
    def __init__(self):
        self.users = db.getAllUsers()

    def checkIfUserExists(self, token):
        output = False
        for user in self.users:
            if token is user.getToken():
                return user
            else:
                output = False
        
        return output

    #add db shit
    def addUser(self, userobj):
        if isinstance(userobj, User):
            db.addUser(userobj)
            self.refresh()
        else:
            return {"success": False, "message": "Not a users.py:User() object."}
    
    def refresh(self):
        self.users = db.getAllUsers()

