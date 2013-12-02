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
	print disease
	# store the history
	if len(History.objects.filter(user=request.user,disease=disease))==0:
		history=History(user=request.user,disease=disease)
		history.save()

	parsed='+'.join(disease.split())
	http = urllib3.PoolManager()
	r = http.request('GET', 
		'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='+\
		parsed+'+AND+2013[pdat]&usehistory=y')
	XML=ET.fromstring(r.data)
	ids=[]
	for child in XML:
		if child.tag=='IdList':
			# print child
			for cid in child:
				# print cid.text
				ids.append(cid.text)


	# get abstract
	listOfrelationships=[]
	leftIds=[]
	for abstractId in ids:
		if len(ParsedSentence.objects.filter(abstractId=abstractId))>1:
			listOfSentences=ParsedSentence.objects.filter(abstractId=abstractId)
			# Parse it to listof relationships
			for each in listOfSentences:
				listOfrelationships.append([each.abstractId,each.sentence,each.gene1,each.gene2,each.relationship])

		else:
			leftIds.append(abstractId)
	for abstractId in leftIds:
		abstract=http.request('GET',
			'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+\
			abstractId+'&retmode=text&rettype=abstract')
		print abstract.data
	# 		parsedList=parseAbstract(abstract.data)

	# 		for sentence in parsedList:
	# 			[pmid,rawsentence,gene1,gene2,relationship]=sentence
	# 			newSentence=ParsedSentence(abstractId=int(pmid),sentence=rawsentence,
	# 				gene1=gene1,gene2=gene2,relationship=relationship,disease=disease)
	# 			newSentence.save()
	# 			listOfrelationships.append([pmid,rawsentence,gene1,gene2,relationship])



	# makeGraph(listOfrelationships)

	return render(request,'webserver/result.html',context)


@login_required
def history(request):
	histories=History.objects.filter(user=request.user)
	context={}
	context['histories']=histories
	return render(request,'webserver/history.html',context)
	