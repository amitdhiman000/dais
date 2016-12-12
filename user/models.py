from __future__ import unicode_literals

from django.db import models
#from time import timezone
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
import hashlib
from pprint import pprint


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
		#self.email = ''
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


class Topic(models.Model):
	topic_name = models.CharField(max_length=50, blank=False)
	topic_desc = models.CharField(max_length=100, blank=True)
	topic_followers = models.IntegerField(default=0)

	@classmethod
	def get_topics(klass, user):
		topics = klass.objects.order_by('-topic_followers')
		if topics != None:
			for topic in topics:
				#tmp = TopicFollower.objects.filter(user=user).order_by('topic__topic_followers')
				if TopicFollower.objects.filter(topic=topic, user=user).exist():
					topic.followed = 1
				else:
					topic.followed = 0
		return topics

class TopicFollower(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

	@classmethod
	def add_follower(klass, user, topic):
		pass

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

	def get_title(self):
		return self.title

	def get_sub_title(self):
		return self.sub_title

	@classmethod
	def create(klass, user, title, text):
		article = klass()
		article.author = User.objects.get(email=user.email)
		if article.author is None:
			raise ValueError('user donsn\'t exist')

		article.title = title
		article.text = text
		article.save()
		return article

	@classmethod
	def get_article(klass, article_id):
		try:
			return klass.objects.get(id=article_id)
		except:
			ValueError('Not any article with this id')

	@classmethod
	def get_user_articles(klass, user, start=0, count=10):
		articles = klass.objects.order_by('-created_date')[start:count]
		for art in articles:
			tmp = ArticleReaction.objects.filter(article=art)
			art.likes = tmp.filter(reaction=1).count()
			art.dislikes = tmp.filter(reaction=-1).count()
			art.reaction = 0
			if user.is_loggedin():
				try:
					art.reaction = ArticleReaction.objects.get(article=art, user=user).reaction
					print('reaction : '+str(art.reaction))
				except:
					pass
		return articles


class ArticleComment(Post):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)

	@classmethod
	def create(klass, article, user, text):
		comment = klass(article=article, author=user, text=text)
		comment.save()

	@classmethod
	def remove(klass, comment_id, user):
		try:
			comment = klass.objects.get(id=comment_id, author=user)
			comment.delete()
			return True
		except:
			return False

	@classmethod
	def get_comments(klass, article_id, start=0, count=10):
		#try:
		#comments = klass.objects.extra(select={'article_id':'article_id'}).filter(article=article_id).order_by('-created_date')[start:count].values('id', 'parent_id', 'author__email', 'text')
		comments = klass.objects.filter(article=article_id).order_by('created_date')[start:count].values('id', 'article_id', 'author__email', 'text')
		return comments
		#except:
		return None

class ReplyComment(Post):
	comment = models.ForeignKey('self', on_delete=models.CASCADE)

	@classmethod
	def create(klass, comment, user, text):
		comment = klass(comment=comment, author=user, text=text)
		comment.save()

	@classmethod
	def remove(klass, comment, user):
		try:
			comment = klass.objects.get(pk=comment.pk, author=user)
			comment.delete()
			return True
		except:
			return False


class ArticleReaction(models.Model):
	# {'condemn': -3, 'angry': -2, dislike': -1, 'like': 1, 'happy': 2, 'waov': 3, 'laugh': 4}
	# default is like
	article = models.ForeignKey(Article, on_delete=models.CASCADE, db_index=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	reaction = models.IntegerField(default=1)

	@classmethod
	def like(klass, user, article):
		# prior check
		article_object = klass.objects.get_or_create(user=user, article=article)[0]
		if 1 != article_object.reaction:
			article_object.reaction = 1
			article_object.save()

	@classmethod
	def dislike(klass, user, article):
		# prior check
		article_object = klass.objects.get_or_create(user=user, article=article)[0]
		if -1 != article_object.reaction:
			article_object.reaction = -1
			article_object.save()

	@classmethod
	def remove(klass, user, article):
		# prior check
		try:
			instance = klass.objects.get(user=user, article=article)
			instance.delete()
		except:
			print('comment doesnt exist');


class CommentReaction(models.Model):
	# {'condemn': -3, 'angry': -2, dislike': -1, 'like': 1, 'happy': 2, 'waov': 3, 'laugh': 4}
	# default is like
	comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, db_index=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	reaction = models.IntegerField(default=1)

	@classmethod
	def like(klass, user, comment):
		# prior check
		comment_object = klass.objects.get_or_create(user=user, comment=comment)[0]
		comment_object.reaction = 1
		comment_object.save()

	@classmethod
	def dislike(klass, user, comment):
		# prior check
		comment_object = klass.objects.get_or_create(user=user, comment=comment)[0]
		comment_object.reaction = -1
		comment_object.save()

class ReplyCommentReaction(models.Model):
	# {'condemn': -3, 'angry': -2, dislike': -1, 'like': 1, 'happy': 2, 'waov': 3, 'laugh': 4}
	# default is like
	comment = models.ForeignKey(ReplyComment, on_delete=models.CASCADE, db_index=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	reaction = models.IntegerField(default=1)

	@classmethod
	def like(klass, user, comment):
		# prior check
		comment_object = klass.objects.get_or_create(user=user, comment=comment)[0]
		comment_object.reaction = 1
		comment_object.save()

	@classmethod
	def dislike(klass, user, comment):
		# prior check
		comment_object = klass.objects.get_or_create(user=user, comment=comment)[0]
		comment_object.reaction = -1
		comment_object.save()