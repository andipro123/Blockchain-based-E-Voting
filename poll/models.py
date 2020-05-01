from django.db import models
from uuid import uuid4
from datetime import datetime

# Create your models here.

def get_time():
    return datetime.now().timestamp()

class Candidate(models.Model):
    candidateID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    party = models.CharField(max_length=100)
    criminalRecords = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

class Voter(models.Model):
    username = models.CharField(max_length=30)
    public_key_n = models.CharField(max_length=320)
    public_key_e = models.IntegerField(default=0)
    has_voted = models.BooleanField(default=False)

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    vote = models.IntegerField(default=0)
    timestamp = models.FloatField(default=get_time)
    block_id = models.IntegerField(null=True)

    def __str__(self):
        return "{}|{}|{}".format(self.id, self.vote, self.timestamp)

class Block(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    prev_hash = models.CharField(max_length=64, blank=True)
    merkle_hash = models.CharField(max_length=64, blank=True)
    self_hash = models.CharField(max_length=64, blank=True)
    nonce = models.IntegerField(null=True)
    timestamp = models.FloatField(default=get_time)

    def __str__(self):
        return str(self.self_hash)

