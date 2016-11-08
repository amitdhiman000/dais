from __future__ import unicode_literals

from django.db import models
#from time import timezone
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
import hashlib


class User(models.Model):
	uid = models.IntegerField(primary_key=True, unique=True)
	name = models.CharField(max_length=50, blank=False, default='')
	email = models.EmailField()
	password = models.CharField(max_length=32, blank=False, default='')
	created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=False, null=True)
	phone = models.CharField(max_length=10, blank=True)
	status = models.IntegerField(default=1)
	level = models.IntegerField(default=1)

	def get_absolute_url(self):
		return '/users/%s/' % urlquote(self.email)

	def get_name(self):
		return self.name
	##
	## Always return True, user object is created means loggedin.
	def is_loggedin(self):
		return True

	def add_user(self):
		self.save()

	def email_user(self, from_email=None, subject='Hello', message=None):
		send_mail(subject, message, from_email, self.email)


class Guest:
	def __init__(self):
		self.email = ''
		self.name = 'Guest'

	def get_full_name(self):
		return self.name

	def is_loggedin(self):
		return False


class Country(models.Model):
	country_id = models.IntegerField(primary_key=True, unique=True, null=False)
	country_name = models.CharField(max_length=50, blank=True)

	class Meta:
		verbose_name = _('country')
		verbose_name_plural= _('countries')


class State(models.Model):
	state_id = models.IntegerField(primary_key=True, unique=True, null=False)
	state_name = models.CharField(max_length=50, blank=True)
	fk_country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('state')
		verbose_name_plural= _('states')


class City(models.Model):
	city_id = models.IntegerField(primary_key=True, unique=True, null=False)
	city_name = models.CharField(max_length=50, blank=True)
	fk_state_id = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('city')
		verbose_name_plural= _('cities')


class Area(models.Model):
	area_id = models.IntegerField(primary_key=True, unique=True, null=False)
	area_name = models.CharField(max_length=50, blank=True)
	area_pin = models.CharField(max_length=10, blank=True)
	fk_city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	fk_state_id = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('area')
		verbose_name_plural= _('areas')

class Address(models.Model):
	address_id = models.IntegerField(primary_key=True, unique=True, null=False)
	house_info = models.CharField(max_length=50, blank=True)
	geo_long = models.CharField(max_length=10, blank=True)
	geo_lat = models.CharField(max_length=10, blank=True)
	fk_area_id = models.ForeignKey(Area, on_delete=models.CASCADE)


class Topics(models.Model):
	topic_name = models.CharField(max_length=50, blank=False)
	topic_desc = models.CharField(max_length=100, blank=True)


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	edited_date = models.DateTimeField(default=timezone.now)
	approved = models.BooleanField(default=False)

	class Meta:
		# it will not create the table for abstact class.
		abstract = True
		verbose_name = _('post')
		verbose_name_plural= _('posts')

	def set_approve(self):
		self.approved = True
		self.save()

	def get_approve(self):
		return self.approved

	def __str__(self):
		return self.text

class Article(Post):
	title = models.CharField(max_length=100, blank=False)
	sub_title = models.CharField(max_length=200, blank=False)

	@classmethod
	def create(self, request):
		post = request.POST
		if post is None:
			raise ValueError('post data can\'t be None')
		title = post.get('title', None)
		text = post.get('text', None)
		if title is None or text is None:
			raise ValueError('Values can\'t be None')

		article = Article()
		article.author = User.objects.get(email=request.user.email)
		if article.author is None:
			raise ValueError('user donsn\'t exist')

		article.title = title
		article.text = text
		return article

	def get_title(self):
		return self.title

	def get_sub_title(self):
		return self.sub_title

class Comment(Post):
	reply_to = models.ForeignKey('self', on_delete=models.CASCADE)