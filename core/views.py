from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse

from django.utils import timezone
from datetime import datetime, timedelta

from .models import product, tags, links, adverts, product_catagory
from .forms import ProductForm, EmailForm, AdvertForm
import random
from . import catagory_utils, advert_utils

@login_required
def create_product(request, username=None):
	if not request.user.is_authenticated:
		raise Http404

	form = ProductForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		form.save_m2m()
		catagory_utils.set_revenue_details(instance.catagory.slug)
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
		"top_text": "Buy New Advert!",
		"form_text": "Either enter the Ad words, or Upload an Image. NOT BOTH.",

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
			advert_utils.ad_contract_completion(ad)
		else:
			pass
		ad.save()

	return HttpResponseRedirect(newlink)

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

def index(request):
	ads = advert_utils.fetch_adverts()
	products_ = product.objects.all()
	tags_ = tags.objects.all()
	links_ = links.objects.all()


	query = request.GET.get("q")
	if query:
		products_ = products_.filter(
			Q(product_name__icontains=query)|
			Q(product_pitch__icontains=query)|
			Q(catagory__catagory_name__icontains=query)|
			Q(catagory__catagory_pitch__icontains=query)|
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

def catagory_list(request):
	all_cats = product_catagory.objects.annotate(number_of_products=Count('catagory', distinct=True))
	"""
	I have no idea why I am counting catagory,								^^^^^^^
	I should be counting "product" to find out the number of products each catagory is connected. 
	DONT CHANGE
	"""
	ads = advert_utils.fetch_adverts()
	context = {
		"all_cats" : all_cats,
		"ads" : ads,
		"show_ads" : True,
	}
	return render(request, 'core/catagory_list.html', context)

def catagory_detail(request, slug=None):
	this_cat = get_object_or_404(product_catagory, slug=slug)
	products_ = product.objects.filter(catagory__slug=slug).order_by('-updated')
	
	total_revenue, avg_revenue, high_revenue = catagory_utils.revenue_details(this_cat, products_)

	query = request.GET.get("q")
	if query:
		products_ = products_.filter(
			Q(product_name__icontains=query)|
			Q(product_pitch__icontains=query)|
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

	ads = advert_utils.fetch_adverts()

	context = {
		'this_cat' : this_cat,
		'products_' : products_,
        "page_request_var" : page_request_var,
    	'total_revenue' : total_revenue,
    	'avg_revenue' : avg_revenue,
    	'high_revenue' : high_revenue,
    	"ads" : ads,
		"show_ads" : True,
	}
	return render(request, 'core/catagory_detail.html', context)





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

	# products from same catagory

	this_catagory = product.objects.filter(catagory=this_product.catagory).exclude(id=this_product.id)
	# print(this_catagory)

	for g1 in this_product.twin.all():
		market_cap += g1.monthly_revenue
		# print("Other player's revenue > " + str(g1.monthly_revenue))

	for g2 in inspired_twins.all():
		market_cap += g2.monthly_revenue
		# print("Other player's revenue > " + str(g2.monthly_revenue))

	# print("market revenue > " + str(market_cap))
	ads = advert_utils.fetch_adverts()
	links_ = links.objects.filter(social_connection=this_product)

	context = {
		"product" : this_product,
		"inspired_twins" : inspired_twins,
		"links_" : links_,
		"ads" : ads,
		"market_cap" : market_cap,
		'this_catagory' : this_catagory,
		"show_ads" : False,
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
