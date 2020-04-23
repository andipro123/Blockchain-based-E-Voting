from django.db import models

# Create your models here.

class Candidate(models.Model):
    candidateID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    party = models.CharField(max_length=100)
    criminalRecords = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
