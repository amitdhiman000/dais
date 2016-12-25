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
	url(r'^$', views.index, name='index'),
#   url(r'^topics/(?P<name>\w+)/$', views.topic_add, name='topic_add'),
	url(r'^topics/$', views.topics_view, name='topics_view'),
	url(r'^alerts/$', views.alerts_view, name='alerts_view'),
	url(r'^invalid-request/$', views.invalid_request_view, name='invalid_request_view'),
	url(r'^polls/$', views.polls_view, name='polls_view'),
	url(r'^petitions/$', views.petitions_view, name='petitions_view'),
	url(r'^topic/new/$', views.new_topic_view, name='new_topic_view'),
	url(r'^topic/create/$', views.create_topic, name='create_topic'),
]
