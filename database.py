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


import sqlite3
import traceback
from users import User

class Database:
    def __init__(self, file):
        print("shortnex | Loading database")
        try:
            self.conn = sqlite3.connect(file, check_same_thread=False)
            self.db = self.conn.cursor()
            print("shortnex | Connected to database!")
            print("shortnex | Testing database...")
            self.checkStart()
            print("shortnex | Success testing database!")

        except Exception:
            print("shortnex | Database connection failed. Exiting...")
            exit(0)

    def __close__(self):
        self.conn.commit()
        self.conn.close()

    def checkStart(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS urls (id text, url text, date integer)")
        self.conn.commit()
        self.db.execute("CREATE TABLE IF NOT EXISTS users (name text, email text, token text)")

    def addURL(self, id, url, date):
        try:
            self.db.execute("INSERT INTO urls VALUES (:i, :u, :d)", {'i': id, 'u': url, 'd': date})
        except Exception:
            traceback.print_exc()
        self.conn.commit()

    def getURL(self, id):
        try:
            a = self.db.execute("""SELECT url FROM urls WHERE id = :bruh;""", {'bruh': id})
            value = a.fetchone()[0]

            if value is None:
                return None
            else:
                return value
        except TypeError:
            return None
    
    def getAllUsers(self):
        try:
            a = self.db.execute("SELECT * FROM users;")
            values = list(a.fetchall())
            output = []
            for val in values:
                output.append(User(val[0], val[1], val[2]))
            return output
        except Exception:
            return None
    
    def addUser(self, user):
        if not isinstance(user, User):
            return {"success": False, "message": "That is not a user object."}
        else:
            try:
                self.db.execute("""INSERT INTO users VALUES (:a, :b, :c)""", {'a': user.getName(), 'b': user.getEmail(), 'c': user.getToken()})
                self.conn.commit()
                return True
            except Exception:
                traceback.print_exc()
                return {"success": False, "message": "Failed the query."}
    
    def removeUser(self, user):
        if not isinstance(user, User):
            return {"success": False, "message": "That is not a user object."}
        else:
            try:
                self.db.execute("""DELETE FROM users WHERE token = :a""", {'a': user.getToken()})
                self.conn.commit()
                return True
            except Exception:
                traceback.print_exc()
                return {"success": False, "message": "Failed the query."}