/**
 * Ratelimites. Greetings go to ratelimited.me!
 */

 var ips = {};
 const conf = require("../conf.json");
 const util = require("./util.js");

 const modules = {
     request: function(req, res, next) {
         if(!conf.ratelimit.enabled) {
             next();
         }

         var ip;

         if(!conf.requestThroughProxy) {
            ip = req.connection.remoteAddress;
         } else {
             ip = request.headers['x-forwarded-for'];
         }

         if(!ips[ip]) {
             ips[ip] = 1;
         } else {
             ips[ip] += 1;
         }

         if(ips[ip] > conf.ratelimit.requests) {
             console.log("WARNING! " + ip + " is sending more requests than allowed. Requests send in interval \"" + conf.ratelimit.interval + "\": " + ips[ip]);
             res.status(429);
             return res.send({error:429, message:"You have been ratelimited."});
         } else {
             next();
         }
         
     },
     start: function() {
         setInterval(function() {
             ips = {};
         }, conf.ratelimit.interval);
     }
 }

 module.exports = modules;
