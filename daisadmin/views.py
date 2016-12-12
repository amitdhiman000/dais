from django.shortcuts import render
from user.models import User, Article, ArticleReaction, ArticleComment, Topic
## custom packages
from device import get_template
from common import redirect_if_loggedin, login_required, __redirect

def index(request):
	data = {'title': 'Dais Admin', 'page':'user'};
	topics = Topic.get_topics(request.user)
	data.update({'topics':topics})
	file = get_template(request, 'admin_index.html')
	return render(request, file, data)

def topics_view(request):
	data = {'title': 'Follow Topics', 'page':'user'};
	topics = Topic.get_topics(request.user)
	data.update({'topics':topics})
	file = get_template(request, 'view_topics.html')
	return render(request, file, data)

def topic_create(request):
	pass

def topic_edit(request):
	pass

def topic_delete(request):
	pass