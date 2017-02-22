from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from common import post_required, login_required, redirect_if_loggedin, __redirect
from post.models import Article

##
import device

## debugging
from pprint import pprint

# Create your views here.

def indian_news_view(request):
	data = {'title': 'News', 'page':'home'};
	file = device.get_template(request, 'indian_news.html')
	return render(request, file, data)

def indian_trending_view(request):
	data = {'title': 'Trending', 'page':'home'};
	file = device.get_template(request, 'indian_news.html')
	return render(request, file, data)

def index(request):
	template = device.get_template(request, 'home.html')
	data = {'title':'Home', 'page':'home'}

	articles = Article.get_user_articles(request.user)

	data.update({'articles': articles})

	return render(request, template, data)

def topics_view(request):
	template = device.get_template(request, 'post_topics.html')
	data = {'title':'Topics', 'page':'post'}
	data.update(csrf(request))
	return render(request, template, data)


def alerts_view(request):
	template = device.get_template(request, 'home_alerts.html')
	return render(request, template, {'title':'Polls', 'page':'alerts'})

def load_topics(request):
	return topics_view(request)


