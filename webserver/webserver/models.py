from django.db import models
from django.contrib.auth.models import User

class Pmid(models.Model):
	abstractId=models.CharField(max_length=100)
# graph model
class Graph(models.Model):
	# graph=models.
	pmid=models.ManyToManyField(Pmid)
	disease=models.CharField(max_length=100)
	path=models.CharField(max_length=100)
class Relationship(models.Model):
	# sentences=models.ManyToManyField(ParsedSentence)
	Object=models.CharField(max_length=100)
	Subject=models.CharField(max_length=100)
	Verb=models.CharField(max_length=100)



class ParsedSentence(models.Model):
	abstractId=models.CharField(max_length=100)
	disease=models.CharField(max_length=100)
	sentence=models.CharField(max_length=100)
	gene1=models.CharField(max_length=100)
	gene2=models.CharField(max_length=100)
	score=models.IntegerField(blank=True)
	# reletionships=models.ManyToManyField(Relationship)
	relationship=models.IntegerField(blank=True)

class History(models.Model):
	disease=models.CharField(max_length=100)
	user=models.ForeignKey(User)

class UselessAbstract(models.Model):
	abstractId=models.CharField(max_length=100)

