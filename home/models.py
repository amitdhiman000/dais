from django.db import models
from user.models import User
from django.utils import timezone
# Create your models here.

class Poll(models.Model):
	pid = models.IntegerField(primary_key=True, unique=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=140, blank=False, default='')
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)

	@classmethod
	def create(klass, user, title, text):
		poll_object = klass()
		poll_object.author = User.objects.get(email=user.email)
		if poll_object.author is None:
			raise ValueError('user donsn\'t exist')

		poll_object.title = title
		poll_object.text = text
		poll_object.save()
		return poll_object

	@classmethod
	def get_poll(klass, poll_id):
		try:
			return klass.objects.get(id=poll_id)
		except:
			ValueError('Not any article with this id')

	@classmethod
	def get_user_polls(klass, user, start=0, count=10):
		polls = klass.objects.order_by('-created_date')[start:count]
		for poll in polls:
			tmp = PollsResponse.objects.filter(poll=poll)
			poll.yes = tmp.filter(response=1).count()
			poll.no = tmp.filter(response=-1).count()
			poll.not_sure = tmp.filter(response=0).count()
			if user.is_loggedin():
				try:
					poll.user_response = PollsResponse.objects.get(poll=poll, user=user).response
					print('user response : '+str(poll.response))
				except:
					pass
		return polls



class PollsResponse(models.Model):
	## {1: yes, -1: no, 0: not sure}
	##
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	response = models.IntegerField(default=3)
	
	@classmethod
	def response_yes(klass, user, poll):
		# prior check
		poll_object = klass.objects.get_or_create(user=user, poll=poll)[0]
		if 1 != poll_object.response:
			poll_object.response = 1
			poll_object.save()

	@classmethod
	def response_no(klass, user, poll):
		# prior check
		poll_object = klass.objects.get_or_create(user=user, poll=poll)[0]
		if -1 != poll_object.response:
			poll_object.response = -1
			poll_object.save()

	@classmethod
	def response_no(klass, user, poll):
		# prior check
		poll_object = klass.objects.get_or_create(user=user, poll=poll)[0]
		if 0 != poll_object.response:
			poll_object.response = 0
			poll_object.save()

	@classmethod
	def response_remove(klass, user, poll):
		# prior check
		try:
			instance = klass.objects.get(user=user, poll=poll)
			instance.delete()
		except:
			print('poll doesnt exist');