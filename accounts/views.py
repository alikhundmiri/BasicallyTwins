from django.conf import settings
from django.urls import reverse

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
	dbug = settings.DEBUG
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		# change redirect to profile page
		return HttpResponseRedirect(reverse('user:home'))
	context = {
		"name_nav" : 'login',
		"nbar" : "login",
		"form" : form,
		"dbug" : dbug,
		'page' : 'full-page',
	}
	return render(request, 'accounts/login.html', context)

def register_view(request):
	dbug = settings.DEBUG
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		# change redirect to profile page
		return HttpResponseRedirect(reverse('user:home'))
	context = {
		"name_nav" : 'register',	
		"nbar" : "register",
		"form":form,
		'dbug' : dbug,
		'page' : 'full-page',
	}
	return render(request, 'accounts/login.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')