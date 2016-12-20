from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

## other app models
from user.models import User
from .models import Article, ArticleReaction, ArticleComment, Topic, TopicFollower

## custom packages
import device
from common import post_required, login_required, redirect_if_loggedin, __redirect

## debug
from pprint import pprint
# Create your views here.

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
	error = None
	data = None
	article_id = request.POST.get('article_id', -1)
	text = request.POST.get('comment', '')
	article = Article.get_article(article_id)
	user = request.user
	comment = ArticleComment.create(article, user, text)
	if comment == None:
		print('failed to post comment')
		error = 'failed to post comment'
	else:
		print('comment posted')
		data = {'id':comment.id, 'text':comment.text, 'author_name':comment.author_name}


	#from django.forms.models import model_to_dict
	#data = model_to_dict(comment)
	#pprint(data)
	
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':200, 'message': 'success', 'comment':data})
		else:
			return JsonResponse({'status':401, 'error': error})
	else:
		if error == None:	
			return __redirect(request, settings.HOME_PAGE_URL)
		else:
			return __redirect(register, settings.HOME_PAGE_URL)

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
	#pprint(objs)
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