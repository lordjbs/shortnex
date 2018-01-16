/**
 *   ____  _                _
 * / ___|| |__   ___  _ __| |_ _ __   _____  __
 * \___ \| '_ \ / _ \| '__| __| '_ \ / _ \ \/ /
 *  ___) | | | | (_) | |  | |_| | | |  __/>  <
 * |____/|_| |_|\___/|_|   \__|_| |_|\___/_/\_\
 *
 * Shortnex v1.0
 * @author lordjbs
 * @requires nodejs9
*/

const express = require('express');
const path = require('path');
const logger = require('morgan');
const bodyParser = require('body-parser');
const config = require("./conf.json");

const app = express();

app.use(express.static(path.join(__dirname, 'public')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use('/', require("./routes/index.js"));
app.use('/shorten', require("./routes/shorten.js"));
app.use('/redirect', require("./routes/redirect.js"));

app.use(function(req, res, next) {
    const err = new Error('Not Found');
    err.status = 404;
    next(err);
});

app.use(function(err, req, res, next) {
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    res.status(err.status || 500);
    return res.send({error:err.message});
});
const port = config.port || 3000;

app.listen(port, function () {
    var lineReader = require('readline').createInterface({
        input: require('fs').createReadStream('ascii.txt')
    });

    lineReader.on('line', function (line) {
        console.log(line);
    });

    setTimeout(function() {
        console.log("Listening on Port: " + port)
        console.log("Starting db...");

        require("./db/db.js").load();
    }, 1000);
});


module.exports = app;
