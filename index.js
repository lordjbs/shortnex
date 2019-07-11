/**
 *   ____  _                _
 * / ___|| |__   ___  _ __| |_ _ __   _____  __
 * \___ \| "_ \ / _ \| "__| __| "_ \ / _ \ \/ /
 *  ___) | | | | (_) | |  | |_| | | |  __/>  <
 * |____/|_| |_|\___/|_|   \__|_| |_|\___/_/\_\
 *
 * Shortnex v2.0beta
 * @author lordjbs
 * @requires nodejs9
*/

const express = require("express");
const path = require("path");
const logger = require("morgan");
const bodyParser = require("body-parser");
const config = require("./conf.json");
const database = require("./db/db.js");
const startup = require("./lib/startup.js");
const ratelimit = require("./lib/ratelimit.js");

const app = express();

if(config.devLog) {
    app.use(logger("dev"));
} else {
    app.use(logger("default"));
}

app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use(function(req,res,next) {ratelimit.request(req,res,next);});

app.use("/", require("./routes/index.js"));
app.use("/user/create", require("./routes/user/create.js"));
app.use("/user/delete", require("./routes/user/delete.js"));
app.use("/shorten", require("./routes/shorten.js"));
app.use("/check/tokensystem", require("./routes/tokenactive.js"));

app.use('/static', express.static('public/html/static'));


app.use(function(req, res, next) {
    const err = new Error("Not Found");
    err.status = 404;
    next(err);
});

app.use(function(err, req, res, next) {
    res.locals.message = err.message;
    res.locals.error = req.app.get("env") === "development" ? err : {};

    res.status(err.status || 500);
    return res.send({error:err.message});
});

const port =  process.env.PORT || config.port || 8080;

app.listen(port, function () {
    ratelimit.start();
    startup(port);

    if(!config.disclaimer.accept) {
        console.log("[shortnex] You have not accepted the Disclaimer. Look into the Config.\nThe Process will now automatically end.");
        process.exit(1);
    } 
});


module.exports = app;
