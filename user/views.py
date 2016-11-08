from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from device import get_template
from common import redirect_if_loggedin, login_required, __redirect
## custom authentication
from .models import Article
from .control import UserRegControl
from . import backends as auth

## debugging
from pprint import pprint

# Create your views here.

@redirect_if_loggedin
def login(request):
	data = {'title':'Login', 'page':'user'}
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	data.update(csrf(request))
	file = get_template(request, 'login.html')
	return render(request, file, data)


def auth1(request):
	if request.method == 'POST':
		username = request.POST.get('user', '')
		password = request.POST.get('pass', '')
		user = auth.auth_user(username=username, password=password)

		if user is not None:
			pprint(vars(user))
			auth.login(request, user)
			#request.session.set_expiry(10)
			return __redirect(request, settings.USER_PROFILE_URL)
		else:
			form_errors = {'user':'*Username or password is wrong!!'}
			form_values = {'user':request.POST.get('user', '')}
			request.session['form_errors'] = form_errors
			request.session['form_values'] = form_values
			return __redirect(request, settings.USER_LOGIN_URL)
		return HttpResponse('Invalid request!!')

def logout(request):
	auth.logout(request)
	return __redirect(request, settings.USER_LOGIN_URL)

#functions for registration
def signup(request):
	data = {'title':'Signup', 'page':'user'}
	data.update(csrf(request))
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	file = get_template(request, 'signup.html')
	return render(request, file, data)


def register(request):
	data = {'title':'Registration Successful', 'page':'user'}
	if request.method == 'POST':
		control = None
		user_type = request.POST.get('user_type', '')
		control = UserRegControl(request.POST)

		if control is not None:
			if control.validate():
				control.register()
				file = get_template(request, 'registered.html')
				return render(request, file, data)
			else:
				request.session['form_errors'] = control.get_errors()
				request.session['form_values'] = control.get_values()
				return __redirect(request, settings.USER_SIGNUP_URL)
	return __redirect(request, settings.INVALID_REQUEST_URL)



def loggedin(request):
	return profile(request)


def profile(request):
	print('request for profile')
	data = {'title':'Profile', 'page':'user'}
	file = get_template(request, 'profile.html');
	return render(request, file, data)


def invalid(request):
	data = {'title': 'Invalid'};
#	return HttpResponse ('This is Invalid Request')
	file = get_template(request, 'profile.html')
	return render(request, file, data)

@login_required
def add_topic(request):
	pprint(request.POST)
	try:
		article = Article.create(request)
		article.save()
	except ValueError as e:
		print('ValueError : '+ str(e))
	except:
		print('Unknown error')

	## send the response
	if request.is_ajax():
		return JsonResponse({'status':204, 'message': 'Successfully published'})
	else:
		template = get_template(request, 'topics.html')
		data = {'title':'Home', 'page':'topics'}
		data.update(csrf(request))
		return render(request, template, data)