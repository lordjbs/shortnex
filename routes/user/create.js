var express = require('express');
var router = express.Router();
var path = require('path');
const utils = require("../../lib/util.js");
const db = require("../../db/userdb.js");
const config = require("../../conf.json");

router.get('/', function(req, res, next) {
    // http://localhost/user/create?username=*name*&token=*token*
    const _token = req.query.token;
    const _name = req.query.username;

    if(!config.userSystem.enabled) {
        res.status(404);
        return res.send({success:false, message:"Module not enabled."});
    }

    if(_token !== config.userSystem.password) {
        res.status(403);
        return res.send({success:false, message:"No Permissions."});
    } else {
        var token = utils.makeToken();
        db.insert({ _name, token, date: new Date()}, function(err) {
            if(err) {
  
              res.send({
                success: false,
                 error: err,
                 code:0
              });
  
            }else {

                var _response ={success:true,message:"Successfully created a new USER!", user: _name, token}
              console.log(_response);
                res.send(_response);
  
            }
          });
    }
});

  

module.exports = router;
