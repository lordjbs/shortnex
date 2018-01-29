var express = require('express');
var router = express.Router();
var path = require('path');

router.get('/', function(req, res, next) {
    var url = req.query.url;
    const createdat = new Date();
    if(!url) {
      return res.send({error:"params missing."});
    }
    try{
        var id = makeid();
        const db = require("../db/db.js");
        if(!url.startsWith("http://") || !url.startsWith("https://")) {
          url = "http://" + url;
        }
        db.insert({id, url, createdat}, function(err) {
          if(err) {
            res.send(err);
          }else {
            res.send({success:true, id, url: req.get('host') });
          }
        });
    } catch(e) {
        res.send({error:e});
        console.error(e)
    }

});

function makeid() {
    var text = "s";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 5; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
  }

module.exports = router;
