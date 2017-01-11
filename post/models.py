from django.db import models
from django.db import connection
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from datetime import datetime
import base64
from django.utils.safestring import mark_safe
## models import
from user.models import User
## debug
from pprint import pprint
# Create your models here.

class Topic(models.Model):
	topic_author = models.ForeignKey(User, on_delete=models.CASCADE)
	topic_name = models.CharField(max_length=50, blank=False)
	topic_desc = models.CharField(max_length=100, blank=True)
	topic_followers = models.IntegerField(default=0)

	@classmethod
	def get_topics(klass, user):
		print(connection.queries)
		print('\n')
		topics = klass.objects.annotate(name=models.F('topic_name')).order_by('-topic_followers').values('id', 'name', 'topic_followers')
		marked = TopicFollower.objects.annotate(topic_id=models.F('topic__id')).filter(user=user).values('topic_id')

		hash = {}
		for mark in marked:
			hash[mark['topic_id']] = 1

		for topic in topics:
			if topic['id'] in hash:
				topic['followed'] = 1
			else:
				topic['followed'] = 0

		for mark in marked:
			print(mark['topic_id'])

		'''
		for topic in topics:
			if TopicFollower.objects.filter(user=user,topic=topic).exists():
				topic.followed = 1
			else:
				topic.followed = 0

		for t in topics:
			print('followed '+str(t['id'])+'/'+str(t['followed']))
		'''
		#print(connection.queries)
		return topics

	@classmethod
	def check_duplicate(klass, name):
		return klass.objects.filter(topic_name__iexact=name).exists()

	@classmethod
	def create(klass, user, title, text):
		topic = klass()
		topic.topic_author = User.objects.get(email=user.email)
		if topic.topic_author is None:
			print('user doesn\'t exist')
			return False

		topic.topic_name = title
		topic.topic_desc = text
		try:
			topic.save()
			return True
		except:
			return False

	@classmethod
	def update(klass, user, topic_id, title, text):
		topic = klass.objects.get(id=topic_id, topic_author=user)
		if topic == None:
			print('topic doesn\'t exist')
			return False

		topic.topic_name = title
		topic.topic_desc = text
		try:
			topic.save()
			return True
		except:
			return False

	@classmethod
	def remove(klass, user, topic_id):
		try:
			topic = klass.objects.get(id=topic_id, topic_author=user)
			topic.delete()
			return True
		except:
			return False

class TopicFollower(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

	@classmethod
	def add_follower(klass, user, topic_id):
		topic = None
		try:
			topic = Topic.objects.get(pk=int(topic_id))
		except:
			print('topic doesnnot exist')
			return False

		follower = klass.objects.get_or_create(user=user, topic=topic)[0]
		if follower == None:
			return False
		return True

	@classmethod
	def remove_follower(klass, user, topic):
		try:
			follower = klass.objects.get(topic=topic, user=user)
			follower.delete()
			return True
		except:
			return False


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
	def remove(klass, user, article_id):
		try:
			comment = klass.objects.get(id=article_id, author=user)
			comment.delete()
			return True
		except:
			return False

	@classmethod
	def get_article(klass, article_id):
		try:
			return klass.objects.get(id=article_id)
		except:
			ValueError('Not any article with this id')

	@classmethod
	def get_user_articles(klass, user, start=0, count=10):
		articles = klass.objects.order_by('-created_date')[start:count]

		data = open(settings.STATIC_ROOT+"/images/icons-svg/user-1.svg", "rb").read()
		image = "data:image/svg+xml;base64,%s" % base64.b64encode(data).decode('utf8')
		for art in articles:
			tmp = ArticleReaction.objects.filter(article=art)
			art.likes = tmp.filter(reaction=1).count()
			art.dislikes = tmp.filter(reaction=-1).count()
			art.reaction = 0
			art.author.image = image
			if user.is_loggedin():
				try:
					art.reaction = ArticleReaction.objects.get(article=art, user=user).reaction
					print('reaction : '+str(art.reaction))
				except:
					pass
		return articles


class ArticleComment(Post):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)

	def __iter__(self):
		return [self.id, self.article_id, self.text, self.author__email]

	@classmethod
	def create(klass, article, user, text):
		try:
			comment = klass.objects.create(article=article, author=user, text=text)
			#comment.save()
			comment.author_name = user.name
			return comment
		except:
			pass
		return None

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
		#comments = klass.objects.extra(select={'author_name':'author__name'}).filter(article=article_id).order_by('created_date')[start:count].values('id', 'article_id', 'author_name', 'text')
		comments = klass.objects.annotate(author_name=models.F('author__name')).filter(article=article_id).order_by('created_date')[start:count].values('id', 'article_id', 'author_name', 'text')
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
		ar_object = klass.objects.get_or_create(user=user, article=article)[0]
		if 1 != ar_object.reaction:
			ar_object.reaction = 1
			ar_object.save()

	@classmethod
	def dislike(klass, user, article):
		# prior check
		ar_object = klass.objects.get_or_create(user=user, article=article)[0]
		if -1 != ar_object.reaction:
			ar_object.reaction = -1
			ar_object.save()

	@classmethod
	def remove(klass, user, article):
		# prior check
		try:
			ar_object = klass.objects.get(user=user, article=article)
			ar_object.delete()
		except:
			print('reaction doesnt exist');


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
