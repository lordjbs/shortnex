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

class User:
    def __init__(self, _name, _token):
        self.name = _name
        self.token = _token
        self.shortenedLinks = []
    
    def getName(self):
        return self.name
    
    def getToken(self):
        return self.token
    
    def getShortenedLinks(self):
        return self.shortenedLinks

class UserSystem:
    def __init__(self):
        self.users = {User("test", "test")}

    def checkIfUserExists(self, token):
        output = False
        for user in users:
            if token is user.getToken():
                return user
            else:
                output = False
        
        return output

    #add db shit
    def addUser(self, userobj):
        if isinstance(userobj, User):
            self.users.add(userobj)
        else:
            return {"success": False, "message": "Not a users.py:User() object."}

