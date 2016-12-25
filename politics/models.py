from django.db import models
from user.models import State

from django.utils.translation import ugettext as _
## debug
from pprint import pprint
# Create your models here.

class Party(models.Model):
	short_name = models.CharField(max_length=10, default='***')
	full_name = models.CharField(max_length=50, default='*****')
	#logo = models.CharField(max_length=50, default='')
	#president = models.CharField(max_length=50, default='')
	#founded_by = models.CharField(max_length=50, default='')
	#founded_year = models.IntegerField(default=0)

	class Meta:
		verbose_name = _('Party')
		verbose_name_plural= _('Parties')

	@classmethod
	def get_list(klass):
		list = klass.objects.all()
		return list


class Leader(models.Model):
	name = models.CharField(max_length=50, default='*****')
	party = models.ForeignKey(Party, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('Leader')
		verbose_name_plural= _('Leaders')



class ParliamentConstituency(models.Model):
	name = models.CharField(max_length=50, default='*****')
	lc = models.ForeignKey('LegislativeConstituency', on_delete=models.CASCADE)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('ParliamentConstituency')
		verbose_name_plural= _('ParliamentConstituencies')



class LegislativeConstituency(models.Model):
	name = models.CharField(max_length=50, default='*****')
	pc = models.ForeignKey(ParliamentConstituency, on_delete=models.CASCADE)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('LegislativeConstituency')
		verbose_name_plural= _('LegislativeConstituencies')



class MemberParliament(models.Model):
	leader = models.ForeignKey(Leader, on_delete=models.CASCADE)
	constituency = models.ForeignKey(ParliamentConstituency, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('MemberParliament')
		verbose_name_plural= _('MemberParliaments')



class MemberLegislative(models.Model):
	leader = models.ForeignKey(Leader, on_delete=models.CASCADE)
	constituency = models.ForeignKey(LegislativeConstituency, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('MemberLegislative')
		verbose_name_plural= _('MemberLegislatives')


