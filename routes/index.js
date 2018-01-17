var express = require('express');
var router = express.Router();
var path = require('path');

router.get('/', function(req, res, next) {
    if(!isEmptyObject(req.query)) {
        var id = req.query;
        id = Object.keys(id)[0];
        console.log(id);
        if(!id) {
          return res.send({error:"params missing."});
        }
    
        try{
        require("../db/db.js").get({id}, function(err,docs) {
            if(err) {
                return res.send({err});
            }
          var u;
          if(!isEmptyObject(docs)) {
              u = docs[0].url;
            }else {
                return res.send({error: "Cannot find in db."});
            }
            
          if(!u.startsWith("https://") || !u.startsWith("http://")) {
            u = "http://" + u;
          }
    
          return res.redirect(docs[0].url);
        }).catch(function(error) {
            res.send({error});
        });
      }catch(e) {
        return;
      }
    }else {
         return res.sendFile(path.resolve('public/html/index.html'));
    }
});

function isEmptyObject(obj) {
    return !Object.keys(obj).length;
  }
  

module.exports = router;
