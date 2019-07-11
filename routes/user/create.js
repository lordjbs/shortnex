var express = require('express');
var router = express.Router();
var path = require('path');
const utils = require("../../lib/util.js");
const db = require("../../db/db.js");
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
    } else if (_name.length < 3) {
        return res.send({success:false, message:"No username set or its too short (min 3)"});
    } else {
        var token = utils.makeToken();
        db.user.create(_name, token,new Date(), function(err) {
            if(err) {
  
              res.send({
                success: false,
                 error: err,
                 message: "Unexpected User Database Error (Error Code: 6)",
                 code:6
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
