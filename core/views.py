from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse

from django.utils import timezone
from datetime import datetime, timedelta

from .models import product, tags, links, adverts
from .forms import ProductForm, EmailForm, AdvertForm

"""
	def blog_create(request):
	    if request.user.is_superuser:# or not request.user.is_staff or not request.user.is_superuser:
	        pass
	    else:
	        raise Http404
	    form = BlogForm(request.POST or None, request.FILES or None)
	    if form.is_valid():
	        instance = form.save(commit=False)
	        # instance.user = request.user
	        instance.save()
	        messages.success(request, "Successfully Created")
	        return HttpResponseRedirect(instance.get_absolute_url())
	    context = {
	        "nbar" : "blog",
	        "form": form,
	        "tab_text": "New Blog Post",
	        "top_text": "New Blog!",
	        "form_text": "Here you can write your blog using the tools provided below.",
	    }
	    return render(request, 'general_form.html', context)
"""

def user_profile(request, username=None):
	# print(type(username))
	products = product.objects.filter(user__username=username)
	# for product_ in products:
		# print(product_)
	context = {
		# "page" : 'full-page',
		"products" : products,
		"show_ads" : False,

	}
	return render(request, 'user_profile.html', context)

@login_required
def create_product(request, username=None):

	# print(request.user)
	# print(username)
	if not request.user.is_authenticated:
		raise Http404

	form = ProductForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		form.save_m2m()

		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		'form' : form,
		"tab_text": "Submit Product",
		"top_text": "New Product",
		"form_text": "Please enter all the information below.",

	}
	return render(request, 'general_form.html', context)


def edit_product(request, username=None, slug=None):

	context = {
		"item" : "item",
	}
	return render(request, 'general_form.html', context)
"""

	@login_required
	def blog_update(request, slug= None):
	    instance = get_object_or_404(Post, slug=slug)
	    if instance.user != request.user:
	        raise Http404
	    form = BlogForm(request.POST or None, request.FILES or None, instance = instance)
	    if form.is_valid():
	        instance = form.save(commit=False)
	        instance.save()
	        messages.success(request, "Blog Edited Successfully!!")
	        return  HttpResponseRedirect(instance.get_absolute_url())
	    context = {
	        "dis_play" : "mode_174",
	        "nbar" : "blog",
	        "form":form,
	        "tab_text": "Edit Blog Post",
	        "top_text": "Editing tools",
	        "form_text": "You can make changes to the blog here!",
	        'this_blog': instance,
	    }
	    return render(request, "general_form.html", context)	
"""
@login_required
def all_advert(request, username=None):
	advert = adverts.objects.filter(user__username=username)
	context = {
		"show_ads" : True,
		'all_adverts' : advert,
	}
	return render(request, 'core/all_adverts.html', context)

@login_required
def create_advert(request, username=None):
	self_products = product.objects.filter(user__username=username)

	form = AdvertForm(request.POST or None, request.FILES or None)
	# overriding the field to show only the products created by this user
	form.fields['customer'].queryset = self_products

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		d = timedelta(days=instance.advert_lifespan)
		instance.advert_end = datetime.now() + d
		
		instance.save()
		form.save_m2m()

		return HttpResponseRedirect(reverse('user:all_advert', args=[username]))#instance.get_absolute_url())
	context = {
		'form' : form,
		"tab_text": "Submit Advert",
		"top_text": "Create New Advert!",
		"form_text": "Please enter all the information below.",

	}
	return render(request, 'general_form.html', context)

def edit_advert(request):
	context = {
		"item" : "item",
	}
	return render(request, 'general_form.html', context)

def advert_redirect(request, id=None):
	
	# advert = get_object_or_404(adverts, id=id)
	advert = adverts.objects.filter(id=id)

	for ad in advert:
		newlink = ad.customer.website
		# print(newlink)
		ad.current_clicks += 1
		if timezone.now() > ad.advert_end:
			# if the number of clicks are equal to requested clicks, turn off the advert status
			ad_contract_completion(ad)
		else:
			pass
		ad.save()

	return HttpResponseRedirect(newlink)
	# return render(request, 'core/all_products.html', context)

def ad_contract_completion(ad):
	ad.advert_status = adverts.AD_STATUS[3][0]
	pass

def index(request):
	ads = fetch_adverts()
	products_ = product.objects.all()
	tags_ = tags.objects.all()
	links_ = links.objects.all()


	query = request.GET.get("q")
	if query:
		products_ = products_.filter(
			Q(product_name__icontains=query)|
			Q(twin__product_name__icontains=query)
		).distinct()

	paginator = Paginator(products_, 10) # show 10 Blogs per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		_products = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		_products = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		_products = paginator.page(paginator.num_pages)


	context = {
		"products_" : _products,
		"tags_" : tags_,
		"links_" : links_,
		"ads" : ads,
        "page_request_var" : page_request_var,		
		"show_ads" : True,
	}
	return render(request, 'core/all_products.html', context)

import random

def fetch_adverts():
	LOAD_ADS = 3
	num_list = []
	# fetch ads
	fetch_ = adverts.objects.filter(advert_status="Paid")
	# fetch the total number of ads available
	limit_ = fetch_.count()
	if limit_ == 0:
		return None
	elif limit_ <= LOAD_ADS:
		rand_ad = fetch_[:limit_]
	else:
		# generate 3 number from the limited range
		num_list = random.sample(range(0, limit_), LOAD_ADS)
		# fetch those ads
		rand_ad = [fetch_[num] for num in num_list]

	print(rand_ad)
	# mark those ads with viewed!
	mark_viewed(rand_ad)
	return rand_ad


def mark_viewed(rand_ad):
	for ad in rand_ad:
		# increment the advert_view field
		ad.advert_view += 1
		ad.save()
		# print(ad.advert_view)
	pass


"""
	get the product

	get product's twins
	all the M2M it is connected
"""
def product_detail(request, slug=None):
	this_product = get_object_or_404(product, slug=slug)
	inspired_twins = product.objects.filter(twin=this_product)
	market_cap = 0
	# print("This products revenue > " + str(this_product.monthly_revenue))

	for g1 in this_product.twin.all():
		market_cap += g1.monthly_revenue
		# print("Other player's revenue > " + str(g1.monthly_revenue))

	for g2 in inspired_twins.all():
		market_cap += g2.monthly_revenue
		# print("Other player's revenue > " + str(g2.monthly_revenue))

	# print("market revenue > " + str(market_cap))
	ads = fetch_adverts()
	links_ = links.objects.filter(social_connection=this_product)

	context = {
		"product" : this_product,
		"inspired_twins" : inspired_twins,
		"links_" : links_,
		"ads" : ads,
		"show_ads" : True,
		"market_cap" : market_cap,
	}
	return render(request, 'core/product_detail.html', context)

'''
	List of all tags with
		1. tag name
		2. number of products with that tag
		3. total estimated market cap caculated with summing all revenue
'''
def all_tags(request):
	return render(request, 'core/twinslist.html')


def tag_detail(request, slug=None):
	return render(request, 'core/twinslist.html')


def lander(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('user:home'))
	else:
		pass

	form = EmailForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'page' : 'full-page',
		'form' : form,
	}

	return render(request, 'lander.html', context)
