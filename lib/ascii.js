const readline = require("readline");

module.exports = function(port, database) {
    const lineReader = readline.createInterface({input: require('fs').createReadStream(__dirname + '\\ascii.txt')});
    lineReader.on('line', function (line) {console.log(line);});

    setTimeout(function() {
        console.log("Listening on Port: " + port)
        console.log("Starting db...");

        database.load(function(response) {
            console.log(response);
        });
    }, 1000);
}