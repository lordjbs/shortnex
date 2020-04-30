var lastURL = "";

function shorten() {
    if(document.getElementById("urlinput").value == lastURL) {
        return setInput("Hey, you already tried that.")
    }
    $.ajax({
        url: "/shorten",
        type: "POST",
        data: JSON.stringify({url:document.getElementById("urlinput").value}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: (data) => {
            if(!data.success) {
                setInput(data.error)
            } else {
                const baseURL = data.url;
                setInput(`${baseURL}/${data.id}`)
            }
        }
    });
    lastURL = document.getElementById("urlinput").value;
}

function setInput(text) {
    document.getElementById("urlinput").value = text;
}

$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        shorten();
    }
});