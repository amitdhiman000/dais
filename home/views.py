from django.shortcuts import render
import device
# Create your views here.

def index(request):
	template = device.get_template(request, 'home.html')
	return render(request, template, {'title':'Dais | Home'})


