from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from .models import UserProfile


from .forms import CreateUserForm, AuthenticateForm


def login_view(request):
	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			print "logged in holmes"
			return HttpResponseRedirect('profile_home')
		else: 
			return HttpResponseRedirect('/')
	else: 
		return HttpResponseRedirect('/')


def signup(request):
	form = CreateUserForm(data=request.POST)
	if request.method == 'POST':
		if form.is_valid():
			birthday = request.POST['birthday']
			gender = request.POST['gender']
			username = form.clean_username()
			password = form.clean_password2()
			form.save()
			user = authenticate(username=username, password=password)
			new_profile = UserProfile(user=user)
			new_profile.birthday = birthday
			new_profile.gender = gender
			new_profile.save()
			login(request, user)
			return HttpResponseRedirect('profile_home')
		else: 
			return HttpResponseRedirect('/')
	else:
		form  = CreateUserForm
		return render_to_response('registration.html', {'form': form},  
			 context_instance=RequestContext(request))