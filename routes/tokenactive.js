const config = require("../conf.json");
var express = require('express');
var router = express.Router();
var path = require('path');
const utils = require("../lib/util.js");

router.get('/', function(req, res, next) {if(config.userSystem.enabled == true) return res.send({active: true}); else return res.send({active: false});});

  

module.exports = router;
