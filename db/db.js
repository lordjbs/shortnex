const low = require('lowdb')
const FileSync = require('lowdb/adapters/FileSync')

const adapter = new FileSync(require("../conf.json").db)
const db = low(adapter)



const database = {
  test: function(func) {
    func(db.get("init").find({bool:true}).value());
  },
  url: {
    add: function(id, url, date, func) {
      try {
      db.get("urls")
      .push({id, url, date})
      .write();
      func(null);
      } catch(e) {
        func(e);
        console.log(e);
      }

    },
    get: function(id, func) {
      var url = "";
      var err = null;
      try {
        url = db.get("urls").find({id:id}).value().url;
        docs = url;

        func(err,url);
      } catch(e) {
        func(err,url);
        console.log(e);

      }

    }
  },
  user: {
      create: function(username, token, date, func) {
        try {
        db.get("users")
        .push({username, token, date})
        .write();
        func(null);
        } catch(e) {
          func(e);
          console.log(e);
        }
  
      },
      getToken: function(token, func) {
        var token = null;
        var err = null;
        try {
          token = db.has(token);
  
  
          func(err,token);
        } catch(e) {
          func(err,token);
          console.log(e);
  
        }
  
      },
      deleteUser: function(username, func) {
        try {
          db.get("users")
          .remove({username})
          .write();
          func(null);
          } catch(e) {
            func(e);
            console.log(e);
          }
      }
  }
};

module.exports = database;