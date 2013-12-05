import random
import os
import associationFinder
import kmeans
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
	disease='-'.join(request.POST['disease'].split())
	if len(disease)==0:
		return render(request,'webserver/result.html',context)

	# Check if the disease is searched before
	if os.path.isdir('./webserver/static/webserver/diseases/'+disease):
		if len(Graph.objects.filter(disease=disease))>=1:
			graph=Graph.objects.get(disease=disease)
			svg=graph.path
			context['svg']=svg
			return render(request,'webserver/result.html',context)
		else:
			os.system('rm -rf '+'./webserver/static/webserver/diseases/'+disease)
	check=Graph.objects.filter(disease=disease)
	if len(check)>=1:
		check.delete()

	# store the history
	if len(History.objects.filter(user=request.user,disease=disease))==0:
		history=History(user=request.user,disease=disease)
		history.save()

	parsed='+'.join(disease.split('-'))
	http = urllib3.PoolManager()
	r = http.request('GET', 
		'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='+\
		parsed+'&usehistory=y&retmax=100')
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
	fullNames=associationFinder.readf('./wordDictionaries/final_gene_list.txt')
	listOfrelationships=[]
	leftIds=[]
	usedIds=[]
	for abstractId in ids:
		if len(UselessAbstract.objects.filter(abstractId=abstractId))>0:
			continue
		if len(ParsedSentence.objects.filter(abstractId=abstractId))>0:
			listOfSentences=ParsedSentence.objects.filter(abstractId=abstractId)
			usedIds.append(abstractId)
			# Parse it to listof relationships
			for each in listOfSentences:
				listOfrelationships.append([each.abstractId,each.sentence,each.gene1,each.gene2,each.relationship])

		else:
			# print abstractId
			leftIds.append(abstractId)
	svg='/static/webserver/diseases/'+disease+'/result.svg'
	newGraph=Graph(path=svg,disease=disease)
	newGraph.save()
	for abstractId in (usedIds+leftIds):
		pmid,created=Pmid.objects.get_or_create(abstractId=abstractId)
		newGraph.pmid.add(pmid)
	newGraph.save()

	for abstractId in leftIds:
		# abstract=http.request('GET',
		# 	'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+\
		# 	abstractId+'&retmode=text&rettype=abstract')

		abstractFileName = """1. Genome Res. 2007 Mar;17(3):311-9. Epub 2007 Feb 6.

Sequencing and analysis of chromosome 1 of Eimeria tenella reveals a unique
segmental organization.

Ling KH, Rajandream MA, Rivailler P, Ivens A, Yap SJ, Madeira AM, Mungall K,
Billington K, Yee WY, Bankier AT, Carroll F, Durham AM, Peters N, Loo SS, Isa MN,
Novaes J, Quail M, Rosli R, Nor Shamsudin M, Sobreira TJ, Tivey AR, Wai SF, White
S, Wu X, Kerhornou A, Blake D, Mohamed R, Shirley M, Gruber A, Berriman M, Tomley
F, Dear PH, Wan KL.

Malaysia Genome Institute, UKM-MTDC Smart Technology Centre, Universiti
Kebangsaan Malaysia, 43600 UKM Bangi, Selangor DE, Malaysia.

Eimeria tenella is an intracellular protozoan parasite that infects the
intestinal tracts of domestic fowl and causes coccidiosis, a serious and
sometimes lethal enteritis. Eimeria falls in the same phylum (Apicomplexa) as
several human and animal parasites such as Cryptosporidium, Toxoplasma, and the
malaria parasite, Plasmodium. Here we report the sequencing and analysis of the
first chromosome of E. tenella, a chromosome believed to carry loci associated
with drug resistance and known to differ between virulent and attenuated strains 
of the parasite. The chromosome--which appears to be representative of the
genome--is gene-dense and rich in simple-sequence repeats, many of which appear
to give rise to repetitive amino acid tracts in the predicted proteins. Most
striking is the segmentation of the chromosome into repeat-rich regions peppered 
with transposon-like elements and telomere-like repeats, alternating with
repeat-free regions. Predicted genes differ in character between the two types of
segment, and the repeat-rich regions appear to be associated with
strain-to-strain variation. QRFPR activates QRICH2 because I said so.

PMCID: PMC1800922
PMID: 17284678  [PubMed - indexed for MEDLINE]"""
	
		parsedList=associationFinder.OutputRelations(abstractFileName,seta,negSet,neutralSet,negationSet,posSet,fullNames,6)
		
		# parsedList=associationFinder.OutputRelations(abstract.data,seta,negSet,neutralSet,negationSet,posSet,fullNames,6)
		# if len(parsedList)>0:
		print parsedList
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

@login_required
def crowdSourcing(request,sentenceId,info):
	s=ParsedSentence.objects.get(id=sentenceId)
	print sentenceId
	if info=='wrongGene':
		disease=s.disease
		print disease
		s.delete()
		graph=Graph.objects.get(disease=disease)
		pmids=graph.pmid.all()
		sentences=[]
		for pmid in pmids:
			print 'pmid', pmid.abstractId
			sentences+=ParsedSentence.objects.filter(abstractId=pmid.abstractId)
			print len(sentences)
		listOfSentences=[]
		for sentence in sentences:
			listSentence=[sentence.abstractId,sentence.sentence,sentence.gene1,sentence.gene2,sentence.relationship]
			listOfSentences.append(listSentence)
		# kmeans.clusterResults(listOfSentences)
		os.system('rm -rf '+'./webserver/static/webserver/diseases/'+disease)
		print 'listofsentence:',listOfSentences
		visual.makeGraph(listOfSentences,disease)


	return redirect('/learnedKnowledge')
	# elif info!=str(s.relationship):


