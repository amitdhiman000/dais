from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from .control import UserRegControl
from device import get_template

## debugging
from pprint import pprint
## custom authentication class
from . import backends as auth


# Create your views here.

def login_old(request):
	c = {'title' : 'Login'};
	title = 'Login'
	t = get_template('login.html')
	html = t.render(Context({'title' : title}))
	return HttpResponse (html)


def login(request):
	c = {'title':'Login'}

	if 'form_errors' in request.session:
		c['form_errors'] = request.session['form_errors']
		c['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	c.update(csrf(request))
	file = get_template(request, 'login.html')
	return render(request, file, c)


def auth1(request):
	if request.method == 'POST':
		username = request.POST.get('user', '')
		password = request.POST.get('pass', '')
		#user = auth.authenticate(username=username, password=password)
		user = auth.auth_user(username=username, password=password)

		if user is not None:
			pprint(vars(user))
			auth.login(request, user)
			#request.session.set_expiry(10)
			return HttpResponseRedirect(settings.USER_PROFILE_URL)
		else:
			form_errors = {'user':'*Username or password is wrong!!'}
			form_values = {'user':request.POST.get('user', '')}
			request.session['form_errors'] = form_errors
			request.session['form_values'] = form_values
			return HttpResponseRedirect(settings.USER_LOGIN_URL)
		return HttpResponse('Invalid request!!')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(settings.USER_LOGIN_URL)

#functions for registration
def signup(request):
	c = {'title':'Signup'}
	c.update(csrf(request))
	if 'form_errors' in request.session:
		c['form_errors'] = request.session['form_errors']
		c['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	file = get_template(request, 'signup.html')
	return render(request, file, c)


def register(request):
	c = {'title':'Registration Successful'}
	if request.method == 'POST':
		control = None
		user_type = request.POST.get('user_type', '')
		control = UserRegControl(request.POST)

		if control is not None:
			if control.validate():
				control.register()
				file = get_template(request, 'registered.html')
				return render(request, file, c)
			else:
				request.session['form_errors'] = control.get_errors()
				request.session['form_values'] = control.get_values()
				return HttpResponseRedirect(settings.USER_SIGNUP_URL)
	return HttpResponseRedirect(settings.INVALID_REQUEST_URL)



def loggedin(request):
	return profile(request)


def profile(request):
	c = {'title':'Profile'}
	file = get_template('profile.html');
	return render(request, file, c)


def invalid(request):
	c = {'title': 'Invalid'};
#	return HttpResponse ('This is Invalid Request')
	file = get_template('profile.html')
	return render(request, file, c)