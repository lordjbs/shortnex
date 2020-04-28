var istokenactive = false;

function pressed() {
    addTokenToURL(function(token) {
        $.ajax({
            //url: "/shorten?url=" + document.getElementById("url").value + token,
            url: "/shorten",
            type: "POST",
            data: JSON.stringify({"url": document.getElementById("url").value}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                console.log(data)
                if (data.success !== true) {
                    console.log(data)
                    switch (data.code) {
                        case 0:
                            setText("Database Error. (Error Code: 0)");
                            break;
                        case 1:
                            setText("The URL is invalid. (Error Code: 1)");
                            break;
                        case 2:
                            setText("The URL is \"undefined\"! (Error Code: 2)");
                            break;
                        case 3:
                            setText("The Usersystem encountered an Error. Check Logs. (Error Code: 3)");
                            break;
                        case 4:
                            setText("You don't have Permissions to do that. (Error Code: 4)");
                            break;
                        case 5:
                            setText("This URL is not in the Database. (Error Code: 5)");
                            break;
                        case 6:
                            setText("Unexpected User Database Error (Error Code: 6)");
                            break;
                        default:
                            setText("Unable to shorten URL (Unknown Error -> Switch Default)");
                            break;
                    }
                } else {
                    setText("Shortened URL: http://" + data.url + "/" + data.id);
                }
            }
        });
    });
}


function checkTokensystem(func) {
    $.ajax({
        url: "/check/tokensystem",
        type: "GET",
        success: function(data) {
            if (data.active) addTokenbar(true);
            else addTokenbar(false);
            return func(data.active);
        }
    });
}

function setText(Text) {
    document.getElementById("u").innerHTML = Text;
}

function addTokenbar(boolean) {
    if (boolean) {
        istokenactive = true;
        document.getElementById("tokenholder").style.visibility = 'visible';
    } else {
        istokenactive = false;
        document.getElementById("tokenholder").style.visibility = 'hidden';



    }
}

function registerColor() {
    var e = Cookies.get("color");

    if (e == "#282c34") {
        setColor(false);
    } else {
        setColor(true);
    }
}

function addTokenToURL(func) {
    var string = "&token=" + document.getElementById("token").value;
    if (addTokenToURL) {
        func(string);
    } else {
        func("");
    }
}

function setColor(bool) {
    if (bool) {
        Cookies.set("color", "#282c34");
    } else if (!bool) {
        Cookies.set("color", "#ffffff");
    } else {
        Cookies.set("color", "#ffffff");
    }

    updateColor(Cookies.get("color"));
}

function updateColor(hex) {
    const obj = document.getElementById("main");
    if (hex == "#282c34") {
        document.body.style.background = "#282c34";
        document.body.style.color = "#ffffff";
        obj.style = "background-color: #282c34; color: white;";
    } else if (hex == "#ffffff") {
        document.body.style.background = "#ffffff";
        document.body.style.color = "#ffffff";
        obj.style = "background-color: #ffffff; color: black;";
    }
}

$("#re").click(function() {
    var e = Cookies.get("color");
    console.log("click clock");
    if (e !== "#282c34") {
        setColor(true);
    } else {
        setColor(false);
    }
});

window.onload = function() {
    var e = Cookies.get("color");

    if (e == "#282c34") {
        setColor(true);
    } else {
        setColor(false);
    }
    checkTokensystem(function(active) {
        console.log(active);
    });
}