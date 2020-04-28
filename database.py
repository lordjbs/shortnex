# shortnex v2.0
# made by jbs (https://github.com/lordjbs/)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
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

    def add(self, id, url, date):
        print("cbt")
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
