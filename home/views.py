from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from common import post_required, login_required, redirect_if_loggedin, __redirect
from post.models import Article
from .models import Poll, PollsResponse

##
import device

## debugging
from pprint import pprint

# Create your views here.

def invalid_request_view(request):
	data = {'title': 'Invalid Request'};
#	return HttpResponse ('This is Invalid Request')
	file = device.get_template(request, 'error_invalid_request.html')
	return render(request, file, data)

def index(request):
	template = device.get_template(request, 'home.html')
	data = {'title':'Home', 'page':'home'}

	articles = Article.get_user_articles(request.user)

	data.update({'articles': articles})

	return render(request, template, data)

def topics_view(request):
	template = device.get_template(request, 'post_topics.html')
	data = {'title':'Topics', 'page':'topics'}
	data.update(csrf(request))
	return render(request, template, data)


def alerts_view(request):
	template = device.get_template(request, 'alerts.html')
	return render(request, template, {'title':'Polls', 'page':'alerts'})

def load_topics(request):
	return topics(request)

def polls_view(request):
	data = {'title':'Polls', 'page':'topics'}
	polls = Poll.get_user_polls(request.user)
	data.update({'polls': polls})
	template = device.get_template(request, 'post_polls.html')
	return render(request, template, data)

def petitions_view(request):
	data = {'title':'Petitions', 'page':'topics'}
	#polls = Petition.get_user_petitions(request.user)
	#data.update({'polls': polls})
	template = device.get_template(request, 'post_petitions.html')
	return render(request, template, data)

@login_required
def new_topic_view(request):
	data = {'title':'New Topic', 'page':'topics'}
	template = device.get_template(request, 'post_new_topic.html')
	return render(request, template, data)

@post_required
@login_required
def create_topic(request):
	pprint(request)
	pprint(request.POST)
	error = None
	topic = None
	topic_type = request.POST.get('topic_type', -1)
	title = request.POST.get('title', '').strip(' \t\n\r')
	text = request.POST.get('text', '').strip(' \t\n\r')
	if title == '' or text == '':
		error = 'Title , Abstract cannot be empty'
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

	## send the response
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':204, 'message': 'published'})
		else:
			return JsonResponse({'status':401, 'message': error})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)

