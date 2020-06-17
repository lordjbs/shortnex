# shortnex
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
    def __init__(self, _name, _email, _token):
        self.name = _name
        self.email = _email
        self.token = _token
    
    def getName(self):
        return self.name

    def getEmail(self):
        return self.email
    
    def getToken(self):
        return self.token
    
class UserSystem:
    def __init__(self, _db):
        self.users = _db.getAllUsers()
        self.db = _db

        for user in _db.getAllUsers():
            print(user.getToken())

    def checkIfUserExists(self, token):
        output = False
        for user in self.users:
            if str(token) == str(user.getToken()):
                output = user
                return user
            else:
                output = False
        
        return output
    
    def get_user_by_name(self, name):
        for user in self.users:
            if str(name) == str(user.getName()):
                return user
        
        return False


    def addUser(self, userobj):
        if isinstance(userobj, User):
            self.db.addUser(userobj)
            self.refresh()
        else:
            return {"success": False, "message": "Not a users.py:User() object."}
    
    def remove_user(self, name):
        try:
            user = self.get_user_by_name(name)
            if not user:
                return {"success": False, "message": "User does not exist."}
            
            self.db.removeUser(user)
            self.refresh()
            return {"success": True}
        except Exception:
            return {"success": False, "message": "Removing failed."}
    
    def refresh(self):
        self.users = self.db.getAllUsers()

