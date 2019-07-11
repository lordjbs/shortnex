const low = require('lowdb')
const FileSync = require('lowdb/adapters/FileSync')

const adapter = new FileSync(require("../config.json").db)
const db = low(adapter)


const database = {
  url: {
    add: function(id, url, date, func) {
      console.log("ran")
      try {
      db.get("urls")
      .push({id, url, date})
      .write();
      console.log("done");
      func(null);
      } catch(e) {
        func(e);
        console.log(e);
      }

      console.log(db.getState());
    },
    get: function(id, func) {
      console.log("ran")
      var url = "";
      var err = null;
      try {
        url = db.get("urls").find({id:id}).value().url;
        docs = url;

        console.log(url);

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
  
        console.log(db.getState());
      },
      getToken: function(token, func) {
        var token = null;
        var err = null;
        try {
          token = db.has(token);
  
          console.log(token);
  
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