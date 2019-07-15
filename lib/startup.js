const readline = require("readline");
const util = require("../lib/util.js");

module.exports = function(port, database) {
    console.log("Shortnex " + util.version + " - Made with <3 in Germany by jbs");

    setTimeout(function() {
        console.log("Listening on Port: " + port)
        console.log("Testing database...");
        database.test(function(bool) {
            if(bool){
                console.log("Successfully tested the database");
             } else {
                  console.log("Something is not right with the database. Please look at the database, or contact administrator.");
                  process.exit(0);
            }
        });

        console.log("Successful start!");

    }, 1000);
}