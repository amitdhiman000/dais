
function searchKey(key)
{
	if (key == "") {
		$("#search_results").text("");
		$("#search_results").fadeOut('fast');
		return;
	}

	var data = 'key=' + encodeURIComponent(key);
	$.ajax({
		url: "ajax/search",
		type: "GET",
		data: data,
		contentType: "text/html",
		cache: false,
		success: function (html) {
			//$('.loading').hide();
			$('#search_results').html(html);
			$('#search_results').fadeIn('fast');
			//$('#body').fadeIn('slow');
		},
		error: function(){ alert("error"); }
	});
}



var storedHash = window.location.hash;

if ("onhashchange" in window) {
	// register the hash change callback.
	window.onhashchange = function () {
        hashChanged(window.location.hash);
    }
} else {
//older mechnism or ask to install latest browser.
window.setInterval(function () {
    if (window.location.hash != storedHash) {
        storedHash = window.location.hash;
        hashChanged(storedHash);
    }
}, 100);
}

function hashChanged(storedHash)
{
	loadPage(window.location.href);
}

function loadPage(url)
{
	console.log("url : "+url);
	return;
	var data = 'hash=' + encodeURIComponent(url);
	$.ajax({
		url: "ajax/loader",
		type: "GET",
		data: data,
		contentType: "text/html",
		cache: false,
		success: function (html) {
			$('.loading').hide();
			$('#content').html(html);
			$('#body').fadeIn('slow');
		},
		error: function(){ alert("error"); }
	});
}