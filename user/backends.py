from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .models import User, Guest

USER_UID_KEY = '_user_uid'
USER_NAME_KEY = '_user_name'
USER_TYPE_KEY = '_user_type'
USER_AUTH_KEY = '_user_auth'


def auth_user(username='', password=''):
	user = None
	try:
		user = User.objects.get(email=username, password=password)
	except ObjectDoesNotExist:
		user = None

	return user


def get_user(request):
	user = None
	if USER_TYPE_KEY in request.session:
		if request.session[USER_TYPE_KEY] == 'User':
			user = User(name=request.session[USER_NAME_KEY])
	else:
		user = Guest()

	#print ('user name : '+user.name)
	return user


def login(request, user):
	# need to do it in accounts.middleware.AuthMiddleware
	#request.user = user
	request.session[USER_UID_KEY] = user._meta.pk.value_to_string(user)
	request.session[USER_NAME_KEY] = user.name
	request.session[USER_TYPE_KEY] = type(user).__name__
	print('class name : '+  type(user).__name__)
	request.session[USER_AUTH_KEY] = True
	request.session.set_expiry(60*5) # 5 minutes session timeout


def logout(request):
	request.session.flush()
	request.user = Guest()
	#request._cached_user = request.user


## Decorator function for chekcing the login status and redirect to login page
##
def login_required(funct):
	#@warps(funct)
	def decorator(request, *args, **kwargs):
		print(request)
		if request.user.is_loggedin() == False:
			return HttpResponseRedirect(settings.USER_LOGIN_URL)
		else:
			return funct(request, *args, **kwargs)
	return decorator;