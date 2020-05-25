import database
import json
from users import User

with open('config.json') as _config:
    data = json.load(_config)
config = {"port": data["port"], "database": data["database"], "url": data["url"], "rEnabled": data["ratelimit"]["enabled"]}
db = database.Database(config.get("database"))
#print(db.addUser(User("test", "test@lordjbs.xyz", "test123")))
print(db.getAllUsers()[0].getName())