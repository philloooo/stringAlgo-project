from django import forms
from django.contrib.auth.models import User
from models import *
class regiForm(forms.Form):
	username=forms.CharField(max_length=20)
	password1=forms.CharField(max_length=10,\
				label="Password",
				widget=forms.PasswordInput())
	password2=forms.CharField(max_length=10,\
				label="Confirm password",
				widget=forms.PasswordInput())
	email=forms.EmailField(max_length=200)
	def clean(self):
		cleaned_data=super(regiForm,self).clean()
		p1=cleaned_data.get('password1')
		p2=cleaned_data.get('password2')
		if p1!=p2:
			raise forms.ValidationError('Passwords did not match')
		return cleaned_data