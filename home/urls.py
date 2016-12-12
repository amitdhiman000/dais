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
    url(r'^topics/$', views.load_topics, name='load_topics'),
    url(r'^polls/$', views.load_polls, name='load_polls'),
    url(r'^petitions/$', views.load_petitions, name='load_petitions'),
    url(r'^topic/new/$', views.new_topic, name='new_topic'),
    url(r'^topic/create/$', views.create_topic, name='create_topic'),
#   url(r'^topics/(?P<name>\w+)/$', views.topic_add, name='topic_add'),
    url(r'^alerts/$', views.alerts, name='alerts'),
]
