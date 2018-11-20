const readline = require("readline");

module.exports = function(port, database, userdatabase) {
    console.log("Shortnex v2.0beta - Made with <3 in Germany by lordjbs");

    setTimeout(function() {
        console.log("Listening on Port: " + port)
        console.log("Starting db...");

        database.load(function(response) {
            console.log(response);
        });

        userdatabase.load(function(response) {
            console.log(response);
        });
    }, 1000);
}