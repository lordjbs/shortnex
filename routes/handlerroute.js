var express = require('express');
var router = express.Router();
var path = require('path');

router.get('/', function(req, res, next) {
    return res.sendFile(path.resolve('public/html/jquery.min.js'));
});

module.exports = router;
