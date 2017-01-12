from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

## other app models
from user.models import User
from home.models import Poll
from .models import Article, ArticleReaction, ArticleComment, Topic, TopicFollower

## custom packages
import device
from common import post_required, login_required, redirect_if_loggedin, __redirect

## debug
from pprint import pprint
# Create your views here.


def polls_view(request):
	data = {'title':'Polls', 'page':'post'}
	polls = Poll.get_user_polls(request.user)
	data.update({'polls': polls})
	template = device.get_template(request, 'post_polls.html')
	return render(request, template, data)

def petitions_view(request):
	data = {'title':'Petitions', 'page':'post'}
	#polls = Petition.get_user_petitions(request.user)
	#data.update({'polls': polls})
	template = device.get_template(request, 'post_petitions.html')
	return render(request, template, data)

@login_required
def new_post_view(request):
	data = {'title':'New Topic', 'page':'post'}
	template = device.get_template(request, 'post_new_topic.html')
	return render(request, template, data)

@post_required
@login_required
def create_post(request):
	pprint(request)
	error = None
	post = None
	post_type = request.POST.get('post_type', '-1')
	title = request.POST.get('post_title', '').strip(' \t\n\r')
	text = request.POST.get('post_text', '').strip(' \t\n\r')
	if title == '' or text == '':
		error = 'Title , Abstract cannot be empty'
	else:
		#try:
		if post_type == '1':
			post = Article.create(request.user, title, text)
		elif post_type == '2':
			post = Poll.create(request.user, title, text)
		elif post_type == '3':
			#topic = Petition.create(request.user, title, text)
			error = 'Not supported yet'
		else:
			error = 'Invalid topic category'

		#except ValueError as e:
		#	print('ValueError : '+ str(e))
		#except:
		#	print('Unknown error')

	## send the response
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':204, 'message': 'published'})
		else:
			return JsonResponse({'status':401, 'message': error})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)


@csrf_exempt
@post_required
@login_required
def update_post(request):
	pprint(request)
	error = None
	post = None
	post_type = int(request.POST.get('post_type', -1))
	post_id = int(request.POST.get('post_id', -1))
	title = request.POST.get('post_title', '').strip(' \t\n\r')
	text = request.POST.get('post_text', '').strip(' \t\n\r')
	if post_type == -1 or post_id == -1:
		error = 'Bad request'
	elif title == '' or text == '':
		error = 'Topic title or abstract cannot be empty'
	else:
		#try:
		updatedObj = None
		if post_type == 1:
			updatedObj = Article.update(request.user, post_id, title, text)
			if updatedObj == None:
				error = 'Failed to update'
			else:
				post = {'post_title': updatedObj.title, 'post_text': updatedObj.text}
		elif post_type == 2:
			updatedObj = Poll.update(request.user, title, text)
			error = 'Failed to update poll'
		elif post_type == 3:
			#topic = Petition.remove(request.user, title, text)
			error = 'Not supported yet'
		else:
			error = 'Invalid topic category'

		#except ValueError as e:
		#	print('ValueError : '+ str(e))
		#except:
		#	print('Unknown error')

	## send the response
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':200, 'message': 'success', 'data': post})
		else:
			return JsonResponse({'status':401, 'error': error})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)


@csrf_exempt
@post_required
@login_required
def delete_post(request):
	pprint(request)
	error = None
	post_type = int(request.POST.get('post_type', -1))
	post_id = int(request.POST.get('post_id', -1))
	if topic_type == -1 or topic_id == -1:
		error = 'Bad request'
	else:
		#try:
		if post_type == 1:
			if Article.remove(request.user, post_id) == False:
				error = 'Failed to delete'
		elif post_type == 2:
			topic = Poll.remove(request.user, title, text)
		elif post_type == 3:
			#topic = Petition.remove(request.user, title, text)
			error = 'Not supported yet'
		else:
			error = 'Invalid topic category'

		#except ValueError as e:
		#	print('ValueError : '+ str(e))
		#except:
		#	print('Unknown error')

	## send the response
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':204, 'message': 'deleted'})
		else:
			return JsonResponse({'status':401, 'message': error})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)


@csrf_exempt
@login_required
def create_post_comment(request):
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
			return JsonResponse({'status':200, 'message': 'success', 'data':data})
		else:
			return JsonResponse({'status':401, 'error': error})
	else:
		if error == None:	
			return __redirect(request, settings.HOME_PAGE_URL)
		else:
			return __redirect(register, settings.HOME_PAGE_URL)

@csrf_exempt
@login_required
def create_reply_comment(request):
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
		return JsonResponse({'status':200, 'message': 'success', 'data': data})
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
		return JsonResponse({'status':200, 'message': 'success', 'data': data})
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