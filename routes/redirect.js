var express = require('express');
var router = express.Router();
var path = require('path');

router.get('/', function(req, res, next) {
    const id = req.query;

    console.log(id);
    if(!id) {
      return res.send({error:"params missing."});
    }

    try{
    require("../db/db.js").get({id}, function(err,docs) {
      var u = docs[0].url
      if(!u.startsWith("https://") || !u.startsWith("http://")) {
        u = "http://" + u;
      }

      res.redirect(docs[0].url);
    });
  }catch(e) {
    return res.send({error});
  }
});

// CMuqYSdQyJUi & M5mJlfojWuBd
module.exports = router;
