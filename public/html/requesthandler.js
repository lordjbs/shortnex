var istokenactive = false;

function pressed() {
  addTokenToURL(function(token) {
    $.ajax({url: "/shorten?url=" + document.getElementById("url").value + token,type: "GET",success: function(data){
      if(data.success !== true) {
          switch(data.code) {
            case 0:
              setText("Unable to shorten URL. (Error Code: 0 -> Database Error)");
              break;
            case 1:
              setText("Unable to shorten URL. (Error Code: 1 -> The URL is invalid.)");
              break;
            case 2:
              setText("Unable to shorten URL. (Error Code: 2 -> The URL is \"undefined\"!)");
              break;
            default:
              setText("Unable to shorten URL (Unknown Error -> Switch Default)");
             break;
          }
      } else {
        setText("Shortened URL: http://" + data.url + "/?" + data.id);
      }
    }});
  });
}



function checkTokensystem(func) {
  $.ajax({url: "/check/tokensystem",type: "GET",success: function(data){
    if(data.active) addTokenbar(true); else addTokenbar(false);
    return func(data.active);
  }});
}

function setText(Text) {
    document.getElementById("u").innerHTML = Text;
}

function addTokenbar(boolean) {
  if(boolean) {
    istokenactive = true;
    document.getElementById("tokenholder").style.visibility='visible';
  } else {
    istokenactive = false;      document.getElementById("tokenholder").style.visibility='hidden';
      document.getElementById("shortenz").style.top='-90px';


  }
}

function registerColor() {
  var e = Cookies.get("color");
  
  if(e == "#282c34") {
    setColor(false);
  } else {
    setColor(true);
  }
}

function addTokenToURL(func) {
  var string = "&token=" + document.getElementById("token").value;
  if(addTokenToURL) {
    func(string);
  } else {
    func("");
  }
}

function setColor(bool) {
  if(bool) {
    Cookies.set("color", "#282c34");
  } else if(!bool) {
    Cookies.set("color", "#ffffff");
  } else {
    Cookies.set("color", "#ffffff");
  }

  updateColor(Cookies.get("color"));
}

function updateColor(hex) {
  const obj = document.getElementById("main");
  if(hex == "#282c34") {
    obj.style = "background-color: #282c34; color: white;";
  }else if(hex == "#ffffff") {
    obj.style = "background-color: #ffffff; color: black;";
  }
}

$( "#re" ).click(function() {
  var e = Cookies.get("color");
  console.log("click clock");
  if(e !== "#282c34") {
    setColor(true);
  } else {
    setColor(false);
  }
});

window.onload = function() {
  var e = Cookies.get("color");
  
  if(e == "#282c34") {
    setColor(true);
  } else {
    setColor(false);
  }
  checkTokensystem(function(active) {
    console.log(active);
  });
}