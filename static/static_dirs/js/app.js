$(document).on('pageinit', function() {
    $(document).on('click', '.submit', function(event) {
        event.preventDefault();
        if(0 === $('#title').val().length || 0 === $('#text').val().length){
            show_toast('Please fill the credentials');
            return;
        }
        //show_toast('form submitted');
        // Send data to server through the Ajax call
        // action is functionality we want to call and outputJSON is our data
        var form = $(this).parents('form');
        var formAction = form.attr('action');
        console.log('action : '+ formAction);
        $.ajax({url: formAction,
            data: form.serialize(),
            type: 'POST',
            async: 'true',
            dataType: 'text', /* xml, html, json, jsonp, text */
            beforeSend: function(xhr) {
                console.log('beforeSend');
                $.mobile.loading('show'); // This will show ajax spinner
            },
            complete: function(response) {
                // This function is called at last for cleanup
                console.log('comeplete :'+ response.status);
                $.mobile.loading('hide'); // This will hide ajax spinner
            },
            success: function (data, status, xhr) {
                mimeType = xhr.getResponseHeader("content-type");
                if (mimeType.indexOf('json') > -1) {
                    console.log('success : ' + data);
                    jsonData = jQuery.parseJSON(data);
                    switch(jsonData.status) {
                    case 302:
                        console.log('redirecting');
                        location.href = jsonData.url;
                        break;
                    case 204:
                        show_toast(jsonData.message);
                        break;
                    default:
                        break;
                    }
                } else if (mimeType.indexOf('html') > -1) {
                    // handle html data
                }
            },
            error: function (xhr,error) {
                console.log('error : '+ error + ', status : '+xhr.status);
                show_toast('Network Error occured');
            }
        });
    });
});

var cookie = {
get: function(name) {
    var cv = null;
    if (document.cookie != 'undefined' && document.cookie !== '') {
        var c = document.cookie.split(';');
        for (var i = 0; i < c.length; i++) {
            var c = jQuery.trim(c[i]);
            // Does this cookie string begin with the name we want?
            if (c.substring(0, name.length + 1) === (name + '=')) {
                cv = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cv;
},
set: function (cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
};

function show_toast(text='Some Error Occured!!')
{
    $('.toast').text(text).fadeIn(500).delay(2000).fadeOut(500);
}