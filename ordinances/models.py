from django.db import models
from django.contrib.auth.models import User

class Ward(models.Model):
    name = models.CharField(max_length=100)
    member_goal = models.IntegerField('member goal')
    ordinance_goal = models.IntegerField('ordinance goal')

    def __unicode__(self):
        return self.name

# Extending the user model
class WardMember(models.Model):
    user = models.OneToOneField(User)
    ward = models.ForeignKey(Ward)

    def __unicode__(self):
        return self.ward.name

class Ancestor(models.Model):
    submitter = models.ForeignKey(User, null=True, blank=True)
    ward = models.ForeignKey(Ward)
    given_name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100)
    birth_year = models.CharField("year", max_length=4, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    baptism_date = models.DateField("baptism date", blank=True, null=True)
    confirmation_date = models.DateField("confirmation date", blank=True, null=True)
    initiatory_date = models.DateField("initiatory date", blank=True, null=True)
    endowment_date = models.DateField("endowment date", blank=True, null=True)
    sealing_to_parents_date = models.DateField("sealing to parent date", blank=True, null=True)
    sealing_to_spouse_date = models.DateField("sealing to spouse date", blank=True, null=True)

    def __unicode__(self):
        return self.given_name + " " + self.surname

