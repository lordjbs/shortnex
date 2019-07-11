var express = require('express');
var router = express.Router();
var path = require('path');
const utils = require("../lib/util.js");

router.get('/', function(req, res, next) {
    if(!utils.isEmpty(req.query)) {
        var id = req.query;

        id = Object.keys(id)[0];
        if(!id) {
          return res.send({error:"params missing."});
        }
    
        try{
        require("../db/db.js").url.get(id, function(err,docs) {
            if(err) {
                return res.send({err});
            }
          var u;
          if(!utils.isEmpty(docs)) {
              u = docs;
            }else {
                return res.send({success: false, error: "This URL is not in the Database. (Error Code: 5)"});
            }
            
          if(!u.startsWith("https://") || !u.startsWith("http://")) {
            u = "http://" + u;
          }
    
          return res.redirect(docs);
        }).catch(function(error) {
            res.send({success: false, error, message:"Unexpected Database Error. (Error Code: 0)"});
        });
      }catch(e) {
        return;
      }
    }else {
         return res.sendFile(path.resolve('public/html/index.html'));
    }
});

  

module.exports = router;
