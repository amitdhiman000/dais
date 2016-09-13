from __future__ import unicode_literals

from django.db import models
from time import timezone
from datetime import datetime
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
import hashlib


class BaseUser(models.Model):
	uid = models.IntegerField(primary_key=True, unique=True)
	name = models.CharField(max_length=50, blank=False, default='')
	email = models.CharField(max_length=50, unique=True, blank=False, default='')
	password = models.CharField(max_length=32, blank=False, default='')
	created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=False, null=True)
	phone = models.CharField(max_length=10, blank=True)

	class Meta:
		# it will not create the table for abstact class.
		abstract = True
		verbose_name = _('user')
		verbose_name_plural= _('users')

	def get_absolute_url(self):
		return '/users/%s/' % urlquote(self.email)

	def get_full_name(self):
		return self.name
	##
	## Always return True, user object is created means loggedin.
	def is_loggedin(self):
		return True

	def add_user(self):
		self.save()

	def email_user(self, from_email=None, subject='Hello', message=None):
		send_mail(subject, message, from_email, self.email)


# Admin user class
class Admin(BaseUser):
	dob = models.CharField(max_length = 50)

	class Meta:
		verbose_name = _('Admin')
		verbose_name_plural= _('Admins')


# Vendor user class
class Moderator(BaseUser):
	#business = models.OneToOneField(Business)

	class Meta:
		verbose_name = _('Moderator')
		verbose_name_plural= _('Moderators')


# Author user class
class Author(BaseUser):
	#business = models.OneToOneField(Business)

	class Meta:
		verbose_name = _('Author')
		verbose_name_plural= _('Authors')


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