from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

## all the decorator functions

## Decorator function for chekcing the login status and redirect to login page
##
def login_required(funct):
	#@warps(funct)
	def decorator(request, *args, **kwargs):
		print(request)
		if request.user.is_loggedin() == False:
			if 'application/json' in request.META.get('HTTP_ACCEPT'):
				return JsonResponse({'status':'false'}, status=302)
			return HttpResponseRedirect(settings.USER_LOGIN_URL)
		else:
			return funct(request, *args, **kwargs)
	return decorator;

def redirect_if_loggedin(funct):
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == True:
			if 'application/json' in request.META.get('HTTP_ACCEPT'):
				return JsonResponse({'status':'false'}, status=302)
			return HttpResponseRedirect(settings.USER_PROFILE_URL)
		return funct(request, *args, **kwargs)
	return _decorator