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
        output = self.db.execute("CREATE TABLE IF NOT EXISTS urls (id text, url text, date integer)")
        self.conn.commit()

    def addURL(self, id, url, date):
        try:
            self.db.execute("INSERT INTO urls VALUES (:i, :u, :d)", {'i': id, 'u': url, 'd': date})
        except Exception as e:
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
