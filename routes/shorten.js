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
            const userdb = require("../db/userdb.js");
            userdb.get({
                token
            }, function(error, response) {
                try {
                    if (error) {
                        res.send({
                            success: false,
                            error: "No Permissions!"
                        });
                    }
                    var id = utils.makeId();

                    if (!url.startsWith("http://") && !url.startsWith("https://")) {
                        url = "http://" + url;
                    }

                    db.insert({
                        id,
                        url,
                        date: new Date()
                    }, function(err) {
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
                                url: req.get('host')
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

            db.insert({
                id,
                url,
                date: new Date()
            }, function(err) {
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
                        url: req.get('host')
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