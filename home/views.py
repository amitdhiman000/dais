from django.shortcuts import render
from django.template.context_processors import csrf
import device
from user.models import Article

# Create your views here.

def index(request):
	template = device.get_template(request, 'home.html')
	data = {'title':'Home', 'page':'home'}

	articles = Article.get_user_articles(request.user)

	data.update({'articles': articles})

	return render(request, template, data)

def topics(request):
	template = device.get_template(request, 'topics.html')
	data = {'title':'Home', 'page':'topics'}
	data.update(csrf(request))
	return render(request, template, data)

def alerts(request):
	template = device.get_template(request, 'alerts.html')
	return render(request, template, {'title':'Home', 'page':'alerts'})

