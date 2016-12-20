from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
##
## import other apps
from user.models import User
from post.models import Article, ArticleReaction, ArticleComment, Topic
## custom packages
from device import get_template
from common import redirect_if_loggedin, login_required, __redirect
## debug
from pprint import pprint

def index(request):
	data = {'title': 'Dais Admin', 'page':'user'};
	topics = Topic.get_topics(request.user)
	data.update({'topics':topics})
	data.update(csrf(request))
	file = get_template(request, 'admin_index.html')
	return render(request, file, data)

def topics_view(request):
	data = {'title': 'Follow Topics', 'page':'user'};
	topics = Topic.get_topics(request.user)
	data.update({'topics':topics})
	data.update(csrf(request))
	file = get_template(request, 'admin_topics_page.html')
	return render(request, file, data)

@login_required
def topic_create(request):
	pprint(request)
	error = None
	name = request.POST.get('topic_name', '').strip(' \t\n\r')
	desc = request.POST.get('topic_desc', '').strip(' \t\n\r')
	if name == '' or desc == '':
		error = 'Title or Description is mentatory'
	elif Topic.check_duplicate(name):
		error = 'Already Exists'
	elif Topic.create(request.user, name, desc) == False:
		error = 'Failed to create topic'


	## send the response
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':200, 'message': 'created'})
		else:
			return JsonResponse({'status':401, 'message': error})
	else:
		if error == None:
			return __redirect(request, settings.DAIS_ADMIN_HOME)
		else:
			return __redirect(request, settings.HOME_PAGE_URL)

@login_required
def topic_update(request):
	topic_id = request.POST.get('topic_id', -1)
	name = request.POST.get('topic_name', '').strip(' \t\n\r')
	desc = request.POST.get('topic_desc', '').strip(' \t\n\r')
	if name == '' or desc == '':
		error = 'Title and Description are mentatory'
	elif topic_id == -1:
		error = 'Invlaid Topic'
	elif Topic.update(request.user, topic_id, name, desc) == False:
		error = 'Failed to update topic'

@login_required
def topic_delete(request):
	topic_id = request.POST.get('topic_id', -1)
	if topic_id == -1:
		error = 'Invlaid Topic'
	elif Topic.update(request.user, topic_id) == False:
		error = 'Failed to delete topic'