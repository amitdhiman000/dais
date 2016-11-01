from django.shortcuts import render
import device
# Create your views here.

def index(request):
	template = device.get_template(request, 'home.html')
	return render(request, template, {'title':'Home', 'page':'home'})

def topics(request):
	template = device.get_template(request, 'topics.html')
	return render(request, template, {'title':'Home', 'page':'topics'})

def alerts(request):
	template = device.get_template(request, 'alerts.html')
	return render(request, template, {'title':'Home', 'page':'alerts'})

