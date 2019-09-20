const config = require("../conf.json");
var express = require('express');
var router = express.Router();
var path = require('path');
const utils = require("../lib/util.js");

router.get('/', function(req, res, next) {
    var string = req.query.string;
    return res.send({string.length()});
});

  

module.exports = router;
