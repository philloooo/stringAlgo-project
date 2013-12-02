from django.db import models
from django.contrib.auth.models import User

# graph model
class Graph(models.Model):
	# graph=models.
	abstractId=models.IntegerField(blank=True, null=True)

class Relationship(models.Model):
	# sentences=models.ManyToManyField(ParsedSentence)
	Object=models.CharField(max_length=100)
	Subject=models.CharField(max_length=100)
	Verb=models.CharField(max_length=100)

class ParsedSentence(models.Model):
	abstractId=models.IntegerField(blank=True, null=True)
	disease=models.CharField(max_length=100)
	sentence=models.CharField(max_length=100)
	gene1=models.CharField(max_length=100)
	gene2=models.CharField(max_length=100)

	# reletionships=models.ManyToManyField(Relationship)
	reletionship=models.IntegerField(blank=True)

class History(models.Model):
	disease=models.CharField(max_length=100)
	user=models.ForeignKey(User)
	

# 