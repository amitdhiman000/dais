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
	url(r'^polls/$', views.polls_view, name='polls_view'),
	url(r'^petitions/$', views.petitions_view, name='petitions_view'),
	url(r'^new-topic/$', views.new_topic_view, name='new_topic_view'),
	url(r'^create-topic/$', views.create_topic, name='create_topic'),
	url(r'^update-topic/$', views.update_topic, name='update_topic'),
	url(r'^delete-topic/$', views.delete_topic, name='delete_topic'),
	url(r'^post-reaction/$', views.post_reaction, name='post_reaction'),
	url(r'^post-comment/$', views.post_comment, name='post_comment'),
	url(r'^post-comment-reaction/$', views.post_comment_reaction, name='post_comment_reaction'),
	url(r'^reply-comment/$', views.reply_comment, name='reply_comment'),
	url(r'^reply-comment-reaction/$', views.reply_comment_reaction, name='reply_comment_reaction'),
	url(r'^load-post-comments/$', views.load_post_comments, name='load_post_comments'),
	url(r'^load-reply-comments/$', views.load_reply_comments, name='load_reply_comments'),
]