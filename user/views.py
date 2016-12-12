from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

## custom packages
from device import get_template
from common import redirect_if_loggedin, login_required, __redirect
## custom authentication
from .models import User, Article, ArticleReaction, ArticleComment, Topic
from .control import UserRegControl
from . import backends as auth

## debugging
from pprint import pprint

# Create your views here.

@redirect_if_loggedin
def signin_view(request):
	data = {'title':'Login', 'page':'user'}
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	data.update(csrf(request))
	file = get_template(request, 'user_signin.html')
	return render(request, file, data)

#functions for registration
def signup_view(request):
	data = {'title':'Signup', 'page':'user'}
	data.update(csrf(request))
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	file = get_template(request, 'user_signup.html')
	return render(request, file, data)

def signout(request):
	auth.logout(request)
	return __redirect(request, settings.USER_LOGIN_URL)


def signin_auth(request):
	pprint(request.POST)
	if request.method == 'POST':
		username = request.POST.get('email', '')
		password = request.POST.get('pass', '')
		user = auth.auth_user(username=username, password=password)

		if user is not None:
			pprint(vars(user))
			auth.login(request, user)
			#request.session.set_expiry(10)
			return __redirect(request, settings.USER_PROFILE_URL)
		else:
			form_errors = {'user':'*Email or password is wrong!!'}
			form_values = {'user':request.POST.get('user', '')}
			request.session['form_errors'] = form_errors
			request.session['form_values'] = form_values
			return __redirect(request, settings.USER_LOGIN_URL)
		return __redirect(request, settings.INVALID_REQUEST_URL)

def signup_register(request):
	data = {'title':'SignUp Successful', 'page':'user'}
	if request.method == 'POST':
		control = None
		control = UserRegControl(request.POST)
		if control is not None:
			if control.validate():
				user = control.register()
				print('registration successful')
				auth.login(request, user)
				if request.is_ajax():
					return __redirect(request, settings.USER_SIGNUP_SUCCESS_URL)
				else:
					file = get_template(request, 'user_registered.html')
					return render(request, file, data)
			else:
				pprint(control.get_errors());
				request.session['form_errors'] = control.get_errors()
				request.session['form_values'] = control.get_values()
				return __redirect(request, settings.USER_SIGNUP_URL)
	return __redirect(request, settings.INVALID_REQUEST_URL)


@login_required
def signup_success_view(request):
	print('registration success')
	data = {'title':'Signup :: Success', 'page':'user'}
	file = get_template(request, 'user_registered.html');
	return render(request, file, data)

@login_required
def profile_view(request):
	print('profile')
	data = {'title':'Profile', 'page':'user'}
	file = get_template(request, 'user_profile.html');
	return render(request, file, data)


def invalid_view(request):
	data = {'title': 'Invalid'};
#	return HttpResponse ('This is Invalid Request')
	file = get_template(request, 'invalid.html')
	return render(request, file, data)


##
## User personal and profile info
##

def user_info_view(request):
	return profile_view(request);

def user_topics_select_view(request):
	data = {'title': 'Follow Topics', 'page':'user'};
	topics = Topic.get_topics(request.user)
	data.update({'topics':topics})
	file = get_template(request, 'user_topics_select.html')
	return render(request, file, data)

def user_topic_selected(request):
	pass

def user_mails_view(request):
	data = {'title': 'User mails', 'page':'user'};
	file = get_template(request, 'user_mails.html')
	return render(request, file, data)

def user_stats_view(request):
	data = {'title': 'User stats', 'page':'user'};
	file = get_template(request, 'user_stats.html')
	return render(request, file, data)

def user_settings_view(request):
	data = {'title': 'User settings', 'page':'user'};
	file = get_template(request, 'user_settings.html')
	return render(request, file, data)


##
## User topic add functionality
##

@login_required
def post_add(request):
	pprint(request.POST)
	title = request.POST.get('title', None)
	text = request.POST.get('text', None)
	try:
		article = Article.create(request.user, title, text)
	except ValueError as e:
		print('ValueError : '+ str(e))
	except:
		print('Unknown error')

	## send the response
	if request.is_ajax():
		return JsonResponse({'status':200, 'message': 'published'})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)

@csrf_exempt
@login_required
def post_comment(request):
	pprint(request.POST)
	#try:
	article_id = request.POST.get('article_id', '')
	text = request.POST.get('comment', '')
	article = Article.get_article(article_id)
	user = request.user
	ArticleComment.create(article, user, text)

	if request.is_ajax():
		return JsonResponse({'status':200, 'message': 'success'})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)

@csrf_exempt
@login_required
def reply_comment(request):
	pprint(request.POST)
	#try:
	comment_id = request.POST.get('comment_id', '')
	text = request.POST.get('comment', '')
	comment = CommentReply.get_comment(comment_id)
	user = request.user
	ReplyComment.create(comment, user, text)

	if request.is_ajax():
		return JsonResponse({'status':200, 'message': 'success'})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)


## Load reply and comments
##

@csrf_exempt
@login_required
def load_post_comments(request):
	pprint(request.POST)
	#try:
	article_id = request.POST.get('article_id', -1)
	start = int(request.POST.get('comment_start', 0))
	count = int(request.POST.get('comment_count', 5))
	if start < 0:
		start = 0
	if count < 0 or count > 10:
		count = 10
	objs = ArticleComment.get_comments(article_id, start, count)

	pprint(objs)

	data = list(objs)
	if request.is_ajax():
		return JsonResponse({'status':200, 'message': 'success', 'comments': data})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)

@csrf_exempt
@login_required
def load_reply_comments(request):
	pprint(request.POST)
	#try:
	comment_id = request.POST.get('comment_id', -1)
	start = int(request.POST.get('comment_start', 0))
	count = int(request.POST.get('comment_count', 5))
	if start < 0:
		start = 0
	if count < 0 or count > 10:
		count = 10
	
	objs = ReplyComment.get_comments(comment_id, start, count)
	data = serializers.serialize('json', [objs,])

	if request.is_ajax():
		return JsonResponse({'status':200, 'message': 'success', 'comments': data})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)


## User Reactions handling.
##

@csrf_exempt
@login_required
def post_reaction(request):
	result = 'error'

	#try:
	reaction = request.POST.get('user_reaction', 'like')
	article_id = request.POST.get('article_id', -1)
	article = Article.get_article(article_id)
	user = request.user
	if reaction == 'like':
		ArticleReaction.like(user, article)
		result = 'liked'
	elif reaction == 'dislike':
		ArticleReaction.dislike(user, article)
		result = 'disliked'
	elif reaction == 'liked':
		ArticleReaction.remove(user, article)
		result = 'like canceled'
	elif reaction == 'disliked':
		ArticleReaction.remove(user, article)
		result = 'dislike canceled'

	if request.is_ajax():
		return JsonResponse({'status':200, 'message': result})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)

@csrf_exempt
@login_required
def post_comment_reaction(request):
	result = 'error'

	#try:
	reaction = request.POST.get('user_reaction', 'like')
	comment_id = request.POST.get('comment_id', -1)
	comment = ArticleComment.get_article(comment_id)
	user = request.user
	if reaction == 'like':
		ArticleCommentReaction.like(user, comment)
		result = 'liked'
	elif reaction == 'dislike':
		ArticleCommentReaction.dislike(user, comment)
		result = 'disliked'
	elif reaction == 'liked':
		ArticleCommentReaction.remove(user, comment)
		result = 'like canceled'
	elif reaction == 'disliked':
		ArticleCommentReaction.remove(user, comment)
		result = 'dislike canceled'

	if request.is_ajax():
		return JsonResponse({'status':200, 'message': result})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)

@csrf_exempt
@login_required
def reply_comment_reaction(request):
	result = 'error'

	#try:
	reaction = request.POST.get('user_reaction', 'like')
	comment_id = request.POST.get('comment_id', -1)
	comment = ReplyComment.get_comment(comment_id)
	user = request.user
	if reaction == 'like':
		ReplyCommentReaction.like(user, comment)
		result = 'liked'
	elif reaction == 'dislike':
		ReplyCommentReaction.dislike(user, comment)
		result = 'disliked'
	elif reaction == 'liked':
		ReplyCommentReaction.remove(user, comment)
		result = 'like canceled'
	elif reaction == 'disliked':
		ReplyCommentReaction.remove(user, comment)
		result = 'dislike canceled'

	if request.is_ajax():
		return JsonResponse({'status':200, 'message': result})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)