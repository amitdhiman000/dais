from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

## all the decorator functions

## Decorator function for chekcing the login status and redirect to login page
##

def __redirect(request, url):
	if request.is_ajax():
		return JsonResponse({'status':302, 'url': url})
	return HttpResponseRedirect(url)

def login_required(funct):
	#@warps(funct)
	def _decorator(request, *args, **kwargs):
		print(request)
		if request.user.is_loggedin() == False:
			return __redirect(request, settings.USER_LOGIN_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		else:
			return funct(request, *args, **kwargs)
	return _decorator;

def redirect_if_loggedin(funct):
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == True:
			return __redirect(request, settings.USER_PROFILE_URL)
		return funct(request, *args, **kwargs)
	return _decorator