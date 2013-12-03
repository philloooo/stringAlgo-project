import random
import os
import associationFinder
import visual
import time
import urllib3
import xml.etree.ElementTree as ET
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import datetime
from django.views.decorators.csrf import csrf_protect
from models import *
from form import *
from django.http import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def register(request):
	context={}
	form=regiForm(request.POST)
	errors=[]
	context['errors']=errors
	context['form']=form
	context['register']=True
	if not form.is_valid():
		return render(request,'webserver/login.html',context)
	if len(User.objects.filter(username = request.POST['username'])) > 0:
		errors.append('Username is already taken.')
	if errors:
		return render(request,'webserver/login.html',context)
	new_user=User.objects.create_user(username=form.cleaned_data['username'],\
					password=form.cleaned_data['password1'],email=form.cleaned_data['email'])

	# new_user.is_active =False
	new_user.save()
	return redirect('/login')


@login_required	
def home(request):
	context = {}
	return render(request,'webserver/home.html',context)

@login_required
def search(request):
	context={}
	# get abstracts id
	disease=request.POST['disease']
	if len(disease)==0:
		return render(request,'webserver/result.html',context)

	# Check if the disease is searched before
	if os.path.isdir('./webserver/static/webserver/diseases/'+disease):
		if len(Graph.objects.filter(disease=disease))>=1:
			graph=Graph.objects.get(disease=disease)
			svg=graph.path
			context['svg']=svg
			return render(request,'webserver/result.html',context)

	
	# store the history
	if len(History.objects.filter(user=request.user,disease=disease))==0:
		history=History(user=request.user,disease=disease)
		history.save()

	parsed='+'.join(disease.split())
	http = urllib3.PoolManager()
	r = http.request('GET', 
		'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='+\
		parsed+'&usehistory=y&retmax=1000')
	XML=ET.fromstring(r.data)
	ids=[]
	for child in XML:
		if child.tag=='IdList':
			# print child
			for cid in child:
				# print cid.text
				ids.append(cid.text)


	# get abstract
	posFileName='./wordDictionaries/posWords.txt'
	geneFileName='./wordDictionaries/finalGeneSymbols.txt'
	neutralFileName='./wordDictionaries/neutralWords.txt'
	negationsFileName='./wordDictionaries/negations.txt'
	negFileName='./wordDictionaries/negWords.txt'
	posSet= set(associationFinder.readf(posFileName))
	seta= set(associationFinder.readf(geneFileName))
	negSet= set(associationFinder.readf(negFileName))
	neutralSet= set(associationFinder.readf(neutralFileName))
	negationSet= set(associationFinder.readf(negationsFileName))

	listOfrelationships=[]
	leftIds=[]
	for abstractId in ids:
		if len(UselessAbstract.objects.filter(abstractId=abstractId))>0:
			continue
		if len(ParsedSentence.objects.filter(abstractId=abstractId))>0:
			listOfSentences=ParsedSentence.objects.filter(abstractId=abstractId)
			# Parse it to listof relationships
			for each in listOfSentences:
				listOfrelationships.append([each.abstractId,each.sentence,each.gene1,each.gene2,each.relationship])

		else:
			# print abstractId
			leftIds.append(abstractId)
	for abstractId in leftIds:
		abstract=http.request('GET',
			'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+\
			abstractId+'&retmode=text&rettype=abstract')

	

		parsedList=associationFinder.OutputRelations(abstract.data,seta,negSet,neutralSet,negationSet,posSet)
		# if len(parsedList)>0:
		# print parsedList
		if len(parsedList)==0:
			uselessAbstract=UselessAbstract(abstractId=abstractId)
			uselessAbstract.save()

		for sentence in parsedList:
			[pmid,rawsentence,gene1,gene2,relationship]=sentence
			# print pmid

			newSentence= ParsedSentence(abstractId=pmid,sentence=rawsentence,
				gene1=gene1,gene2=gene2,relationship=relationship,disease=disease,score=relationship*100)
			newSentence.save()
			listOfrelationships.append([pmid,rawsentence,gene1,gene2,relationship])

	# print listOfrelationships

	visual.makeGraph(listOfrelationships,disease)
	svg='/static/webserver/diseases/'+disease+'/result.svg'
	newGraph=Graph(path=svg,disease=disease)
	newGraph.save()
	context['svg']=svg
	return render(request,'webserver/result.html',context)


@login_required
def history(request):
	histories=History.objects.filter(user=request.user)
	context={}
	context['histories']=histories
	return render(request,'webserver/history.html',context)

@login_required
def historyDisease(request,disease):
	context={}
	graph=Graph.objects.get(disease=disease)
	context['svg']=graph.path
	# print context
	return render(request,'webserver/result.html',context)

@login_required
def learnedKnowledge(request):
	context={}
	unsure=ParsedSentence.objects.filter(relationship=2)
	
	pos=ParsedSentence.objects.filter(relationship=1)
	neg=ParsedSentence.objects.filter(relationship=-1)
	if len(pos)>5:
		pos=pos[0:5]
	else:
		pos=pos[0:len(pos)]
	print pos
	if len(neg)>5:
		neg=neg[0:5]
	else:
		neg=neg[0:len(neg)]
	unsure=unsure[0:6]
	print type(unsure),type(pos),type(neg)
	unsure=list(unsure)+list(pos)+list(neg)
	random.shuffle(unsure)
	context['unsure']=unsure
	return render(request,'webserver/learned.html',context)
