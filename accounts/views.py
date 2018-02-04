from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from social_django.models import UserSocialAuth

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
	next = ""

	if request.GET:  
		next = request.GET['next']

	dbug = settings.DEBUG
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		if next == "":
			return HttpResponseRedirect(reverse('user:home'))
		else:
			return HttpResponseRedirect(next)

	context = {
		"name_nav" : 'login',
		"nbar" : "login",
		"form" : form,
		"dbug" : dbug,
		'page' : 'full-page',

	}
	return render(request, 'accounts/login.html', context)

def register_view(request):
	next = ""

	if request.GET:
		next = request.GET['next']

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
		if next == "":
			return HttpResponseRedirect(reverse('user:home'))
		else:
			return HttpResponseRedirect(next)
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

@login_required
def user_settings(request):
	user = request.user

	try:
		twitter_login = user.social_auth.get(provider='twitter')
	except UserSocialAuth.DoesNotExist:
		twitter_login = None

	can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

	return render(request, 'accounts/settings.html', {
		'twitter_login': twitter_login,
		'can_disconnect': can_disconnect
	})

@login_required
def user_password(request):
	if request.user.has_usable_password():
		PasswordForm = PasswordChangeForm
	else:
		PasswordForm = AdminPasswordChangeForm

	if request.method == 'POST':
		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Your password was successfully updated!')
			return redirect('password')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordForm(request.user)
	return render(request, 'accounts/password.html', {'form': form})	