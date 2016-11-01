
function doSearch(key)
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
