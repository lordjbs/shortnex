var express = require('express');
var router = express.Router();
var path = require('path');

router.get('/', function(req, res, next) {
    const url = req.query.url;
    const ip = 0;
    const createdat = new Date();
    if(!url) {
      return res.send({error:"params missing."});
    }
    try{
      var id = makeid();
        const db = require("../db/db.js");
        db.insert({id, url, ip, createdat}, function(err) {
          if(err) {
            res.send(err);
          }else {
            res.send({success:true, id });
          }
        });
    } catch(e) {
        res.send({error:e});
        console.error(e)
    }

});

function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 12; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
  }

module.exports = router;
