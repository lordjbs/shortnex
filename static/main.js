/*
# shortnex v2.0
# made by jbs (https://github.com/lordjbs/)
# Copyright (C) 2018-2020 jbs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

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
    const keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        shorten();
    }
});