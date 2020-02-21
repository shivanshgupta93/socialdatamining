
var fb_id;

$(document).ready(() => {
    setInterval(function(){ reload_page(); },5000);
    $.get("/api/user", (user, err) => {
        if (err !== "success") console.error(err);
        if (user && Array.isArray(user.data)) {
            var username_array = [...new Set(user.data.map(user => user.fb_name))]
            var fbid_array = [...new Set(user.data.map(user => user.fb_id))]
            const login_container = document.querySelector(".loginname")
            var login_name = username_array[0]
            fb_id = fbid_array[0]
            login_container.innerText = "WELCOME " + login_name.toUpperCase()
        }
    $.get("/api/facebook/" + fb_id, (facebook, err) =>{
        if (err !== "success") console.error(err);
        if (facebook && Array.isArray(facebook.data)) {
            var post = '';
            facebook_data = sortByKeyDesc(facebook.data, 'created_time')
            for (var i=0; i<facebook_data.length; i++)
            {
                var url_li = '';
                if (facebook_data[i]['attach_url'] != 'None')
                {
                   url_li = '<li> Url: <a href="' + facebook_data[i]['attach_url']+ '">Attachment</a></li>'
                }
                if(facebook_data[i]['attach_url'] == 'None')
                {
                    url_li = '<li> Url: None</li>'
                }
                post = post + '<div class="innerpost"><ul>'
                            +'<li> Create Date: ' + (facebook_data[i]['created_time'].substring(0,facebook_data[i]['created_time'].indexOf('+'))).replace('T',' ') + '</li>'
                            +'<li> Status Type: ' + (facebook_data[i]['status_type'].split('_').join(' ')).replace(/\b\w/g, function(l){ return l.toUpperCase() }) + '</li>'
                            +'<li> Caption: ' + facebook_data[i]['caption'] + '</li>'
                            +'<li> Message: ' + facebook_data[i]['message'] + '</li>'
                            +'<li> Story: ' + facebook_data[i]['story'] + '</li>'
                            +'<li> Description: ' + facebook_data[i]['description'] + '</li>'
                            +'<li> Type: ' + facebook_data[i]['type'].replace(/\b\w/g, function(l){ return l.toUpperCase() }) + '</li>'
                            +'<li> Attachement: <div><ul>' 
                                +'<li> Title: ' + facebook_data[i]['attach_title']+ '</li>'
                                +'<li> Type: ' + (facebook_data[i]['attach_type'].split('_').join(' ')).replace(/\b\w/g, function(l){ return l.toUpperCase() })+ '</li>'
                                + url_li
                                +'<li> Description: ' + facebook_data[i]['attach_description']+ '</li>'
                                +'</ul></div></li>'
                            +'</ul></div>'
            }
            $(".posts").append(post)
        }
    })
})
});

function sortByKeyDesc(array, key) {
    return array.sort(function (a, b) {
        var x = a[key]; var y = b[key];
        return ((x > y) ? -1 : ((x < y) ? 1 : 0));
    });
}

function sortByKeyAsc(array, key) {
    return array.sort(function (a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}

function reload_page()
 {
    window.location.reload(true);
 }