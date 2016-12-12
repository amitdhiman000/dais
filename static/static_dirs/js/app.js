$(document).on('pagecontainerbeforeshow', function() {
	console.log('enhance the page');
	//$(this).enhanceWithin();
});


$(document).on('pageinit', function() {
	/********* Unregister all callbacks **********/
	$(document).off('keyup', '#search');
	$(document).off('click', '.user-reaction');
	$(document).off('click', '.user-comment-link');
	$(document).off('click', '.user-comment-submit');
	$(document).off('click', '.submit');

	/********** Register the callbacks ***********/
	$(document).on('keyup', '#search', doSearch);
	$(document).on('click', '.user-reaction', userReaction);
	$(document).on('click', '.user-comment-link', userComment);
	$(document).on('click', '.user-comment-submit', userCommentSubmit);
	$(document).on('click', '.submit', function(e) {
		e.preventDefault();
		/*
		if(0 === $('#title').val().length || 0 === $('#text').val().length){
			show_toast('Please fill the credentials');
			return;
		}
		*/

		var form = $(this).parents('form');
		var formAction = form.attr('action');
		console.log('action : '+ formAction);
		$.ajax({url: formAction,
			data: form.serialize(),
			type: 'POST',
			async: 'true',
			dataType: 'text', // xml, html, json, jsonp, text //
			beforeSend: function(xhr) {
				console.log('beforeSend');
				$.mobile.loading('show');
			},
			complete: function(response) {
				// This function is called at last for cleanup
				console.log('comeplete :'+ response.status);
				$.mobile.loading('hide');
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
					case 200:
						//console.log(jsonData.message);
						Toast.show(jsonData.message);
						break;
					case 204:
						Toast.show(jsonData.message);
						Toast.show('Done');
						break;
					default:
						console.log(jsonData.message);
						Toast.show(jsonData.message);
						break;
					}
				} else if (mimeType.indexOf('html') > -1) {
					// handle html data
				}
			},
			error: function (xhr,error) {
				console.log('error : '+ error + ', status : '+xhr.status);
				Toast.show('Network Error occured');
			}
		});
	});
});

function doSearch()
{
	console.log('doSearch');
	var key = $(this).val();
	var list = $('#search-results');
	if ('' === key) {
		list.hide();
		return;
	}

	$.ajax({url: '/ajax/search/',
		data: key,
		type: 'POST',
		async: 'true',
		dataType: 'text',
		success: function (data, status, xhr) {
			console.log('success : ' + data);
			var item = null;
			list.empty();
			jsonData = jQuery.parseJSON(data).text;
			for (i = 0; i < jsonData.length; ++i) {
				item = '<li data-filtertext="'+ jsonData[i] +'"><a href="#">'+ jsonData[i] +'</a></li>';
				list.append(item);
			}
			list.show();
			list.listview('refresh');
		}
	});
}

function userReaction()
{
	var pThis = $(this);
	var reaction = pThis.text();
	var article_id = pThis.parents('.user-reaction-div').attr('article-id');
	console.log('user reaction : '+ reaction);
	$.ajax({url: '/user/post/reaction/',
		data: {user_reaction:reaction, article_id:article_id},
		type: 'POST',
		async: 'true',
		dataType: 'text',
		success: function (data, status, xhr) {
			mimeType = xhr.getResponseHeader("content-type");
			if (mimeType.indexOf('json') > -1) {
				console.log('success : ' + data);
				jsonData = jQuery.parseJSON(data);
				switch(jsonData.status) {
				case 302:
					location.href = jsonData.url;
					break;
				case 200:
					var count = 0;
					var other = null;
					switch(reaction) {
					case 'like':
						count = parseInt(pThis.attr('article-likes')) + 1;
						pThis.attr('article-likes', count);
						pThis.text('liked');
						pThis.next().text('['+count+']');
						other = pThis.parent().next();
						resetDislike(other);
						pThis.parent().attr('dais-active', 'true');
						break;
					case 'dislike':
						count = parseInt(pThis.attr('article-dislikes')) + 1;
						pThis.attr('article-dislikes', count);
						pThis.text('disliked');
						pThis.next().text('['+count+']');
						other = pThis.parent().prev();
						resetLike(other);
						pThis.parent().attr('dais-active', 'true');
						break;
					case 'liked':
						resetLike(pThis.parent());
						break;
					case 'disliked':
						resetDislike(pThis.parent());
						break;
					default:
						break;
					}
				default:
					Toast.show('message : '+jsonData.message);
					break;
				}
			} else if (mimeType.indexOf('html') > -1) {
				// handle html data
			}
		}
	});
}

function resetLike(obj)
{
	console.log('resetLike');
	if (obj.attr('dais-active') === 'true') {
		var likeObj = obj.children('.user-reaction');
		var count = parseInt(likeObj.attr('article-likes')) - 1;
		likeObj.attr('article-likes', count);
		likeObj.next().text((count>0)?'['+count+']':'');
		likeObj.text('like');
		obj.attr('dais-active', 'false');
		console.log('resetLike Done');
	}
}

function resetDislike(obj)
{
	console.log('resetDislike');
	if (obj.attr('dais-active') === 'true') {
		var likeObj = obj.children('.user-reaction');
		var count = parseInt(likeObj.attr('article-dislikes')) - 1;
		likeObj.attr('article-dislikes', count);
		likeObj.next().text((count>0)?'['+count+']':'');
		likeObj.text('dislike');
		obj.attr('dais-active', 'false');
		console.log('resetDislike Done');
	}
}

function userComment()
{
	var cw = $(this).next('.user-comments-wid');
	if (cw.exists()) {
		console.log("hiding comment widget");
		console.log("length : "+ cw.length);
		console.log("name : "+ cw.prop('tagName'));
		(cw.is(":visible"))?cw.hide():cw.show();
	} else {
		console.log("creating comment widget");
		var article_id = $(this).parents('.user-reaction-div').attr('article-id');
		var xx = $('#user-comments-wid').clone().removeAttr('id');
		xx.find('#article_id').val(article_id);
		xx.insertAfter($(this)).show();
		loadPostComments(xx.find('.user-comments'), article_id, 0, 10);
	}
}

function loadPostComments(pThis, art_id, s, c)
{
	console.log('loadPostComments');
	$.ajax({url: '/user/load/post-comments/',
		data: {'article_id':art_id, 'comment_start':0, 'comment_count':5},
		type: 'POST',
		async: 'true',
		dataType: 'text',
		success: function (data, status, xhr) {
			mimeType = xhr.getResponseHeader("content-type");
			if (mimeType.indexOf('json') > -1) {
				console.log('success : ' + data);
				jsonData = jQuery.parseJSON(data);
				switch(jsonData.status) {
				case 302:
					location.href = jsonData.url;
					break;
				case 200:
				console.log('200');
					//Toast.show(jsonData.message);
					console.log(jsonData.comments);
					publishComments(pThis, jsonData.comments);
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
			Toast.show('Network Error occured');
		}
	});
}

function publishComments(pThis, cmts)
{
	console.log('publishComments');
	var html = '';
	var cmt = null;
	for (i = 0; i < cmts.length; ++i) {
		cmt = cmts[i];
		html += '<div class ="user-comment" comment-id="'+cmt.id+'" >'
		+ '<div class="user-name" > <strong>' + cmt.author__email + '</strong></div>'
		+ '<div class="comment-text" >' + cmt.text + '</div>'
		+ '<div class="h-bar" ></div>'
		+ '</div>';
	}

	pThis.html(html).show();
}

function userCommentSubmit(e)
{
	e.preventDefault();
	var pThis = $(this);
	var form = pThis.parents('form');
	var formAction = form.attr('action');
	console.log('action : '+ formAction);
	$.ajax({url: formAction,
		data: form.serialize(),
		type: 'POST',
		async: 'true',
		dataType: 'text',
		success: function (data, status, xhr) {
			mimeType = xhr.getResponseHeader("content-type");
			if (mimeType.indexOf('json') > -1) {
				console.log('success : ' + data);
				jsonData = jQuery.parseJSON(data);
				switch(jsonData.status) {
				case 302:
					console.log('redirect');
					location.href = jsonData.url;
					break;
				case 200:
				console.log('200');
					Toast.show(jsonData.message);
					break;
				case 204:
				console.log('204');
					Toast.show('Done');
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
			Toast.show('Network Error occured');
		}
	});
}


/****************** Exteded Jquery *******************/
jQuery.fn.exists = function(){return this.length>0;}
/****************** Toast API ************************/
var Toast =  {
show: function(text='Error', timeout=1200) {
	//$('.toast').text(text).fadeIn(500).delay(timeout).fadeOut(500);
	$('.toast').fadeIn({duration: 500, start: function() {$(this).text(text);}}).delay(timeout).fadeOut(500);
},
hide: function() {
	$('.toast').hide();
}
};

/****************** cookie API ***********************/
var Cookie = {
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