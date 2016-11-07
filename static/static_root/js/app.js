$(document).on('pageinit', '#topicsaddpage', function() {
    $(document).on('click', '#submit', function(event) {
        event.preventDefault();
        if(0 === $('#title').val().length && 0 === $('#text').val().length){
            alert('Please fill the values');
            return;
        }
        show_toast('form submitted');
        // Send data to server through the Ajax call
        // action is functionality we want to call and outputJSON is our data
        var form = $(this).parents('form');
        var formAction = form.attr('action');
        var csrftoken = form.find('input[name="csrfmiddlewaretoken"]').val();
        console.log('action : '+ formAction);
        console.log('csrftoken : '+ csrftoken);
        $.ajax({url: formAction,
            data: {action : formAction, formData : form.serialize()},
            type: 'POST',
            async: 'true',
            dataType: 'json',
            beforeSend: function(xhr) {
                console.log('beforeSend');
                console.log(cookie.get('csrftoken'));
                $.mobile.loading('show'); // This will show ajax spinner
                xhr.setRequestHeader('X-CSRFToken', cookie.get('csrftoken'));
            },
            complete: function(response) {
                // This function is called at last for cleanup
                console.log('comeplete :'+ response.status);
                $.mobile.loading('hide'); // This will hide ajax spinner
                switch(response.status) {
                case 201:
                    show_toast('user not found');
                    break;
                case 302:
                    show_toast('redirect request');
                    //location.href = response.getResponseHeader("Location");
                    break;
                default:
                    break;
                    // notihng
                }
                console.log('complete done!!');
            },
            success: function (data) {
                console.log('success');
            },
            error: function (xhr,error) {
                console.log('error : '+ error + ', status : '+xhr.status);
                show_toast('Network Error occured');
            }
        });
        //return false; // cancel original event to prevent form submitting
    });
});

var cookie = {
get: function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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