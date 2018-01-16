var Datastore = require('nedb')
var db;

exports.load = () => {
   db = new Datastore({ filename: require("../conf.json").db, autoload: true });
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
