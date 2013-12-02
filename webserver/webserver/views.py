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

