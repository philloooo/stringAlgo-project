from django.db import models
from django.contrib.auth.models import User

# graph model
class Graph(models.Model):
	graph=models.
	abstractId=models.IntegerField(blank=True;null=True)

class ParsedSentence(models.Model):
	abstractId=models.IntegerField(blank=True;null=True)
	disease=models.CharField()
	sentence=models.CharField()
	reletionships=models.ManyToManyField(Relatioship)

class Relationship(models.Model):
	# sentences=models.ManyToManyField(ParsedSentence)
	Object=models.CharField()
	Subject=models.CharField()
	Verb=models.CharField()

# 