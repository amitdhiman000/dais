"""MyOffers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^latest-laws/$', views.indian_latest_laws_view, name='indian_trending_view'),
	url(r'^latest-debates/$', views.indian_latest_debates_view, name='indian_trending_view'),
	url(r'^latest-petitions/$', views.indian_latest_petitions_view, name='indian_trending_view'),
	url(r'^parliament-const/$', views.parliament_const_view, name='parliament_const_view'),
	url(r'^legislative-const/$', views.legislative_const_view, name='legislative_const_view'),
	url(r'^indian-parliament-members/$', views.indian_parliament_members_view, name='indian_parliament_members_view'),
	url(r'^indian-rajyasabha-members/$', views.indian_rajyasabha_members_view, name='indian_rajyasabha_members_view'),
	url(r'^state-legislative-members/$', views.state_legislative_members_view, name='state_legislative_members_view'),
	url(r'^center-govt-projects/$', views.center_govt_projects_view, name='center_govt_projects_view'),
	url(r'^state-govt-projects/$', views.state_govt_projects_view, name='state_govt_projects_view'),
	url(r'^parties/$', views.parties_view, name='parties_view'),
	url(r'^indian-gdp/$', views.indian_gdp_view, name='indian_gdp_view'),
	url(r'^indian-fdi/$', views.indian_fdi_view, name='indian_fdi_view'),
]