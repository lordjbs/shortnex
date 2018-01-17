$('#shorten')
    .ajaxForm({
        url : '/shorten?url=' + document.getElementById("url").value, // or whatever
        dataType : 'json',
        success : function (response) {
            alert("The server says: " + response);
        }
    })
;