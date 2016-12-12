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
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^home$', views.index, name='index'),
    url(r'^topics-view/$', views.topics_view, name='topics_view'),
	url(r'^topic-create/$', views.topic_create, name='topic_create'),
    url(r'^topic-edit/$', views.topic_edit, name='topic_edit'),
    url(r'^topic-delete/$', views.topic_delete, name='topic_delete'),

    #url(r'^polls/view$', views.view_polls, name='view_polls'),
    #url(r'^poll/create$', views.create_poll, name='create_poll'),
    #url(r'^poll/edit/$', views.edit_poll, name='edit_poll'),
    #url(r'^poll/edit/$', views.edit_poll, name='edit_poll'),
]
