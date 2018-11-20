var Datastore = require('nedb');
var db;

exports.load = (func) => {
  console.log("Loading User Database");
  try{
    db = new Datastore({ filename: require("../conf.json").userSystem.db, autoload: true });
    func("Success! User Database loaded!")
    exports.db = db;
  }catch(error) {
    return func("Cannot load User Database. " + error.message);
  }

};

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
