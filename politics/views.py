from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from common import post_required, login_required, redirect_if_loggedin, __redirect
from .models import Party

##
import device

## debugging
from pprint import pprint

# Create your views here.

def page_under_construction(request):
	data = {'title': 'Under Construction', 'page':'home'};
	file = device.get_template(request, 'error_under_construction.html')
	return render(request, file, data)

def indian_news_view(request):
	data = {'title': 'News', 'page':'home'};
	file = device.get_template(request, 'indian_news.html')
	return render(request, file, data)

def indian_trending_view(request):
	data = {'title': 'Trending', 'page':'home'};
	file = device.get_template(request, 'indian_news.html')
	return render(request, file, data)

def indian_latest_debates_view(request):
	return page_under_construction(request)

def indian_latest_laws_view(request):
	return page_under_construction(request)

def indian_latest_petitions_view(request):
	return page_under_construction(request)

def center_govt_projects_view(request):
	return page_under_construction(request)

def state_govt_projects_view(request):
	return page_under_construction(request)

def indian_parliament_members_view(request):
	return page_under_construction(request)

def indian_rajyasabha_members_view(request):
	return page_under_construction(request)

def state_legislative_members_view(request):
	return page_under_construction(request)


def parliament_const_view(request):
	parties = Party.get_list()
	data = {'title': 'Parties', 'page':'home', 'parties': parties};
	file = device.get_template(request, 'poltics_parties.html')
	return render(request, file, data)


def legislative_const_view(request):
	parties = Party.get_list()
	data = {'title': 'Parties', 'page':'home', 'parties': parties};
	file = device.get_template(request, 'poltics_parties.html')
	return render(request, file, data)


def parties_view(request):
	data = {'title': 'Parties', 'page':'home'};
	parties = Party.get_list()
	data.update({'parties': parties})
	file = device.get_template(request, 'poltics_parties.html')
	return render(request, file, data)


def indian_gdp_view(request):
	data = {'title': 'Indian GDP', 'page':'home'};
	file = device.get_template(request, 'indian_gdp.html')
	return render(request, file, data)


def indian_fdi_view(request):
	data = {'title': 'Indian FDI', 'page':'home'};
	file = device.get_template(request, 'indian_fdi.html')
	return render(request, file, data)