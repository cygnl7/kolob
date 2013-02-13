from django.db import models
from django.contrib.auth.models import User

class Ancestor(models.Model):
    submitter = models.ForeignKey(User, null=True, blank=True)
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
