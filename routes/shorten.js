var express = require('express');
var router = express.Router();
var path = require('path');
const db = require("../db/db.js");
const utils = require("../lib/util.js");
const config = require("../conf.json");

router.get('/', function(req, res, next) {
    var url = req.query.url;

    if (!url) {
        return res.send({
            success: false,
            code: 2
        });
    }

    if (url.length < 0) {
        return res.send({
            success: false,
            code: 1
        });
    }

    if (config.userSystem.enabled == true) {
        var token = req.query.token;
        if (!token) {
            return res.send({
                success: false,
                error: "no token given"
            });
        } else {
            db.user.getToken(token, function(error, response) {
                try {
                    if (error) {
                        res.send({
                            success: false,
                            error: "No Permissions!",
                            code:3
                        });
                    }

                    if(utils.isEmpty(response)) {
                        return res.send({
                            success:false,
                            error: "No Permissions!",
                            code:4
                        })
                    }
                    var id = utils.makeId();

                    if (!url.startsWith("http://") && !url.startsWith("https://")) {
                        url = "http://" + url;
                    }
                    db.url.add(id,url,new Date(), function(err) {
                        if (err) {
                            res.send({
                                success: false,
                                error: err,
                                code: 0
                            });
        
                        } else {
        
                            res.send({
                                success: true,
                                id,
                                url: config.url
                            });
        
                        }
                    });
                } catch (e) {
                    res.send({
                        error: e
                    });
                    console.error(e)
                }

            });
        }
    } else {

        try {
            var id = utils.makeId();

            if (!url.startsWith("http://") && !url.startsWith("https://")) {
                url = "http://" + url;
            }

            db.url.add(id,url,new Date(), function(err) {
                if (err) {
                    res.send({
                        success: false,
                        error: err,
                        code: 0
                    });

                } else {

                    res.send({
                        success: true,
                        id,
                        url: config.url
                    });

                }
            });
        } catch (e) {
            res.send({
                error: e
            });
            console.error(e)
        }
    }

});


module.exports = router;