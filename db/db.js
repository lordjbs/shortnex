var Datastore = require('nedb')
var db;

exports.load = (func) => {
  console.log("Loading Database");
  try{
    db = new Datastore({ filename: require("../conf.json").db, autoload: true });
    func("Success! Database loaded!")
    exports.db = db;
  }catch(error) {
    return func("Cannot load Database. " + error.message);
  }
}

exports.insert = function(stuff, func) {
  db.insert(stuff, function(err) {
    func(err);
  });

}

exports.get = function(stuff, func) {
  db.find(stuff, function(err,docs) {
    func(err,docs);
  })
}
exports.db = db;
