
var tw_id;

$(document).ready(() => {
    setInterval(function(){ reload_page(); },5000);
    $.get("/api/user", (user, err) => {
        if (err !== "success") console.error(err);
        if (user && Array.isArray(user.data)) {
            var username_array = [...new Set(user.data.map(user => user.tw_name))]
            var twid_array = [...new Set(user.data.map(user => user.tw_id))]
            const login_container = document.querySelector(".loginname")
            var login_name = username_array[0]
            tw_id = twid_array[0]
            login_container.innerText = "WELCOME " + login_name.toUpperCase()
        }
    $.get("/api/twitter/" + tw_id, (twitter, err) =>{
        if (err !== "success") console.error(err);
        if (twitter && Array.isArray(twitter.data)) {
            var post = '';
            var retweet = '';
            twitter_data = sortByKeyDesc(twitter.data, 'created_time')
            //twitter_data = twitter.data
            for (var i=0; i<twitter.data.length; i++)
            {
                var url_li = 'None'
                if(twitter_data[i]['retweet_count'] > 0)
                {
                    retweet = "Yes, Retweeted " + twitter_data[i]['retweet_count'] + " times"
                }
                if(twitter_data[i]['retweet_count'] == 0)
                {
                    retweet = "No"
                }

                if(twitter_data[i]['url'] != 'None')
                {
                   url_li = '<li> Url: <a href="' + twitter_data[i]['url']+ '">Tweet URL</a></li>'
                }
                if(twitter_data[i]['url'] == 'None')
                {
                   url_li = '<li> Url: None</li>'
                }
                post = post + '<div class="innerpost"><ul>'
                            +'<li> Create Date: ' + twitter_data[i]['created_time'] + '</li>'
                            +'<li> Tweet: ' + twitter_data[i]['text'] + '</li>'
                            +'<li> Retweet: ' + retweet + '</li>'
                            +'<li> Replied To: ' + twitter_data[i]['reply_user'] + '</li>'
                            + url_li
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