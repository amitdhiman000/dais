from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from common import redirect_if_loggedin, login_required, __redirect
import device
from user.models import Article
from .models import Poll, PollsResponse

## debugging
from pprint import pprint

# Create your views here.

def index(request):
	template = device.get_template(request, 'home.html')
	data = {'title':'Home', 'page':'home'}

	articles = Article.get_user_articles(request.user)

	data.update({'articles': articles})

	return render(request, template, data)

def topics(request):
	template = device.get_template(request, 'topics.html')
	data = {'title':'Topics', 'page':'topics'}
	data.update(csrf(request))
	return render(request, template, data)


def alerts(request):
	template = device.get_template(request, 'alerts.html')
	return render(request, template, {'title':'Polls', 'page':'alerts'})

def load_topics(request):
	return topics(request)

def load_polls(request):
	data = {'title':'Polls', 'page':'topics'}
	polls = Poll.get_user_polls(request.user)
	data.update({'polls': polls})
	template = device.get_template(request, 'polls.html')
	return render(request, template, data)

def load_petitions(request):
	data = {'title':'Petitions', 'page':'topics'}
	#polls = Petition.get_user_petitions(request.user)
	#data.update({'polls': polls})
	template = device.get_template(request, 'petitions.html')
	return render(request, template, data)

#@login_required
def new_topic(request):
	data = {'title':'New Topic', 'page':'topics'}
	template = device.get_template(request, 'new_topic.html')
	return render(request, template, data)

@login_required
def create_topic(request):
	pprint(request);
	if request.method == 'POST':
		pprint(request.POST)
		error = None
		topic = None
		topic_type = request.POST.get('topic_type', -1)
		title = request.POST.get('title', None)
		text = request.POST.get('text', None)
		if title == None or text == None:
			error = 'Title , Abstract can\'t be empty'
		else:
			#try:
			if topic_type == '1':
				topic = Article.create(request.user, title, text)
			elif topic_type == '2':
				topic = Poll.create(request.user, title, text)
			elif topic_type == '3':
				#topic = Petition.create(request.user, title, text)
				error = 'Not supported yet'
			else:
				error = 'Invalid topic category'

			#except ValueError as e:
			#	print('ValueError : '+ str(e))
			#except:
			#	print('Unknown error')
	else:
		error = 'Invalid request'

	## send the response
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':204, 'message': 'published'})
		else:
			return JsonResponse({'status':401, 'message': error})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)

